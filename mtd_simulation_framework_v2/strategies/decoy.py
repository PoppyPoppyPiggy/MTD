# strategies/decoy.py
import random

class DecoyManager:
    def __init__(self):
        self.active_decoys = {}

    def create_fake_log(self, drone_id):
        logs = [
            f"{drone_id}: login failed for root",
            f"{drone_id}: invalid password attempt from 192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            f"{drone_id}: sudo access denied"
        ]
        log = random.choice(logs)
        print(f"[DECOY] Log injected: {log}")
        return log

    def deploy_fake_banner(self, service):
        banners = {
            "ssh": "OpenSSH_8.2p1 Ubuntu-4ubuntu0.3",
            "http": "Apache/2.4.41 (Ubuntu)",
            "ftp": "vsFTPd 3.0.3"
        }
        banner = banners.get(service.lower(), "Unknown Service")
        print(f"[DECOY] Fake banner for {service}: {banner}")
        return banner

    def generate_hint(self):
        hints = ["Password hint: birth_year + pet_name", "Try 'admin123'", "Last changed: 2022"]
        hint = random.choice(hints)
        print(f"[DECOY] Password hint given: {hint}")
        return hint

# 테스트 실행
if __name__ == "__main__":
    d = DecoyManager()
    d.create_fake_log("honeydrone1")
    d.deploy_fake_banner("SSH")
    d.generate_hint()