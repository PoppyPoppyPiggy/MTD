#visualize.py
import matplotlib.pyplot as plt
import re
from datetime import datetime

# 로그에서 필요한 정보 파싱
def parse_log(file_path):
    timestamps, diversity, redundancy, shuffle_cost, energy = [], [], [], [], []
    with open(file_path, "r") as f:
        for line in f:
            if "[EVAL]" in line:
                ts_match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", line)
                if ts_match:
                    timestamps.append(datetime.strptime(ts_match.group(1), "%Y-%m-%d %H:%M:%S"))
                diversity.append(float(re.search(r"Diversity=([\d.]+)", line).group(1)))
                redundancy.append(float(re.search(r"Redundancy=([\d.]+)", line).group(1)))
                shuffle_cost.append(float(re.search(r"Shuffle=([\d.]+)", line).group(1)))
                energy.append(float(re.search(r"Energy=([\d.]+)", line).group(1)))
    return timestamps, diversity, redundancy, shuffle_cost, energy

# 시각화 함수
def visualize_metrics(file_path):
    ts, div, red, shf, eng = parse_log(file_path)

    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.plot(ts, div, label="Diversity", color="green")
    plt.ylabel("Diversity")
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(ts, red, label="Redundancy", color="orange")
    plt.ylabel("Redundancy")
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.plot(ts, shf, label="Shuffle Index", color="blue")
    plt.ylabel("Shuffle Index")
    plt.xlabel("Time")
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(ts, eng, label="Energy", color="red")
    plt.ylabel("Energy")
    plt.xlabel("Time")
    plt.grid(True)

    plt.tight_layout()
    plt.suptitle("MTD Performance Metrics Over Time", fontsize=16, y=1.02)
    plt.show()

if __name__ == "__main__":
    visualize_metrics("mtd_log.txt")
