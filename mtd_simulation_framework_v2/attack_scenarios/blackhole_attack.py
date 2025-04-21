# attack_scenarios/blackhole_attack.py
import random
import time

# 시뮬레이션 용도: 블랙홀 노드가 트래픽을 받아 먹고 드롭
class BlackholeAttack:
    def __init__(self, victim_node):
        self.victim = victim_node
        self.active = True

    def execute(self):
        print(f"[BLACKHOLE] Node {self.victim} is absorbing all packets and dropping them.")
        for _ in range(5):
            print(f"[BLACKHOLE] Dropping packet at {self.victim}")
            time.sleep(random.uniform(0.5, 1.0))

if __name__ == "__main__":
    atk = BlackholeAttack("realdrone2")
    atk.execute()