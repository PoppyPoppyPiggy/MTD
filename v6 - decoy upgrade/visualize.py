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
    decoy_counter = 0
    heatmap_data = defaultdict(lambda: defaultdict(int))

    detection_pattern = re.compile(r"\[(.*?)\] \[Detection\] Attack Detected - IP: (\d+\.\d+\.\d+\.\d+), Port: (\d+)")
    honeypot_pattern = re.compile(r"\[(.*?)\] \[Honeypot Detection\] IP: (\d+\.\d+\.\d+\.\d+), Port: (\d+)")
    decoy_pattern = re.compile(r"\[(.*?)\] \[Decoy Illusion\] IP: (\d+\.\d+\.\d+\.\d+), Illusion Count: (\d+)")

    with open(filename, "r") as f:
        for line in f:
            det_match = detection_pattern.search(line)
            honeypot_match = honeypot_pattern.search(line)
            decoy_match = decoy_pattern.search(line)

            if det_match:
                ts_str, ip, port = det_match.groups()
                ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                timestamps.append(ts)
                ip_counter[ip] += 1
                port_counter[int(port)] += 1
                heatmap_data[ip][int(port)] += 1

            elif honeypot_match:
                honeypot_counter += 1

            elif decoy_match:
                illusion_count = int(decoy_match.group(3))
                decoy_counter += illusion_count

    return timestamps, ip_counter, port_counter, heatmap_data, honeypot_counter, decoy_counter

def plot_stats(timestamps, ip_counter, port_counter, heatmap_data, honeypot_count, decoy_count):
    plt.figure(figsize=(18, 12))

    plt.subplot(3, 2, 1)
    hourly_count = Counter([ts.replace(minute=0, second=0) for ts in timestamps])
    plt.bar(hourly_count.keys(), hourly_count.values(), width=0.03)
    plt.title("1. Detections Over Time")
    plt.xlabel("Time")
    plt.ylabel("Detections")
    plt.xticks(rotation=45)

    plt.subplot(3, 2, 2)
    plt.bar(ip_counter.keys(), ip_counter.values())
    plt.title("2. Detected IPs")
    plt.xlabel("IP")
    plt.ylabel("Count")
    plt.xticks(rotation=90)

    plt.subplot(3, 2, 3)
    plt.bar(port_counter.keys(), port_counter.values())
    plt.title("3. Detected Ports")
    plt.xlabel("Port")
    plt.ylabel("Count")

    plt.subplot(3, 2, 4)
    ips = list(heatmap_data.keys())
    ports = sorted(set(p for ip in heatmap_data for p in heatmap_data[ip]))
    matrix = [[heatmap_data[ip].get(port, 0) for port in ports] for ip in ips]
    plt.imshow(matrix, cmap="YlOrRd", aspect="auto")
    plt.colorbar(label="Detections")
    plt.xticks(ticks=range(len(ports)), labels=ports, rotation=90)
    plt.yticks(ticks=range(len(ips)), labels=ips)
    plt.title("4. Detection Heatmap (IP vs Port)")

    plt.subplot(3, 2, 5)
    plt.bar(["Honeypot Detection"], [honeypot_count])
    plt.title("5. Honeypot Detection Count")
    plt.ylabel("Count")

    plt.subplot(3, 2, 6)
    plt.bar(["Decoy Illusion"], [decoy_count])
    plt.title("6. Decoy Illusion Count")
    plt.ylabel("Count")

    plt.suptitle("MTD + Honeypot + Decoy Detection Summary", fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(OUTPUT_FILE)
    print(f"✅ 시각화 저장 완료: {OUTPUT_FILE}")

if __name__ == "__main__":
    ts, ip_cnt, port_cnt, heatmap, honeypot_hits, decoy_hits = parse_logs(LOG_FILE)
    if ts:
        plot_stats(ts, ip_cnt, port_cnt, heatmap, honeypot_hits, decoy_hits)
    else:
        print("📭 분석할 탐지 로그가 없습니다.")
