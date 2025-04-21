# visualize.py
import pandas as pd
import matplotlib.pyplot as plt

# CSV 로드
df = pd.read_csv("results.csv")

# 시각화 함수들
def plot_metric(metric):
    plt.figure(figsize=(8, 4))
    plt.plot(df['timestamp'], df[metric], marker='o')
    plt.title(f"{metric} over Time")
    plt.xlabel("Timestamp")
    plt.ylabel(metric)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    for m in ["diversity", "redundancy", "shuffle_efficiency", "energy", "lure_rate", "deception_time"]:
        plot_metric(m)