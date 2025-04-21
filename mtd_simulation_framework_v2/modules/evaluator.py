# modules/evaluator.py
import csv
from datetime import datetime

class Evaluator:
    def __init__(self):
        self.records = []

    def log_event(self, timestamp, drone_id, diversity, redundancy, shuffle_efficiency, energy, lure_rate, deception_time):
        self.records.append({
            "timestamp": timestamp,
            "drone_id": drone_id,
            "diversity": diversity,
            "redundancy": redundancy,
            "shuffle_efficiency": shuffle_efficiency,
            "energy": energy,
            "lure_rate": lure_rate,
            "deception_time": deception_time
        })

    def save_to_csv(self, path="results.csv"):
        with open(path, 'w', newline='') as csvfile:
            fieldnames = ["timestamp", "drone_id", "diversity", "redundancy", "shuffle_efficiency", "energy", "lure_rate", "deception_time"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.records:
                writer.writerow(row)
        print(f"[EVALUATOR] Results saved to {path}")

    def compute_metrics(self):
        # 향후 통계 분석용 평균, 분산 등 추가 가능
        print(f"[EVALUATOR] 총 평가 이벤트 수: {len(self.records)}")

# 테스트 실행 예시
if __name__ == "__main__":
    ev = Evaluator()
    ev.log_event(
        timestamp=datetime.now().isoformat(),
        drone_id="honeydrone1",
        diversity=0.8,
        redundancy=0.6,
        shuffle_efficiency=0.75,
        energy=12,
        lure_rate=0.5,
        deception_time=30
    )
    ev.save_to_csv()
    ev.compute_metrics()