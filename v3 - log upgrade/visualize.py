# visualize.py
import matplotlib.pyplot as plt
import re
from datetime import datetime
from collections import Counter, defaultdict
import os

MLOG_FILE = "mtd_log.txt"
OUTPUT_FILE = "detection_summary.png"


def parse_detections(filename):
    timestamps = []
    ip_ports = []
    port_list = []
    ip_counter = Counter()
    port_counter = Counter()
    heatmap_data = defaultdict(lambda: defaultdict(int))

    pattern = re.compile(
        r"\[(.*?)\] \[Detection\] Attack Detected - IP: (\d+\.\d+\.\d+\.\d+), Port: (\d+)"
    )

    with open(filename, "r") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                timestamp = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
                ip = match.group(2)
                port = int(match.group(3))

                timestamps.append(timestamp)
                ip_ports.append((ip, port))
                port_list.append(port)

                ip_counter[ip] += 1
                port_counter[port] += 1
                heatmap_data[ip][port] += 1

    return timestamps, ip_ports, port_list, ip_counter, port_counter, heatmap_data


def plot_detection_stats(timestamps, ip_counter, port_counter, heatmap_data):
    plt.figure(figsize=(16, 10))

    # 1. 시간별 탐지 카운트
    hourly_count = Counter([ts.replace(minute=0, second=0) for ts in timestamps])
    plt.subplot(2, 2, 1)
    plt.bar(hourly_count.keys(), hourly_count.values(), width=0.03)
    plt.title("Detections Over Time")
    plt.xlabel("Time")
    plt.ylabel("Detections")
    plt.xticks(rotation=45)

    # 2. 포트별 탐지 카운트
    plt.subplot(2, 2, 2)
    plt.bar(port_counter.keys(), port_counter.values())
    plt.title("Detected Ports Frequency")
    plt.xlabel("Port")
    plt.ylabel("Detections")

    # 3. IP별 탐지 카운트
    plt.subplot(2, 2, 3)
    plt.bar(ip_counter.keys(), ip_counter.values())
    plt.title("Detected IP Frequency")
    plt.xlabel("IP")
    plt.ylabel("Detections")
    plt.xticks(rotation=45)

    # 4. 히트맵: IP vs Port 탐지 횟수
    plt.subplot(2, 2, 4)
    ips = list(heatmap_data.keys())
    ports = sorted(set(port for pmap in heatmap_data.values() for port in pmap))
    matrix = [
        [heatmap_data[ip].get(port, 0) for port in ports]
        for ip in ips
    ]

    plt.imshow(matrix, cmap='YlOrRd', aspect='auto')
    plt.colorbar(label='Detections')
    plt.xticks(ticks=range(len(ports)), labels=ports, rotation=90)
    plt.yticks(ticks=range(len(ips)), labels=ips)
    plt.title("Detection Heatmap (IP vs Port)")

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE)
    print(f"✅ 그래프 저장 완료: {OUTPUT_FILE}")


if __name__ == "__main__":
    ts, ip_ports, ports, ip_counter, port_counter, heatmap_data = parse_detections(MLOG_FILE)
    if ts:
        plot_detection_stats(ts, ip_counter, port_counter, heatmap_data)
    else:
        print("No detection logs found.")