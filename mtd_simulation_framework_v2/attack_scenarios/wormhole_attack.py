# attack_scenarios/wormhole_attack.py
import time

class WormholeAttack:
    def __init__(self, entry_node, exit_node):
        self.entry = entry_node
        self.exit = exit_node

    def execute(self):
        print(f"[WORMHOLE] Establishing tunnel between {self.entry} and {self.exit}...")
        for _ in range(5):
            print(f"[WORMHOLE] Tunneling packets: {self.entry} <--> {self.exit}")
            time.sleep(1)

if __name__ == "__main__":
    atk = WormholeAttack("realdrone1", "realdrone3")
    atk.execute()
