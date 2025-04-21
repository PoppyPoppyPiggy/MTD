# modules/attacker.py
import time

class Attacker:
    def __init__(self):
        self.state = "Idle"
        self.history = []

    def trigger_attack(self, target, attack_type):
        print(f"[ATTACK] State: {self.state}, Target: {target}, Attack: {attack_type}")

        # 상태 기반 공격 트리거
        state_transition = {
            "Idle": self._scan_if_needed,
            "ScanningDetected": self._login_if_needed,
            "Engaged": self._persistent_if_needed,
            "TrapLocked": self._shuffle_if_needed,
            "DecopyShffuling": self._escalate_if_needed,
            "EscalatedDefense": self._reset
        }

        if self.state in state_transition:
            state_transition[self.state](target, attack_type)
        else:
            print("[ATTACK] Unknown state.")

    def _scan_if_needed(self, target, attack_type):
        if attack_type in ["mitm", "ddos", "wormhole"]:
            self._log_action("ScanningDetected", f"Port scan triggered on {target} using {attack_type}")

    def _login_if_needed(self, target, attack_type):
        if attack_type in ["mitm", "blackhole"]:
            self._log_action("Engaged", f"Brute-force login attempt on {target} via {attack_type}")

    def _persistent_if_needed(self, target, attack_type):
        if attack_type in ["mitm", "blackhole", "wormhole"]:
            self._log_action("TrapLocked", f"Persistent session established with {target} during {attack_type} attack")

    def _shuffle_if_needed(self, target, attack_type):
        if attack_type in ["ddos", "wormhole", "sybil"]:
            self._log_action("DecopyShffuling", f"Activating high-frequency shuffle due to {attack_type} on {target}")

    def _escalate_if_needed(self, target, attack_type):
        if attack_type in ["ddos", "mitm", "replay"]:
            self._log_action("EscalatedDefense", f"Defensive escalation triggered by repeat {attack_type} on {target}")

    def _reset(self, target, attack_type):
        self._log_action("Idle", f"Resetting state after {attack_type} attack cycle on {target}")

    def _log_action(self, next_state, message):
        print(f"[TRANSITION] {self.state} → {next_state}: {message}")
        self.history.append(f"{self.state} → {next_state}: {message}")
        self.state = next_state
        time.sleep(1)

    def get_history(self):
        return self.history

if __name__ == "__main__":
    attacker = Attacker()
    attack_pattern = ["mitm", "mitm", "blackhole", "ddos", "replay", "mitm"]
    for atk in attack_pattern:
        attacker.trigger_attack("172.20.0.10", atk)
        time.sleep(1)
