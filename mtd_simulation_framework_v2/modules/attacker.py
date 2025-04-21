# modules/attacker.py
import random
import time

class Attacker:
    def __init__(self):
        self.state = "Idle"

    def trigger_attack(self, target):
        print(f"[ATTACK] Current state: {self.state}")
        if self.state == "Idle":
            self.state = "Recon"
            self.perform_scan(target)
        elif self.state == "Recon":
            self.state = "Engage"
            self.attempt_login(target)
        elif self.state == "Engage":
            self.state = "Exploit"
            self.run_payload(target)
        elif self.state == "Exploit":
            self.state = "Idle"
            print("[ATTACK] Cycle complete, resetting.")

    def perform_scan(self, target):
        print(f"[RECON] Scanning {target} for open ports...")
        time.sleep(1)

    def attempt_login(self, target):
        print(f"[ENGAGE] Attempting SSH login to {target} with brute-force...")
        time.sleep(1)

    def run_payload(self, target):
        print(f"[EXPLOIT] Deploying payload to {target} (e.g., DDoS, ARP spoofing)")
        time.sleep(1)

# 테스트 코드
if __name__ == "__main__":
    attacker = Attacker()
    for _ in range(5):
        attacker.trigger_attack("172.20.0.10")
        time.sleep(2)