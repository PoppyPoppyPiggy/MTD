import random
import logging
from collections import defaultdict

logger = logging.getLogger("MTD")

class Defender:
    def __init__(self, ip_pool_size=32, shuffle_interval=5):
        self.default_pool_size = ip_pool_size
        self.shuffle_interval = shuffle_interval
        self.energy_cost = 0
        self.datapath_map = defaultdict(str)
        self.device_ip_map = {}
        self.ip_pool = self._generate_ip_pool(ip_pool_size)
        self.current_index = 0
        self.ip_access_count = defaultdict(int)

    def _generate_ip_pool(self, size):
        return [f"10.0.0.{i+1}" for i in range(size)]

    def register_datapath(self, datapath_id):
        if datapath_id not in self.datapath_map:
            ip = self._assign_ip()
            self.datapath_map[datapath_id] = ip
            self.device_ip_map[datapath_id] = ip
            logger.info(f"[Defender] Registered DPID {datapath_id} with IP {ip}")

    def _assign_ip(self):
        ip = self.ip_pool[self.current_index % len(self.ip_pool)]
        self.current_index += 1
        return ip

    def record_access(self, ip):
        self.ip_access_count[ip] += 1
        logger.debug(f"[Defender] Access recorded for IP {ip}. Access count: {self.ip_access_count[ip]}")

        if self.ip_access_count[ip] > 10:
            logger.warning(f"[Defender] Suspicious activity detected on IP {ip}. Triggering shuffle.")
            return True
        return False

    def shuffle_ips(self, force=False):
        if force:
            logger.info("[Defender] Forced shuffle triggered.")
        else:
            logger.info("[Defender] Periodic shuffle triggered.")

        self.energy_cost += len(self.datapath_map)
        available_ips = self.ip_pool.copy()
        random.shuffle(available_ips)

        for dpid in self.datapath_map:
            old_ip = self.datapath_map[dpid]
            new_ip = available_ips.pop()
            logger.info(f"[Defender] DPID {dpid}: {old_ip} → {new_ip}")
            self.datapath_map[dpid] = new_ip
            self.device_ip_map[dpid] = new_ip