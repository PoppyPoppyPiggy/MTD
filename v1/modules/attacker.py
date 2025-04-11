import random
import logging
logger = logging.getLogger("MTD")

class AttackerSimulator:
    def __init__(self):
        self.ip_pool = list(range(32))
        self.attacker_history = []

    def scan(self):
        target_ip = random.choice(self.ip_pool)
        self.attacker_history.append(target_ip)
        logger.info(f"[ATTACK] Attacker scans IP: {target_ip}")
