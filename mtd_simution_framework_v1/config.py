# config.py

# --- 시뮬레이션 제어 설정 ---
NUM_RUNS = 30             # 전략별 반복 실행 횟수
SIMULATION_STEPS = 100    # 한 번의 시뮬레이션당 시간단위 (tick) 수

# --- 전략 설정 ---
# STRATEGY = "MTD"
# STRATEGY = "MTD_HONEYPOT"
# STRATEGY = "MTD_HONEYPOT_DECOY"
STRATEGY = "MTD_HONEYPOT_DECOY"  # 기본 전략 (simulation.py에서 동적으로 재지정됨)

# --- MTD 전략 파라미터 ---
IP_POOL_SIZE = 10         # 사용할 가상 IP 수
SHUFFLE_INTERVAL = 5      # 몇 tick마다 셔플 수행

# --- Honeypot / Decoy 설정 ---
HONEYPOT_LURE_PROB = 0.5  # 허니팟 유인 확률
DECOY_CONFUSE_PROB = 0.2  # 디코이 혼란 유발 확률
DECOY_COUNT = 3           # 디코이 노드 수
