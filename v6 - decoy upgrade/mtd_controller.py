from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import packet, ethernet
from ryu.lib import hub

from modules.attacker import Attacker
from modules.defender import Defender
from modules.evaluator import Evaluator
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MTDController")

class MTDController(app_manager.RyuApp):
    def __init__(self, *args, **kwargs):
        super(MTDController, self).__init__(*args, **kwargs)
        self.defender = Defender(ip_pool_size=32)
        self.attacker = Attacker()
        self.evaluator = Evaluator(self.defender)
        self.mac_to_port = {}
        self.datapaths = {}

        self.attack_interval = 1
        self.shuffle_interval = self.defender.shuffle_interval

        self.monitor_thread = hub.spawn(self._mtd_cycle)
        self.attacker_thread = hub.spawn(self._attacker_cycle)
        self.defender.initialize_default_datapaths(num_datapaths=5)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(datapath.ofproto.OFPP_CONTROLLER,
                                          datapath.ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        self.defender.register_datapath(datapath.id)
        self.datapaths[datapath.id] = datapath
        logger.info(f"[MTDController] Registered datapath {datapath.id}")

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath, priority=priority, match=match,
            instructions=inst, buffer_id=buffer_id if buffer_id else ofproto.OFP_NO_BUFFER
        )
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        dpid = msg.datapath.id
        in_port = msg.match['in_port']
        dst = eth.dst
        src = eth.src

        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src] = in_port
        out_port = self.mac_to_port[dpid].get(dst, msg.datapath.ofproto.OFPP_FLOOD)
        actions = [msg.datapath.ofproto_parser.OFPActionOutput(out_port)]

        out = msg.datapath.ofproto_parser.OFPPacketOut(
            datapath=msg.datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=msg.data if msg.buffer_id == msg.datapath.ofproto.OFP_NO_BUFFER else None
        )
        msg.datapath.send_msg(out)

    def _mtd_cycle(self):
        while True:
            for ip, count in self.defender.ip_access_count.items():
                if count > 10:
                    logger.warning(f"[MTDController] Suspicious access → {ip}")
                    self.defender.shuffle_ips(force=True)
            self.evaluator.evaluate()
            hub.sleep(self.shuffle_interval)

    def _attacker_cycle(self):
        while True:
            if self.defender.defender_map:
                result = self.attacker.simulate_intrusion(
                    self.defender.defender_map,
                    honeypot_ips=self.defender.honeypot_ips
                )
                if result:
                    for ip in self.attacker.history[-1:]:
                        for dpid, assigned_ip in self.defender.defender_map.items():
                            if assigned_ip == ip:
                                label = "[HONEYPOT]" if dpid == self.defender.honeypot_dp else "[NORMAL]"
                                logger.info(f"[MTDController] 공격 감지됨 {label} Datapath {dpid} → IP: {ip}")
                                if dpid == self.defender.honeypot_dp:
                                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    with open("mtd_log.txt", "a") as log:
                                        log.write(f"[{timestamp}] [Honeypot Detection] IP: {ip}, Port: unknown\n")
                                break
                    self.defender.shuffle_ips(force=True)
            hub.sleep(self.shuffle_interval)
