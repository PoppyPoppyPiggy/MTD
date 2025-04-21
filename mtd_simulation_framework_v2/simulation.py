# simulation.py
from modules.defender import MTDDefender
from modules.attacker import Attacker
from modules.evaluator import Evaluator
from topo.topology_builder import TopologyBuilder
from datetime import datetime
import random
import time

# 구성 초기화
topo = TopologyBuilder("topo/topology_json/default.json")
defender = MTDDefender(mode='mtd+honeypot+decoy')
attacker = Attacker()
evaluator = Evaluator()

drone_ids = ["realdrone1", "realdrone2", "realdrone3", "honeydrone1", "honeydrone2"]
attack_types = ["mitm", "ddos", "wormhole", "blackhole", "replay"]

# 시뮬레이션 반복
total_steps = 15
for step in range(total_steps):
    print(f"\n===== SIMULATION STEP {step + 1}/{total_steps} =====")
    target = random.choice(drone_ids)
    attack_type = random.choice(attack_types)

    attacker.trigger_attack(target, attack_type)
    metrics = defender.respond_to(attack_type, target)

    evaluator.log_event(
        timestamp=datetime.now().isoformat(),
        drone_id=target,
        **metrics
    )
    time.sleep(1)

# 결과 저장 및 요약 출력
evaluator.save_to_csv()
evaluator.compute_metrics()