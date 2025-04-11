# mtd_controller.py

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

logger = logging.getLogger("MTDController")

class MTDController(app_manager.RyuApp):
    def __init__(self, *args, **kwargs):
        super(MTDController, self).__init__(*args, **kwargs)
        self.attacker = Attacker()
        self.defender = Defender(ip_pool_size=32)
        self.evaluator = Evaluator(self.defender)
        self.mac_to_port = {}
        self.datapaths = {}

        # 주기 설정
        self.attack_interval = 1  # 공격자 침투 시도 주기 (초)
        self.shuffle_interval = self.defender.shuffle_interval  # 셔플 주기

        # MTD 평가 및 공격자 루프 쓰레드 실행
        self.monitor_thread = hub.spawn(self._mtd_cycle)
        self.attacker_thread = hub.spawn(self._attacker_cycle)

        # 테스트용 가상 datapath 등록
        self.defender.initialize_default_datapaths(num_datapaths=3)

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
        logger.info(f"[MTDController] Registered datapath {datapath.id}")

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        dst = eth.dst
        src = eth.src
        dpid = datapath.id

        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=msg.buffer_id,
                                  in_port=in_port,
                                  actions=actions,
                                  data=data)
        datapath.send_msg(out)

    def _mtd_cycle(self):
        """MTD 주기적 실행 및 평가"""
        while True:
            for ip, count in self.defender.ip_access_count.items():
                if count > 10:
                    logger.warning(f"[MTDController] Suspicious activity detected on {ip}. Triggering forced shuffle.")
                    print(f"[MTDController] 비정상 접근 감지 → {ip} 강제 셔플")
                    self.defender.shuffle_ips(force=True)

            self.evaluator.evaluate()
            hub.sleep(self.defender.shuffle_interval)

    def _attacker_cycle(self):
        """공격자 주기적 침투 시도"""
        while True:
            if self.defender.defender_map:
                result = self.attacker.simulate_intrusion(self.defender.defender_map)
                if result:
                    logger.info("[MTDController] 공격 감지됨 → IP 셔플")
                    print("[MTDController] 공격 감지됨 → IP 셔플")
                    self.defender.shuffle_ips(force=True)
                else:
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("mtd_log.txt", "a") as log:
                        log.write(f"[{timestamp}] [MTDController] 공격 실패. 감지 없음.\n")
            hub.sleep(self.defender.shuffle_interval)



