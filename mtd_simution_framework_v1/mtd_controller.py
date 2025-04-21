# mtd_controller.py
from modules.attacker import Attacker
from modules.defender import Defender

def run_simulation_once():
    # 방어자 & 공격자 초기화
    defender = Defender()
    attacker = Attacker()

    # 시뮬레이션 루프
    total_steps = 0
    honeypot_hits = 0
    decoy_hits = 0
    real_hits = 0
    num_shuffles = 0

    for t in range(1, SIMULATION_STEPS+1):
        # 공격자 행동
        outcome = attacker.attack(defender)
        total_steps += 1
        # 공격 결과에 따른 통계 집계
        if outcome == "honeypot":
            honeypot_hits += 1
        elif outcome == "decoy":
            decoy_hits += 1
        elif outcome == "real":
            real_hits += 1
        else:  # outcome == "fail"
            # fail도 공격 저지로 간주 (디코이나 허니팟 아닌 경우)
            pass

        # 방어자 상태 업데이트 (셔플 등)
        defender.update()
        # 셔플이 일어났으면 방어자 객체에 last_shuffle_tick이 갱신됨
        if defender.strategy.last_shuffle_tick == t:
            num_shuffles += 1
            # 셔플 직후에는 공격자의 current_info를 False로 설정하여 다음 공격에 반영
            attacker.current_info = False

    # 시뮬레이션 종료: 수집된 데이터 반환
    # 다양성 계산을 위해 defender.strategy.ip_usage_history 활용
    diversity = calc_diversity(defender.strategy.ip_usage_history)
    redundancy = calc_redundancy(
        num_real=1,
        num_honeypot=(1 if hasattr(defender.strategy, "honeypot_ip") else 0),
        num_decoy=(len(defender.strategy.decoy_ips) if hasattr(defender.strategy, "decoy_ips") else 0)
    )
    attacks_foiled = honeypot_hits + decoy_hits
    # MTD 단독의 fail도 foiled에 포함
    # (허니팟/디코이 없는 경우 fail 발생 시 decoy_hits로 집계되지 않으므로 별도 처리)
    if real_hits + honeypot_hits + decoy_hits < total_steps:
        attacks_foiled += (total_steps - (real_hits + honeypot_hits + decoy_hits))
    shuffle_eff = calc_shuffle_efficiency(attacks_foiled, num_shuffles)
    energy = calc_energy(num_shuffles,
                         num_honeypot=(1 if hasattr(defender.strategy, "honeypot_ip") else 0),
                         num_decoy=(len(defender.strategy.decoy_ips) if hasattr(defender.strategy, "decoy_ips") else 0),
                         steps=total_steps)
    lure_rate = calc_honeypot_lure(honeypot_hits, total_steps)

    return {
        "diversity": diversity,
        "redundancy": redundancy,
        "shuffle_efficiency": shuffle_eff,
        "energy": energy,
        "honeypot_lure_rate": lure_rate
    }
