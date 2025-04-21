# strategies/decoy.py
from strategies.honeypot import HoneypotStrategy
import random

class DecoyStrategy(HoneypotStrategy):
    def __init__(self, ip_pool_size, decoy_count):
        super().__init__(ip_pool_size)
        # 디코이 노드들의 IP 목록 생성 (풀 밖의 IP들로 가정)
        self.decoy_ips = set()
        base_octet = 200  # 10.0.0.200번대 사용 예시
        for i in range(decoy_count):
            self.decoy_ips.add(f"10.0.0.{base_octet+i+1}")
        # 디코이들은 고정 IP로 존재 (허니팟과 달리 변경 없음)

    def shuffle_ips(self, current_tick):
        # HoneypotStrategy의 shuffle_ips 수행 (실제 IP 변경 + 허니팟 이전 IP 인계)
        old_ip = self.current_ip
        super().shuffle_ips(current_tick)
        # 디코이 전략에서는 특별한 추가 셔플 동작은 없음
        # (고급 구현: old_ip를 일부 디코이와도 교체하여 더욱 혼란 야기 가능)
        # 여기서는 허니팟으로 old_ip 이동만 수행 (상속된 동작)
