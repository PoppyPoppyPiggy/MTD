import matplotlib.pyplot as plt
import re
from datetime import datetime
from collections import defaultdict, Counter

LOG_FILE = "mtd_log.txt"
OUTPUT_FILE = "detection_summary.png"

def parse_logs(filename):
    timestamps = []
    ip_counter = Counter()
    port_counter = Counter()
    honeypot_counter = 0
    heatmap_data = defaultdict(lambda: defaultdict(int))

    detection_pattern = re.compile(r"\[(.*?)\] \[Detection\] Attack Detected - IP: (\d+\.\d+\.\d+\.\d+), Port: (\d+)")
    honeypot_pattern = re.compile(r"\[(.*?)\] \[Honeypot Detection\] IP: (\d+\.\d+\.\d+\.\d+), Port: (\d+)")

    with open(filename, "r") as f:
        for line in f:
            det_match = detection_pattern.search(line)
            honeypot_match = honeypot_pattern.search(line)

            if det_match:
                ts_str, ip, port = det_match.groups()
                ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                timestamps.append(ts)
                ip_counter[ip] += 1
                port_counter[int(port)] += 1
                heatmap_data[ip][int(port)] += 1

            elif honeypot_match:
                honeypot_counter += 1

    return timestamps, ip_counter, port_counter, heatmap_data, honeypot_counter

def plot_stats(timestamps, ip_counter, port_counter, heatmap_data, honeypot_count):
    plt.figure(figsize=(16, 10))

    # 1. 시간별 탐지 수
    hourly_count = Counter([ts.replace(minute=0, second=0) for ts in timestamps])
    plt.subplot(2, 2, 1)
    plt.bar(hourly_count.keys(), hourly_count.values(), width=0.03)
    plt.title("Detections Over Time")
    plt.xlabel("Time")
    plt.ylabel("Detections")
    plt.xticks(rotation=45)

    # 2. IP별 탐지 수
    plt.subplot(2, 2, 2)
    plt.bar(ip_counter.keys(), ip_counter.values())
    plt.title("Detected IPs")
    plt.xlabel("IP")
    plt.ylabel("Count")
    plt.xticks(rotation=90)

    # 3. 포트별 탐지 수
    plt.subplot(2, 2, 3)
    plt.bar(port_counter.keys(), port_counter.values())
    plt.title("Detected Ports")
    plt.xlabel("Port")
    plt.ylabel("Count")

    # 4. Heatmap
    plt.subplot(2, 2, 4)
    ips = list(heatmap_data.keys())
    ports = sorted(set(p for ip in heatmap_data for p in heatmap_data[ip]))
    matrix = [[heatmap_data[ip].get(port, 0) for port in ports] for ip in ips]

    plt.imshow(matrix, cmap="YlOrRd", aspect="auto")
    plt.colorbar(label="Detections")
    plt.xticks(ticks=range(len(ports)), labels=ports, rotation=90)
    plt.yticks(ticks=range(len(ips)), labels=ips)
    plt.title("Detection Heatmap (IP vs Port)")

    plt.suptitle(f"Total Honeypot Detections: {honeypot_count}", fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE)
    print(f"✅ 시각화 저장 완료: {OUTPUT_FILE}")

if __name__ == "__main__":
    ts, ip_cnt, port_cnt, heatmap, honeypot_hits = parse_logs(LOG_FILE)
    if ts:
        plot_stats(ts, ip_cnt, port_cnt, heatmap, honeypot_hits)
    else:
        print("📭 분석할 탐지 로그가 없습니다.")
