# strategies/mtd.py
import random

class MTDStrategy:
    def __init__(self, ip_pool_size):
        # 사용할 IP 풀 (예: 가상 IP 주소 리스트 생성)
        self.ip_pool = [f"10.0.0.{i+1}" for i in range(ip_pool_size)]
        # 초기 실제 자산 IP 할당
        self.current_ip = self.ip_pool[0]
        self.last_shuffle_tick = 0
        # IP 사용 이력 (다양성 계산 용도)
        self.ip_usage_history = {ip: 0 for ip in self.ip_pool}
        self.ip_usage_history[self.current_ip] += 1

    def shuffle_ips(self, current_tick):
        """
        실제 자산의 IP를 풀 내 다른 IP로 변경.
        """
        old_ip = self.current_ip
        # 새로운 IP를 무작위 선택 (현재 IP와 다른 것으로)
        choices = [ip for ip in self.ip_pool if ip != old_ip]
        if choices:
            new_ip = random.choice(choices)
        else:
            new_ip = old_ip
        self.current_ip = new_ip
        self.last_shuffle_tick = current_tick
        # 사용 이력 갱신
        self.ip_usage_history[new_ip] += 1
