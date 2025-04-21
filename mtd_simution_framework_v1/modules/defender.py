# modules/defender.py
from strategies.mtd import MTDStrategy
from strategies.honeypot import HoneypotStrategy
from strategies.decoy import DecoyStrategy
from config import STRATEGY, IP_POOL_SIZE, DECOY_COUNT, SHUFFLE_INTERVAL

class Defender:
    def __init__(self):
        # 선택된 전략에 따라 적절한 전략 객체 생성
        if STRATEGY == "MTD":
            self.strategy = MTDStrategy(IP_POOL_SIZE)
        elif STRATEGY == "MTD_HONEYPOT":
            self.strategy = HoneypotStrategy(IP_POOL_SIZE)
        elif STRATEGY == "MTD_HONEYPOT_DECOY":
            self.strategy = DecoyStrategy(IP_POOL_SIZE, DECOY_COUNT)
        else:
            raise ValueError("Unknown strategy")
        self.tick_count = 0  # 현재 시뮬레이션 시간 (tick)

    def get_state(self):
        """
        공격자가 인식할 수 있는 현재 방어자 상태를 반환.
        실제로 공격자가 알 수 있는 것은 IP 수준 정보만이라고 가정.
        """
        state = {}
        state["real_ip"] = self.strategy.current_ip
        # 허니팟/디코이 존재 시 IP 정보 노출
        if hasattr(self.strategy, "honeypot_ip"):
            state["honeypot_ip"] = self.strategy.honeypot_ip
        if hasattr(self.strategy, "decoy_ips"):
            state["decoy_ips"] = list(self.strategy.decoy_ips)
        state["last_shuffle"] = self.strategy.last_shuffle_tick
        return state

    def update(self):
        """
        한 tick 진행 (공격자 공격 후 호출됨). 필요시 셔플 등 방어 조치 수행.
        """
        self.tick_count += 1
        # MTD 셔플 주기에 도달하면 IP 셔플 실행
        if self.tick_count % SHUFFLE_INTERVAL == 0:
            self.strategy.shuffle_ips(current_tick=self.tick_count)
