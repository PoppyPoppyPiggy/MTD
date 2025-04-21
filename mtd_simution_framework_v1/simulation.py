# simulation.py
import csv
from config import STRATEGY, NUM_RUNS, STRATEGY
from mtd_controller import run_simulation_once
from modules.evaluator import summarize_results

# 비교할 전략 목록 (전략 이름 문자열과 설정값 매핑)
strategies_to_test = ["MTD", "MTD_HONEYPOT", "MTD_HONEYPOT_DECOY"]

# CSV 결과 파일 준비
with open("results.csv", mode="w", newline='') as csvfile:
    fieldnames = ["strategy", "diversity_mean", "diversity_var",
                  "redundancy_mean", "redundancy_var",
                  "shuffle_efficiency_mean", "shuffle_efficiency_var",
                  "energy_mean", "energy_var",
                  "honeypot_lure_rate_mean", "honeypot_lure_rate_var"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for strat in strategies_to_test:
        # 설정한 전략으로 시뮬레이션 실행 NUM_RUNS회
        STRATEGY = strat  # 현재 전략 설정 (config 전역 변수 변경)
        results_list = []
        for i in range(NUM_RUNS):
            result = run_simulation_once()
            results_list.append(result)
        summary = summarize_results(results_list)
        summary["strategy"] = strat
        writer.writerow(summary)
        print(f"{strat} done. Avg Results: {summary}")
