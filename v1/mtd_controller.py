from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import hub
from modules.attacker import AttackerSimulator
from modules.defender import Defender
from modules.evaluator import MTDEvaluator
import logging
import atexit

class MTDController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MTDController, self).__init__(*args, **kwargs)
        self._setup_logging()
        self.datapaths = {}
        self.attacker = AttackerSimulator()
        self.defender = Defender()
        self.evaluator = MTDEvaluator(self.attacker, self.defender)
        self.monitor_thread = hub.spawn(self._mtd_cycle)

    def _setup_logging(self):
        self.logger = logging.getLogger("MTD")
        self.logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler("mtd_log.txt", mode="w", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(file_handler)

        logging.getLogger().handlers = self.logger.handlers
        logging.getLogger().setLevel(logging.INFO)

        atexit.register(lambda: [h.flush() for h in self.logger.handlers])

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            self.datapaths[datapath.id] = datapath
            self.logger.info(f"Switch {datapath.id} connected.")

            # 서비스 등록: datapath.id 기준으로 3개 가상 서비스에 분배
            service_id = f"service-{datapath.id % 3}"
            self.defender.register_device(datapath.id, service_id)
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                del self.datapaths[datapath.id]
                self.logger.info(f"Switch {datapath.id} disconnected.")

    def _mtd_cycle(self):
        while True:
            hub.sleep(0.1)
            self.attacker.scan()
            self.defender.shuffle_ips(self.datapaths)
            self.evaluator.evaluate()
