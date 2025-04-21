# strategies/mtd.py
import random
import time

class IPPool:
    def __init__(self):
        self.pool = [f"10.0.0.{i}" for i in range(2, 255)]
        random.shuffle(self.pool)

    def shuffle(self):
        random.shuffle(self.pool)
        print("[MTD] IP pool shuffled")

    def get_ip(self):
        ip = self.pool.pop() if self.pool else "10.0.0.1"
        print(f"[MTD] IP assigned: {ip}")
        return ip

class PortShuffler:
    def __init__(self):
        self.ports = list(range(2000, 3000))

    def shuffle_ports(self):
        random.shuffle(self.ports)
        ports = self.ports[:3]
        print(f"[MTD] Ports shuffled: {ports}")
        return ports

class RSSIShuffler:
    def shuffle_rssi(self):
        level = random.choice(["Low", "Medium", "High"])
        print(f"[MTD] RSSI level adjusted to: {level}")
        return level

# 테스트
if __name__ == "__main__":
    ipm = IPPool()
    psh = PortShuffler()
    rss = RSSIShuffler()
    ipm.shuffle()
    ipm.get_ip()
    psh.shuffle_ports()
    rss.shuffle_rssi()
