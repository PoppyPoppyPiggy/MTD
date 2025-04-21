# modules/defender.py
from strategies.mtd import IPPool, PortShuffler, RSSIShuffler
from strategies.honeypot import deploy_honeydrone
from strategies.decoy import DecoyManager
import math

class MTDDefender:
    def __init__(self, mode='mtd+honeypot+decoy'):
        self.mode = mode
        self.ip_pool = IPPool()
        self.port_shuffler = PortShuffler()
        self.rssi_shuffler = RSSIShuffler()
        self.decoy = DecoyManager()

        self.state = {
            'attack_types': {},
            'ip_changes': 0,
            'port_changes': 0,
            'rssi_changes': 0,
            'honeypot_used': 0,
            'decoy_activated': 0,
            'decoy_duration': 0,
            'attack_engaged': 0,
            'survived_real': 0,
            'survived_honey': 0
        }

    def respond_to(self, attack_type, target):
        print(f"[DEFENDER] Strategy: {self.mode}, Responding to: {attack_type}, Target: {target}")
        self.state['attack_engaged'] += 1
        self.state['attack_types'][attack_type] = self.state['attack_types'].get(attack_type, 0) + 1

        # MTD 전략 실행
        self.ip_pool.shuffle()
        _ = self.ip_pool.get_ip()
        self.state['ip_changes'] += 1

        _ = self.port_shuffler.shuffle_ports()
        self.state['port_changes'] += 1

        _ = self.rssi_shuffler.shuffle_rssi()
        self.state['rssi_changes'] += 1

        if 'honeypot' in self.mode:
            deploy_honeydrone(target, "172.20.0.200", [2222])
            self.state['honeypot_used'] += 1

        if 'decoy' in self.mode:
            self.decoy.create_fake_log(target)
            self.decoy.generate_hint()
            self.decoy.deploy_fake_banner("ssh")
            self.state['decoy_activated'] += 1
            self.state['decoy_duration'] += 10

        # 생존성 시뮬레이션 (확률 기반)
        if 'real' in target:
            self.state['survived_real'] += 1 if attack_type != 'ddos' else 0
        elif 'honey' in target:
            self.state['survived_honey'] += 1 if attack_type in ['mitm', 'replay', 'blackhole'] else 0

        return self.compute_metrics()

    def compute_metrics(self):
        a = self.state['attack_engaged']
        n_types = len(self.state['attack_types'])

        # Diversity: Shannon Entropy normalized
        type_dist = [v / a for v in self.state['attack_types'].values()]
        entropy = -sum([p * math.log(p + 1e-8) for p in type_dist]) / math.log(n_types + 1e-8)

        # Redundancy: inverse of concentration (Herfindahl Index)
        hhi = sum([(v / a) ** 2 for v in self.state['attack_types'].values()])
        redundancy = 1 - hhi

        # Shuffle Efficiency: 평균 변화량
        shuffle_efficiency = (self.state['ip_changes'] + self.state['port_changes'] + self.state['rssi_changes']) / (a * 3)

        # Energy: 가중합 기반 에너지 소모
        energy = (
            self.state['ip_changes'] * 1.0 +
            self.state['port_changes'] * 0.5 +
            self.state['rssi_changes'] * 0.2 +
            self.state['honeypot_used'] * 2.0 +
            self.state['decoy_activated'] * 1.5
        )

        # Survivability: 실제/허니드론의 생존 비율
        real_surv = self.state['survived_real'] / a
        honey_surv = self.state['survived_honey'] / a

        # Lure Rate: 허니드론 유도 비율
        lure_rate = self.state['honeypot_used'] / a if a else 0

        # Deception Persistence: 총 지속 시간
        deception_time = self.state['decoy_duration']

        return {
            'diversity': round(entropy, 3),
            'redundancy': round(redundancy, 3),
            'shuffle_efficiency': round(shuffle_efficiency, 3),
            'energy': round(energy, 2),
            'survivability_real': round(real_surv, 3),
            'survivability_honey': round(honey_surv, 3),
            'lure_rate': round(lure_rate, 3),
            'deception_time': deception_time
        }
