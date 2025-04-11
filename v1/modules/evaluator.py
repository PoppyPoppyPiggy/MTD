import logging
logger = logging.getLogger("MTD")

class MTDEvaluator:
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender
        self.last_defender_map = dict(defender.defender_map)
        self.last_reverse_map = dict(defender.reverse_map) if hasattr(defender, 'reverse_map') else {}

    def evaluate(self):
        # 1. Diversity: 공격자가 관측한 유니크한 IP 수 / 전체 IP 풀 수
        observed_ips = set(self.attacker.attacker_history)
        total_possible = len(self.defender.ip_pool) or 1
        diversity = len(observed_ips) / total_possible

        # 2. Redundancy: 하나의 서비스에 여러 IP가 매핑되어 있는 비율
        service_to_ips = {}
        for ip, service in self.defender.reverse_map.items():  # reverse_map[ip] = service_id
            service_to_ips.setdefault(service, set()).add(ip)
        redundancy = sum(len(ips) > 1 for ips in service_to_ips.values()) / len(service_to_ips) if service_to_ips else 0

        # 3. Shuffle: 이전 상태 대비 IP 변경된 비율
        changed = 0
        total = len(self.defender.defender_map)
        for device_id, new_ip in self.defender.defender_map.items():
            old_ip = self.last_defender_map.get(device_id)
            if old_ip != new_ip:
                changed += 1
        shuffle_rate = changed / total if total > 0 else 0

        # 4. Efficiency 계산 (단순 평균)
        efficiency = (diversity + redundancy + shuffle_rate) / 3

        # 상태 업데이트
        self.last_defender_map = dict(self.defender.defender_map)
        self.last_reverse_map = dict(self.defender.reverse_map)

        # 로그 출력
        logger.info(
            f"MTD Evaluation: Diversity={diversity:.2f}, Redundancy={redundancy:.2f}, Shuffle={shuffle_rate:.2f}, Efficiency={efficiency:.2f}"
        )