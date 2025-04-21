# simulation.py
from modules.defender import MTDDefender
from modules.attacker import Attacker
from modules.evaluator import Evaluator
from topo.topology_builder import TopologyBuilder
from datetime import datetime
import random
import time

# 초기 구성
topo = TopologyBuilder("topo/topology_json/default.json")
defender = MTDDefender()
attacker = Attacker()
evaluator = Evaluator()

drone_ids = ["realdrone1", "realdrone2", "honeydrone1", "honeydrone2"]

# 시뮬레이션 루프
for step in range(5):
    print(f"\n===== SIMULATION STEP {step + 1} =====")
    target = random.choice(drone_ids)
    attacker.trigger_attack(target)

    # 위협 대응 시뮬레이션
    if target.startswith("honey"):
        defender.defend_mitm()
        defender.defend_ddos()
    else:
        defender.defend_blackhole()

    # 평가 기록
    evaluator.log_event(
        timestamp=datetime.now().isoformat(),
        drone_id=target,
        diversity=random.uniform(0.7, 1.0),
        redundancy=random.uniform(0.5, 1.0),
        shuffle_efficiency=random.uniform(0.6, 1.0),
        energy=random.randint(5, 20),
        lure_rate=random.uniform(0.3, 0.9),
        deception_time=random.randint(10, 60)
    )
    time.sleep(2)

# 평가 저장
evaluator.save_to_csv()
evaluator.compute_metrics()