import random
import logging

logger = logging.getLogger("MTD")

class Attacker:
    def __init__(self):
        self.target_ip = None
        self.history = []
        self.log_file = "attack_log.txt"

    def choose_target(self, defender_map):
        if not defender_map:
            logger.warning("[Attacker] Defender map is empty. No target to choose.")
            return None
        
        self.target_ip = random.choice(list(defender_map.values()))
        self.history.append(self.target_ip)
        logger.info(f"[Attacker] Targeting IP: {self.target_ip}")
        return self.target_ip

    def attempt_attack(self, defender_map):
        if self.target_ip in defender_map.values():
            logger.info(f"[Attacker] Attack success on {self.target_ip}")
            self._log_attack_activity(self.target_ip, True)
            return True
        else:
            logger.info(f"[Attacker] Attack failed on {self.target_ip}. IP changed or unavailable.")
            self._log_attack_activity(self.target_ip, False)
            return False

    def _log_attack_activity(self, target_ip, result):
        with open(self.log_file, "a") as log:
            log.write(f"Target IP: {target_ip}, Result: {'Success' if result else 'Failure'}\n")