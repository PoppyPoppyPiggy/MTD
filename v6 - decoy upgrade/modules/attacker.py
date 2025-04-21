import random
import logging
from datetime import datetime

logger = logging.getLogger("MTD")

class Attacker:
    def __init__(self):
        self.attack_log_file = "attack_log.txt"
        self.mtd_log_file = "mtd_log.txt"
        self.honeypot_hits = 0
        self.history = []

    def simulate_intrusion(self, defender_map, honeypot_ips=None):
        if not defender_map:
            return False

        attack_success = False
        scanned_ips = list(defender_map.values())

        for ip in scanned_ips:
            for port in random.sample(range(20, 1025), 10):
                is_open = random.random() < 0.03
                self._log_scan(ip, port, is_open)

                if is_open:
                    attack_success = True
                    self._log_detection(ip, port)
                    self.history.append(ip)

                    if honeypot_ips and ip in honeypot_ips:
                        self.honeypot_hits += 1
                        self._log_honeypot(ip, port)

        return attack_success

    def _log_scan(self, ip, port, success):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = "Open" if success else "Closed"
        with open(self.attack_log_file, "a") as log:
            log.write(f"[{timestamp}] [Attacker] Scanned IP: {ip}, Port: {port}, Result: {result}\n")

    def _log_detection(self, ip, port):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.mtd_log_file, "a") as log:
            log.write(f"[{timestamp}] [Detection] Attack Detected - IP: {ip}, Port: {port}\n")

    def _log_honeypot(self, ip, port):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.mtd_log_file, "a") as log:
            log.write(f"[{timestamp}] [Honeypot Detection] IP: {ip}, Port: {port}\n")
