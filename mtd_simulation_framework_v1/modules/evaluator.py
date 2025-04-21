# modules/evaluator.py
import math

def calc_diversity(ip_history):
    """
    ip_history: 딕셔너리 {ip: 사용횟수, ...}
    Shannon 다양성 지수 계산
    """
    total = sum(ip_history.values())
    if total == 0:
        return 0.0
    H = 0.0
    for ip, count in ip_history.items():
        p = count / total
        if p > 0:
            H -= p * math.log(p)
    return H

def calc_redundancy(num_real, num_honeypot, num_decoy):
    # 중복도 = (허니팟 수 + 디코이 수) / 실제 자산 수
    if num_real == 0:
        return 0.0
    return (num_honeypot + num_decoy) / num_real

def calc_shuffle_efficiency(attacks_foiled, num_shuffles):
    # 셔플 효율 = 공격 저지 횟수 / 셔플 횟수
    if num_shuffles == 0:
        return 0.0
    return attacks_foiled / num_shuffles

def calc_energy(num_shuffles, num_honeypot, num_decoy, steps,
                cost_shuffle=1.0, cost_honeypot=1.0, cost_decoy=1.0):
    # Energy = 셔플 비용*횟수 + 허니팟 비용*시간 + 디코이 비용*시간
    return cost_shuffle*num_shuffles + cost_honeypot*num_honeypot*steps + cost_decoy*num_decoy*steps

def calc_honeypot_lure(honeypot_hits, total_attacks):
    if total_attacks == 0:
        return 0.0
    return honeypot_hits / total_attacks

def summarize_results(results_list):
    """
    여러 번 실행한 결과 리스트를 받아 각 지표의 평균과 분산 계산.
    results_list: [{ "diversity": x, "redundancy": y, ...}, {...}, ... ]
    """
    if not results_list:
        return {}
    # 지표별 평균 계산
    avg = {}
    for metric in results_list[0].keys():
        avg[metric] = sum(run[metric] for run in results_list) / len(results_list)
    # 지표별 분산 계산
    var = {}
    for metric in results_list[0].keys():
        var[metric] = sum((run[metric] - avg[metric])**2 for run in results_list) / len(results_list)
    # 평균과 분산 결과 합치기
    summary = {}
    for metric in avg.keys():
        summary[f"{metric}_mean"] = avg[metric]
        summary[f"{metric}_var"] = var[metric]
    return summary
