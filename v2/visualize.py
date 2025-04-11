import matplotlib.pyplot as plt
import re
from datetime import datetime

LOG_FILE = "mtd_log.txt"

def parse_evaluator_logs(filename):
    timestamps = []
    diversity_values = []
    redundancy_values = []
    efficiency_values = []
    energy_values = []

    # 로그 패턴: [시간] [Evaluator] Diversity: x, Redundancy: y, Shuffle Efficiency: z, Energy: w
    pattern = re.compile(
        r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] \[Evaluator\] Diversity: ([\d.]+), Redundancy: ([\d.]+), Shuffle Efficiency: ([\d.]+), Energy: (\d+)"
    )

    with open(filename, "r") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                timestamp_str = match.group(1)
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                diversity = float(match.group(2))
                redundancy = float(match.group(3))
                efficiency = float(match.group(4))
                energy = int(match.group(5))

                timestamps.append(timestamp)
                diversity_values.append(diversity)
                redundancy_values.append(redundancy)
                efficiency_values.append(efficiency)
                energy_values.append(energy)

    return timestamps, diversity_values, redundancy_values, efficiency_values, energy_values

def plot_metrics(timestamps, diversity, redundancy, efficiency, energy):
    plt.figure(figsize=(12, 10))

    # Diversity
    plt.subplot(2, 2, 1)
    plt.plot(timestamps, diversity, marker='o', color='blue')
    plt.title("Diversity Over Time")
    plt.xlabel("Time")
    plt.ylabel("Diversity")
    plt.xticks(rotation=45)

    # Redundancy
    plt.subplot(2, 2, 2)
    plt.plot(timestamps, redundancy, marker='s', color='orange')
    plt.title("Redundancy Over Time")
    plt.xlabel("Time")
    plt.ylabel("Redundancy")
    plt.xticks(rotation=45)

    # Shuffle Efficiency
    plt.subplot(2, 2, 3)
    plt.plot(timestamps, efficiency, marker='^', color='green')
    plt.title("Shuffle Efficiency Over Time")
    plt.xlabel("Time")
    plt.ylabel("Efficiency")
    plt.xticks(rotation=45)

    # Energy Consumption
    plt.subplot(2, 2, 4)
    plt.plot(timestamps, energy, marker='d', color='red')
    plt.title("Energy Usage Over Time")
    plt.xlabel("Time")
    plt.ylabel("Energy")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    ts, div, red, eff, eng = parse_evaluator_logs(LOG_FILE)
    if ts:
        plot_metrics(ts, div, red, eff, eng)
    else:
        print("No valid [Evaluator] logs found in the log file.")
