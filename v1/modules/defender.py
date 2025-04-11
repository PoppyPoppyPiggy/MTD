import random
import logging
logger = logging.getLogger("MTD")

class Defender:
    def __init__(self):
        self.defender_map = {}
        self.reverse_map = {}  # ip -> service_id
        self.ip_pool = list(range(32))
        self.services = {}  # device_id -> service_id

    def register_device(self, device_id, service_id):
        self.services[device_id] = service_id

    def shuffle_ips(self, datapaths):
        changed_count = 0
        self.reverse_map.clear()
        for device_id in datapaths:
            new_ip = random.choice(self.ip_pool)
            if self.defender_map.get(device_id) != new_ip:
                self.defender_map[device_id] = new_ip
                changed_count += 1
            service_id = self.services.get(device_id, f"svc-{device_id}")
            self.reverse_map[new_ip] = service_id
            logger.info(f"[DEFENSE] Device-{device_id} (Service-{service_id}) changes IP to: {new_ip}")
        logger.info(f"[SHUFFLE] Total IP changes: {changed_count}")
