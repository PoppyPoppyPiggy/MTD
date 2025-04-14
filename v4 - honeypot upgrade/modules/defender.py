# modules/defender.py
from datetime import datetime
import random
import logging
from modules.evaluator import Evaluator

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

        self.honeypot_dp = 5
        self.honeypot_ips = []

    def initialize_default_datapaths(self, num_datapaths=5):
        for dpid in range(1, num_datapaths + 1):
            ip = self._generate_random_ip()
            self.defender_map[dpid] = ip
            self.ip_access_count[ip] = 0

            if dpid == self.honeypot_dp:
                self.honeypot_ips = [ip]
                self._log(f"[Defender] Honeypot assigned → Datapath {dpid} → {ip}")

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

            label = "[HONEYPOT]" if dpid == self.honeypot_dp else "[NORMAL]"
            if dpid == self.honeypot_dp:
                self.honeypot_ips = [new_ip]
            self._log(f"[Defender] {label} Datapath {dpid} IP changed to {new_ip}")

        self.evaluator.evaluate()

    def _generate_random_ip(self):
        return f"10.0.0.{random.randint(1, self.ip_pool_size)}"

    def _log(self, line):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.mtd_log_file, "a") as log:
            log.write(f"[{timestamp}] {line}\n")
