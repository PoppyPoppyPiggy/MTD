# attack_scenarios/jamming_attack.py
import random
import time

class JammingAttack:
    def __init__(self, frequencies=[2400, 2450, 2500]):
        self.frequencies = frequencies

    def execute(self):
        print("[JAMMING] Simulating RF interference across frequencies...")
        for _ in range(10):
            freq = random.choice(self.frequencies)
            print(f"[JAMMING] Interference at {freq} MHz")
            time.sleep(1)

if __name__ == "__main__":
    atk = JammingAttack()
    atk.execute()
