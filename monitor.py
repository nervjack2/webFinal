from operator import attrgetter
from switch import SimpleSwitch

from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
from ryu.lib.packet import in_proto

import json


class SimpleMonitor(SimpleSwitch):

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(5)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body
        
        self.logger.info('datapath'
                         '          in-port       src_ip src_port'
                         '       dst_ip dst_port protocol'
                         '  action packets    bytes')
        self.logger.info('---------------- '
                         '-------- ------------ -------- '
                         '------------ -------- --------'
                         ' ------- ------- --------')        

        for stat in [flow for flow in body if flow.priority == 1]:
            out_port = stat.instructions[0].actions[0].port
            out_port = f'port {out_port}'
            
            if stat.match['ip_proto'] == in_proto.IPPROTO_ICMP:
                src_port = 'N/A'
                dst_port = 'N/A'
                protocol = 'ICMP'
                
            elif stat.match['ip_proto'] == in_proto.IPPROTO_TCP:
                src_port = stat.match['tcp_src']
                dst_port = stat.match['tcp_dst']
                protocol = 'TCP'

            elif stat.match['ip_proto'] == in_proto.IPPROTO_UDP:
                src_port = stat.match['udp_src']
                dst_port = stat.match['udp_dst']
                protocol = 'UDP'
            
            self.logger.info('%016x %8x '
                             '%12s %8s '
                             '%12s %8s %8s '
                             '%7s %7d %8d',
                             ev.msg.datapath.id, stat.match['in_port'],
                             stat.match['ipv4_src'], src_port,
                             stat.match['ipv4_dst'], dst_port, protocol,
                             out_port, stat.packet_count, stat.byte_count)
            

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body

        self.logger.info('datapath         port     '
                         'rx-pkts  rx-bytes rx-error '
                         'tx-pkts  tx-bytes tx-error')
        self.logger.info('---------------- -------- '
                         '-------- -------- -------- '
                         '-------- -------- --------')
        for stat in sorted(body, key=attrgetter('port_no')):
            self.logger.info('%016x %8x %8d %8d %8d %8d %8d %8d',
                             ev.msg.datapath.id, stat.port_no,
                             stat.rx_packets, stat.rx_bytes, stat.rx_errors,
                             stat.tx_packets, stat.tx_bytes, stat.tx_errors)
