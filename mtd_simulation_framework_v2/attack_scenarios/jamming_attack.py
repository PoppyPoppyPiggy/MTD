# attack_scenarios/jamming_attack.py
import random
import time

class JammingAttack:
    def __init__(self, frequencies=[2400, 2450, 2500]):
        self.frequencies = frequencies

    def execute(self):
        print("[JAMMING] Simulating radio interference across frequencies...")
        for _ in range(5):
            target_freq = random.choice(self.frequencies)
            print(f"[JAMMING] Interfering on {target_freq} MHz")
            time.sleep(1)

if __name__ == "__main__":
    atk = JammingAttack()
    atk.execute()