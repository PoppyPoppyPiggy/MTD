# modules/attacker.py
import random
import logging
from datetime import datetime

logger = logging.getLogger("MTD")

class Attacker:
    def __init__(self, attack_level=1):
        self.history = []
        self.attack_log_file = "attack_log.txt"
        self.mtd_log_file = "mtd_log.txt"
        self.attack_categories = [
            "Jamming Threat",
            "Man-in-the-Middle Threat",
            "DDoS Threat",
            "Blackhole Routing Pollution Threat",
            "Wormhole Routing Pollution Threat"
        ]
        self.scanned_ports = list(range(20, 1025))  # Common port range for scanning

    def simulate_intrusion(self, defender_map):
        if not defender_map:
            logger.warning("[Attacker] Defender map is empty. No targets to scan.")
            return False

        attack_detected = False

        for ip in defender_map.values():
            for port in self.scanned_ports:
                result = self._attempt_connection(ip, port)
                self._log_scan_attempt(ip, port, result)
                if result:
                    attack_detected = True
                    self._log_detection(ip, port)

        return attack_detected

    def _attempt_connection(self, ip, port):
        return random.random() < 0.03  # 3% chance of 'open' port

    def _log_scan_attempt(self, target_ip, port, result):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Open" if result else "Closed"

        log_line = f"[{timestamp}] [Attacker] Scanned IP: {target_ip}, Port: {port}, Result: {status}\n"

        with open(self.attack_log_file, "a") as log:
            log.write(log_line)

    def _log_detection(self, ip, port):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        detection_line = f"[{timestamp}] [Detection] Attack Detected - IP: {ip}, Port: {port}\n"
        with open(self.attack_log_file, "a") as log:
            log.write(detection_line)
        with open(self.mtd_log_file, "a") as mtd_log:
            mtd_log.write(detection_line)