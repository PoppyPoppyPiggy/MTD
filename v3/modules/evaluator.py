import logging

logger = logging.getLogger("MTD")

class Evaluator:
    def __init__(self, defender):
        self.defender = defender
        self.success_count = 0
        self.fail_count = 0

    def record_attack_result(self, result):
        if result:
            self.success_count += 1
        else:
            self.fail_count += 1
        logger.info(f"[Evaluator] Attack success: {self.success_count}, failure: {self.fail_count}")

    def evaluate(self):
        total_attempts = self.success_count + self.fail_count
        success_rate = (self.success_count / total_attempts) if total_attempts > 0 else 0
        fail_rate = 1 - success_rate

        evaluation = {
            "success_rate": success_rate,
            "fail_rate": fail_rate,
        }
        logger.info(f"[Evaluate] Success Rate: {success_rate:.2f}, Fail Rate: {fail_rate:.2f}")
        return evaluation