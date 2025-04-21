# attack_scenarios/blackhole_attack.py
import time

class BlackholeAttack:
    def __init__(self, target_node):
        self.node = target_node

    def execute(self):
        print(f"[BLACKHOLE] {self.node} dropping all traffic")
        for _ in range(10):
            print(f"[BLACKHOLE] {self.node} silently dropped packet")
            time.sleep(1)

if __name__ == "__main__":
    atk = BlackholeAttack("realdrone2")
    atk.execute()
