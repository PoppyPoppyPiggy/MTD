from datetime import datetime
import math
from collections import Counter

class Evaluator:
    def __init__(self, defender):
        self.defender = defender
        self.log_file = "mtd_log.txt"

    def evaluate(self):
        diversity = self._calculate_entropy_diversity()
        redundancy = self._calculate_redundancy()
        efficiency = self._calculate_efficiency()
        energy = self.defender.energy_consumed

        qual_sec = "Stable" if diversity > 0.7 else "Unstable"
        qual_perf = "Efficient" if energy < 100 else "Overused"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as log:
            log.write(
                f"[{timestamp}] [Evaluator] Diversity: {diversity:.2f}, Redundancy: {redundancy:.2f}, "
                f"Shuffle Efficiency: {efficiency:.2f}, Energy: {energy} | "
                f"[Security: {qual_sec}, Performance: {qual_perf}]\n"
            )

    def _calculate_entropy_diversity(self):
        values = list(self.defender.defender_map.values())
        count = Counter(values)
        total = len(values)
        entropy = -sum((c / total) * math.log2(c / total) for c in count.values())
        max_entropy = math.log2(self.defender.ip_pool_size)
        return entropy / max_entropy if max_entropy else 0

    def _calculate_redundancy(self):
        values = list(self.defender.defender_map.values())
        return 1 - (len(set(values)) / len(values))

    def _calculate_efficiency(self):
        if self.defender.energy_consumed == 0:
            return 1.0
        return 1 - self._calculate_redundancy()
