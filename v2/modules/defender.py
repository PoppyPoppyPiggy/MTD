from datetime import datetime
import random
import logging
from modules.evaluator import Evaluator  # evaluator import 추가

logger = logging.getLogger("MTD")

class Defender:
    def __init__(self, ip_pool_size=32, shuffle_interval=5):
        self.ip_pool_size = ip_pool_size
        self.shuffle_interval = shuffle_interval
        self.defender_map = {}
        self.ip_access_count = {}
        self.energy_consumed = 0
        self.mtd_log_file = "mtd_log.txt"

        self.evaluator = Evaluator(self)  # evaluator 인스턴스 생성

    def initialize_default_datapaths(self, num_datapaths=3):
        for dpid in range(1, num_datapaths + 1):
            ip = self._generate_random_ip()
            self.defender_map[dpid] = ip
            self.ip_access_count[ip] = 0

    def register_datapath(self, dpid):
        ip = self._generate_random_ip()
        self.defender_map[dpid] = ip
        self.ip_access_count[ip] = 0

    def shuffle_ips(self, force=False):
        """IP 변경 수행"""
        for dpid in self.defender_map:
            new_ip = self._generate_random_ip()
            self.defender_map[dpid] = new_ip
            self.ip_access_count[new_ip] = 0
            self.energy_consumed += 1
            logger.info(f"[Defender] Datapath {dpid} IP changed to {new_ip}")
            print(f"[Defender] Datapath {dpid} IP changed to {new_ip}")
            self._log_ip_change(dpid, new_ip)

        # 평가 지표 자동 기록
        self.evaluator.evaluate()

    def _generate_random_ip(self):
        return f"10.0.0.{random.randint(1, self.ip_pool_size)}"

    def _log_ip_change(self, dpid, new_ip):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.mtd_log_file, "a") as log:
            log.write(f"[{timestamp}] [Defender] Datapath {dpid} → New IP: {new_ip}\n")
