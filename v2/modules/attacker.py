import random
import logging
from datetime import datetime

logger = logging.getLogger("MTD")

class Attacker:
    def __init__(self, attack_level=1):
        self.target_ip = None
        self.history = []
        self.attack_log_file = "attack_log.txt"
        self.mtd_log_file = "mtd_log.txt"

    def choose_target(self, defender_map):
        """공격 대상 선택"""
        if not defender_map:
            logger.warning("[Attacker] Defender map is empty. No target to choose.")
            return None

        self.target_ip = random.choice(list(defender_map.values()))
        self.history.append(self.target_ip)
        logger.info(f"[Attacker] Targeting IP: {self.target_ip}")
        print(f"[Attacker] Targeting IP: {self.target_ip}")
        return self.target_ip

    def attempt_attack(self, defender_map):
        """공격 시도 및 성공 여부 기록"""
        if self.target_ip in defender_map.values():
            logger.info(f"[Attacker] Attack success on {self.target_ip}")
            print(f"[Attacker] Attack success on {self.target_ip}")
            self._log_attack_activity(self.target_ip, True)
            return True
        else:
            logger.info(f"[Attacker] Attack failed. IP changed.")
            print(f"[Attacker] Attack failed. IP changed.")
            self._log_attack_activity(self.target_ip, False)
            return False

    def simulate_intrusion(self, defender_map):
        """침입 시도"""
        target_ip = self.choose_target(defender_map)
        if not target_ip:
            logger.warning("[Attacker] No target IP selected. Skipping intrusion attempt.")
            print("[Attacker] No target IP selected. Skipping intrusion attempt.")
            return False
        return self.attempt_attack(defender_map)

    def detect(self, defender_map):
        """공격 탐지"""
        return self.simulate_intrusion(defender_map)

    def _log_attack_activity(self, target_ip, result):
        """공격 결과 로그 기록"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Success" if result else "Failure"
        log_line = f"[{timestamp}] [Attacker] Target IP: {target_ip}, Result: {status}\n"

        with open(self.attack_log_file, "a") as log:
            log.write(log_line)

        with open(self.mtd_log_file, "a") as mtd_log:
            mtd_log.write(log_line)
