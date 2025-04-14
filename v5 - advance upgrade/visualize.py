import matplotlib.pyplot as plt
import re
from datetime import datetime
from collections import defaultdict, Counter

LOG_FILE = "mtd_log.txt"
OUTPUT_FILE = "detection_summary_extended.png"

def parse_logs(filename):
    timestamps = []
    ip_counter = Counter()
    port_counter = Counter()
    honeypot_counter = 0
    heatmap_data = defaultdict(lambda: defaultdict(int))
    honeypot_ips = set()
    honeypot_detect_ts = []
    normal_detect_ts = []

    eval_timestamps = []
    diversity_vals = []
    redundancy_vals = []
    efficiency_vals = []
    energy_vals = []

    detection_pattern = re.compile(r"\[(.*?)\] \[Detection\] Attack Detected - IP: (\d+\.\d+\.\d+\.\d+), Port: (\d+)")
    honeypot_pattern = re.compile(r"\[(.*?)\] \[Honeypot Detection\] IP: (\d+\.\d+\.\d+\.\d+), Port: (\d+)")
    eval_pattern = re.compile(r"\[(.*?)\] \[Evaluator\] Diversity: ([\d.]+), Redundancy: ([\d.]+), Shuffle Efficiency: ([\d.]+), Energy: (\d+)")

    with open(filename, "r") as f:
        for line in f:
            honeypot_match = honeypot_pattern.search(line)
            if honeypot_match:
                ts_str, ip, port = honeypot_match.groups()
                ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                honeypot_counter += 1
                honeypot_ips.add(ip)
                honeypot_detect_ts.append(ts)
                continue

            det_match = detection_pattern.search(line)
            if det_match:
                ts_str, ip, port = det_match.groups()
                ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                timestamps.append(ts)
                ip_counter[ip] += 1
                port_counter[int(port)] += 1
                heatmap_data[ip][int(port)] += 1

                if ip in honeypot_ips:
                    honeypot_detect_ts.append(ts)
                else:
                    normal_detect_ts.append(ts)

            eval_match = eval_pattern.search(line)
            if eval_match:
                ts_str, div, red, eff, eng = eval_match.groups()
                ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                eval_timestamps.append(ts)
                diversity_vals.append(float(div))
                redundancy_vals.append(float(red))
                efficiency_vals.append(float(eff))
                energy_vals.append(int(eng))

    return (timestamps, ip_counter, port_counter, heatmap_data,
            honeypot_counter, honeypot_detect_ts, normal_detect_ts,
            eval_timestamps, diversity_vals, redundancy_vals, efficiency_vals, energy_vals)

def plot_stats(timestamps, ip_counter, port_counter, heatmap_data, honeypot_count,
               honeypot_ts, normal_ts, eval_ts, div_vals, red_vals, eff_vals, eng_vals):
    total_detections = len(timestamps)
    honeypot_rate = (honeypot_count / total_detections) * 100 if total_detections else 0.0

    plt.figure(figsize=(20, 20))
    plt.subplots_adjust(top=0.92)

    # 1. 시간별 탐지 수
    hourly_count = Counter([ts.replace(minute=0, second=0) for ts in timestamps])
    plt.subplot(4, 2, 1)
    plt.bar(hourly_count.keys(), hourly_count.values(), width=0.03)
    plt.title("Detections Over Time")
    plt.xlabel("Time")
    plt.ylabel("Detections")
    plt.xticks(rotation=45)

    # 2. IP별 탐지 수
    plt.subplot(4, 2, 2)
    plt.bar(ip_counter.keys(), ip_counter.values())
    plt.title("Detected IPs")
    plt.xlabel("IP")
    plt.ylabel("Count")
    plt.xticks(rotation=90)

    # 3. 포트별 탐지 수
    plt.subplot(4, 2, 3)
    plt.bar(port_counter.keys(), port_counter.values())
    plt.title("Detected Ports")
    plt.xlabel("Port")
    plt.ylabel("Count")

    # 4. Heatmap
    plt.subplot(4, 2, 4)
    ips = list(heatmap_data.keys())
    ports = sorted(set(p for ip in heatmap_data for p in heatmap_data[ip]))
    matrix = [[heatmap_data[ip].get(port, 0) for port in ports] for ip in ips]

    plt.imshow(matrix, cmap="YlOrRd", aspect="auto")
    plt.colorbar(label="Detections")
    plt.xticks(ticks=range(len(ports)), labels=ports, rotation=90)
    plt.yticks(ticks=range(len(ips)), labels=ips)
    plt.title("Detection Heatmap (IP vs Port)")

    # 5. 허니팟 vs 일반 탐지 비율
    plt.subplot(4, 2, 5)
    categories = ['Honeypot', 'Normal']
    counts = [len(honeypot_ts), len(normal_ts)]
    plt.bar(categories, counts, color=['red', 'gray'])
    plt.title("Honeypot vs Normal Detection Count")
    plt.ylabel("Count")

    # 6. 시간 흐름에 따른 누적 유인율 그래프
    plt.subplot(4, 2, 6)
    combined = sorted([(ts, 'honeypot') for ts in honeypot_ts] + [(ts, 'normal') for ts in normal_ts])
    hp_cum = 0
    norm_cum = 0
    hp_rates = []
    x_ticks = []

    for ts, typ in combined:
        if typ == 'honeypot':
            hp_cum += 1
        else:
            norm_cum += 1

        total = hp_cum + norm_cum
        hp_rate = (hp_cum / total) * 100 if total else 0
        x_ticks.append(ts)
        hp_rates.append(hp_rate)

    plt.plot(x_ticks, hp_rates, marker='o', label="Honeypot Attraction Rate (%)")
    plt.title("Cumulative Honeypot Attraction Rate Over Time")
    plt.ylabel("Attraction Rate (%)")
    plt.xlabel("Time")
    plt.xticks(rotation=45)
    plt.ylim(0, 100)
    plt.legend()

    # 7. MTD 평가 지표 그래프
    plt.subplot(4, 1, 4)
    plt.plot(eval_ts, div_vals, label='Diversity')
    plt.plot(eval_ts, red_vals, label='Redundancy')
    plt.plot(eval_ts, eff_vals, label='Efficiency')
    plt.plot(eval_ts, eng_vals, label='Energy')
    plt.xlabel("Time")
    plt.ylabel("Metric Value")
    plt.title("MTD Evaluation Metrics Over Time")
    plt.legend()
    plt.xticks(rotation=45)

    # 저장
    plt.suptitle(
        f"MTD Detection Summary | Honeypot Hits: {honeypot_count} / {total_detections} "
        f"({honeypot_rate:.2f}%)", fontsize=16
    )
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE)
    print(f"✅ 시각화 저장 완료: {OUTPUT_FILE}")

if __name__ == "__main__":
    results = parse_logs(LOG_FILE)
    if results[0]:
        plot_stats(*results)
    else:
        print("📭 분석할 탐지 로그가 없습니다.")
