import matplotlib.pyplot as plt
import re
from datetime import datetime

def parse_log(file_path):
    timestamps, diversity, redundancy, shuffle = [], [], [], []

    with open(file_path, 'r') as f:
        for line in f:
            match = re.search(
                r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - INFO - MTD Evaluation: "
                r"Diversity=([\d.]+), Redundancy=([\d.]+), Shuffle=([\d.]+)",
                line
            )
            if match:
                timestamp = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S,%f")
                timestamps.append(timestamp)
                diversity.append(float(match.group(2)))
                redundancy.append(float(match.group(3)))
                shuffle.append(float(match.group(4)))

    return timestamps, diversity, redundancy, shuffle


def plot_metrics(timestamps, diversity, redundancy, shuffle):
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, diversity, label='Diversity', color='tab:blue')
    plt.plot(timestamps, redundancy, label='Redundancy', color='tab:red')
    plt.plot(timestamps, shuffle, label='Shuffle', color='tab:green')

    plt.xlabel("Timestamp")
    plt.ylabel("Metric Value")
    plt.title("MTD Evaluation Metrics Over Time")
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    log_file = "mtd_log.txt"
    ts, div, red, shf = parse_log(log_file)
    plot_metrics(ts, div, red, shf)
