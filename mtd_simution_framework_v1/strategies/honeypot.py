# strategies/honeypot.py
from strategies.mtd import MTDStrategy

class HoneypotStrategy(MTDStrategy):
    def __init__(self, ip_pool_size):
        super().__init__(ip_pool_size)
        # 허니팟 노드 IP (고정 또는 초기에는 None)
        # 여기서는 풀 밖의 고정 IP 하나를 사용한다고 가정
        self.honeypot_ip = "10.0.0.250"
        # 허니팟이 초기에는 실행되나, 공격자에게 실체를 드러내기 위해 IP 존재
        # (더 정교한 구현에서는 허니팟을 초기에는 숨겨두고 첫 셔플 때 등장시킬 수도 있음)

    def shuffle_ips(self, current_tick):
        # 현재 IP 변경 (기존 MTD 동작)
        old_ip = self.current_ip
        super().shuffle_ips(current_tick)
        new_ip = self.current_ip
        # 허니팟 전략: 이전 실제 IP를 허니팟이 인계받음
        # (즉, 허니팟IP와 이전 IP를 스왑하는 형태로 구현)
        if old_ip and self.honeypot_ip:
            # 허니팟이 사용하던 IP와 old_ip를 교체
            # (단순 시뮬레이션이므로 실제 IP 스왑이 아니라, honeypot_ip 변수를 old_ip로 설정)
            self.honeypot_ip = old_ip
        # 사용 이력 갱신 (MTDStrategy에서 new_ip 추가는 이미 수행됨)
        # 허니팟 IP는 다양성 계산에서는 제외 (실제 자산이 아니므로)
