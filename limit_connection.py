def limit_connection(datapath, ofproto, ofparser):
    """ Configure meter """
    b1 = ofparser.OFPMeterBandDscpRemark(rate=10, prec_level=1)
    req = ofparser.OFPMeterMod(datapath, command=ofproto.OFPMC_ADD, flags=ofproto.OFPMF_PKTPS, meter_id=1, bands=[b1])
    datapath.send_msg(req)

 @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        ### add mitigation ###
        this.limit_connection(datapath, ofproto, parser)
        ###