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

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("mtd_log.txt"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("MTD")

class MTDController(app_manager.RyuApp):
    def __init__(self, *args, **kwargs):
        super(MTDController, self).__init__(*args, **kwargs)
        self.attacker = Attacker()
        self.defender = Defender(ip_pool_size=32)
        self.evaluator = Evaluator(self.defender)
        self.mac_to_port = {}
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._mtd_cycle)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        self.defender.register_datapath(datapath.id)
        self.datapaths[datapath.id] = datapath

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                 match=match, instructions=inst)
        datapath.send_msg(mod)

    def _mtd_cycle(self):
        while True:
            for ip, count in self.defender.ip_access_count.items():
                if count > 10:
                    logger.warning(f"[MTDController] Suspicious activity detected on {ip}. Triggering forced shuffle.")
                    self.defender.shuffle_ips(force=True)
            hub.sleep(self.defender.shuffle_interval)