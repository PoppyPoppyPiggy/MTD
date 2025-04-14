# modules/defender.py
from datetime import datetime
import random
import logging
from modules.evaluator import Evaluator
from modules.categorization import ThreatCategorization

logger = logging.getLogger("MTD")

class Defender:
    def __init__(self, ip_pool_size=32, shuffle_interval=5):
        self.ip_pool_size = ip_pool_size
        self.shuffle_interval = shuffle_interval
        self.defender_map = {}
        self.ip_access_count = {}
        self.energy_consumed = 0
        self.mtd_log_file = "mtd_log.txt"

        self.evaluator = Evaluator(self)
        self.honeypot_pool = ["10.0.0.200", "10.0.0.201"]  # 사전 정의된 허니팟 IP
        self.categorizer = ThreatCategorization()

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
        for dpid in self.defender_map:
            new_ip = self._generate_random_ip()
            self.defender_map[dpid] = new_ip
            self.ip_access_count[new_ip] = 0
            self.energy_consumed += 1
            logger.info(f"[Defender] Datapath {dpid} IP changed to {new_ip}")
            self._log_ip_change(dpid, new_ip)

        self.evaluator.evaluate()

    def deploy_honeypot(self):
        for ip in self.honeypot_pool:
            logger.info(f"[Defender] Honeypot deployed at {ip}")
            with open(self.mtd_log_file, "a") as log:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log.write(f"[{timestamp}] [Defender] Honeypot deployed at {ip}\n")

    def analyze_threat_and_respond(self, threat_type):
        strategy = self.categorizer.get_response_strategy(threat_type)
        logger.info(f"[Defender] Threat type: {threat_type}, Strategy: {strategy['response']}")
        if strategy["use_honeypot"]:
            self.deploy_honeypot()
        self.shuffle_ips(force=True)

    def check_honeypot_triggered(self, target_ip):
        if target_ip in self.honeypot_pool:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.mtd_log_file, "a") as log:
                log.write(f"[{timestamp}] [Defender] Honeypot triggered by attack on {target_ip}\n")
            logger.warning(f"[Defender] Honeypot triggered! Attack on {target_ip}")
            return True
        return False

    def _generate_random_ip(self):
        return f"10.0.0.{random.randint(1, self.ip_pool_size)}"

    def _log_ip_change(self, dpid, new_ip):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.mtd_log_file, "a") as log:
            log.write(f"[{timestamp}] [Defender] Datapath {dpid} → New IP: {new_ip}\n")
