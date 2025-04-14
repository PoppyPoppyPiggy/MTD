# modules/categorization.py

class ThreatCategorization:
    def __init__(self):
        self.strategies = {
            "Jamming Threat": self.handle_jamming,
            "Man-in-the-Middle Threat": self.handle_mitm,
            "DDoS Threat": self.handle_ddos,
            "Blackhole Routing Pollution Threat": self.handle_blackhole,
            "Wormhole Routing Pollution Threat": self.handle_wormhole,
        }

    def get_response_strategy(self, threat_type):
        handler = self.strategies.get(threat_type, self.default_strategy)
        return handler()

    def handle_jamming(self):
        return {
            "move_target": "IP + Port + Frequency Hopping",
            "response": "Switch to backup frequency or virtual channel",
            "use_honeypot": False
        }

    def handle_mitm(self):
        return {
            "move_target": "IP + ARP Cache",
            "response": "Inject decoy MAC, rotate ARP mapping",
            "use_honeypot": True
        }

    def handle_ddos(self):
        return {
            "move_target": "Public-facing IP + NAT",
            "response": "Redirect flood to honeypot, throttle rate",
            "use_honeypot": True
        }

    def handle_blackhole(self):
        return {
            "move_target": "Route Path",
            "response": "Bypass suspicious node, reroute",
            "use_honeypot": True
        }

    def handle_wormhole(self):
        return {
            "move_target": "Tunnel Link + Delay Pattern",
            "response": "Break tunneling loop, shuffle via latency",
            "use_honeypot": True
        }

    def default_strategy(self):
        return {
            "move_target": "IP",
            "response": "Generic shuffle",
            "use_honeypot": False
        }