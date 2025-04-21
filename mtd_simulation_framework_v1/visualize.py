# visualize.py (Optional visualization - not fully implemented)
import pandas as pd
import matplotlib.pyplot as plt

# 결과 CSV 읽기
df = pd.read_csv("results.csv")
print(df.to_string(index=False))
# 시각화 생략 또는 필요시 matplotlib 등으로 그래프 생성
