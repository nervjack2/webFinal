from operator import attrgetter
from switch import SimpleSwitch

from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
from ryu.lib.packet import in_proto
from ryu.lib.packet import ether_types
from pca import PCA

import json
import numpy as np
import sys

class SimpleMonitor(SimpleSwitch):
    def __init__(self, *args, **kwargs):
        super(SimpleMonitor, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.init = 0
        self.monitor_thread = hub.spawn(self._monitor)

        # Record number of total packets of previous timestep
        self.record = {}

        # Record which switch we have met at each timestape
        self.switch_set = set()

        # Parameters to try in PCA detection
        self.bins = 30 
        self.time_interval = 1

        # Number of hosts in the topology
        # Modify the number according to the topology
        self.num_host = 8
        
        # Record packet count of each (src_ip, dst_ip) pair
        self.od_flow = None      
        self.flow_matrix = PCA(self.bins, self.num_host * (self.num_host-1))        
        self.timestep = 0


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
            hub.sleep(self.time_interval)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)
    
    def _init_odpair(self):
        odpair_dict = {}
        for i in range(1, self.num_host+1):
            for j in range(1, self.num_host+1):
                if i != j:
                    src_ip = '10.0.0.' + str(i)
                    dst_ip = '10.0.0.' + str(j)
                    odpair_dict[(src_ip, dst_ip)] = 0
        return odpair_dict

    def _make_row(self):
        count = 0
        odpair_to_index = {}        
        row = np.zeros(self.num_host * (self.num_host - 1))

        # Convert (src_ip, dst_ip) pair to an index
        for i in range(1, self.num_host+1):
            for j in range(1, self.num_host+1):
                if i != j:
                    src_ip = '10.0.0.' + str(i)
                    dst_ip = '10.0.0.' + str(j)                    
                    odpair_to_index[(src_ip, dst_ip)] = count
                    count += 1
                    
        # The real traffic should be the difference between
        # the current timestep and the previous timestep
        for pair, value in self.od_flow.items():                        
            row[odpair_to_index[pair]] = max(0, value - self.record[pair])

        # print('traffic at t = {:2} {}'.format(self.index+1, row))

        # update flow matrix and detect if ddos happens
        if self.timestep < self.bins:
            self.flow_matrix.init_data_matrix(row, self.timestep)        
        else:
            self.flow_matrix.update_data(row)
            ddos, _ = self.flow_matrix.detect_ddos()
            if ddos:
                print('At t = {} ddos detected!'.format(self.timestep+1))
            else:
                print('At t = {} normal traffic'.format(self.timestep+1))
                
        self.timestep += 1
        self.record = self.od_flow
        self.od_flow = self._init_odpair()        
        self.switch_set = set()
        
    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body        

        if not self.init:
            self.od_flow = self._init_odpair()
            self.record = self._init_odpair()
            self.init = 1

        # If the switch appears again, the next timestep is about to begin
        # Thus we need to record the traffic of the current step first
        _id = ev.msg.datapath.id            
        if _id in self.switch_set:            
            self._make_row()        
        self.switch_set.add(_id)

        '''
        # print monitor information
        # uncommnent if needed
        if self.timestep % self.bins == 0:
            self.logger.info('datapath'
                             '          in-port       src_ip'
                             '       dst_ip'
                             '  action packets    bytes')
            self.logger.info('---------------- '
                             '-------- ------------ '
                             '------------'
                             ' ------- ------- --------')                
        '''

        for e,stat in enumerate(body):
            if stat.priority != 1:
                continue
            if stat.match['eth_type'] != ether_types.ETH_TYPE_IP:
                continue

            src_ip = stat.match['ipv4_src']
            dst_ip = stat.match['ipv4_dst']
            out_port = stat.instructions[0].actions[0].port
            out_port = f'port {out_port}'        

            '''
            # print monitor information
            # uncommnent if needed
            if self.timestep % self.bins == 0:
                self.logger.info('%016x %8x '
                                 '%12s %12s '
                                 '%7s %7d %8d',
                                 ev.msg.datapath.id, stat.match['in_port'],
                                 src_ip, dst_ip,
                                 out_port, stat.packet_count, stat.byte_count)
            '''

            # The same (src_ip, dst_ip) can be recorded in different switches
            # However their packet count and bytes count could differ
            # Here we retrieve the largest number
            od_key_pair = (src_ip, dst_ip)
            self.od_flow[od_key_pair] = max(stat.packet_count, self.od_flow[od_key_pair])
                        
