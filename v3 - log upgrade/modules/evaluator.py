# modules/evaluator.py
from datetime import datetime

class Evaluator:
    def __init__(self, defender):
        self.defender = defender
        self.log_file = "mtd_log.txt"

    def evaluate(self):
        diversity = self._calculate_diversity()
        redundancy = self._calculate_redundancy()
        efficiency = self._calculate_efficiency()
        energy = self.defender.energy_consumed

        # Qualitative 평가 기준 (간단 표시)
        qualitative_security = "Stable" if diversity > 0.7 else "Unstable"
        qualitative_performance = "Efficient" if energy < 50 else "Overused"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as log:
            log.write(
                f"[{timestamp}] [Evaluator] Diversity: {diversity:.2f}, Redundancy: {redundancy:.2f}, "
                f"Shuffle Efficiency: {efficiency:.2f}, Energy: {energy} | "
                f"[Security: {qualitative_security}, Performance: {qualitative_performance}]\n"
            )

    def _calculate_diversity(self):
        unique_ips = len(set(self.defender.defender_map.values()))
        return unique_ips / self.defender.ip_pool_size

    def _calculate_redundancy(self):
        values = list(self.defender.defender_map.values())
        redundancy = 1 - (len(set(values)) / len(values))
        return redundancy

    def _calculate_efficiency(self):
        if self.defender.energy_consumed == 0:
            return 1.0
        return 1 - self._calculate_redundancy()
