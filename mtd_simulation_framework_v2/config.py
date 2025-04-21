# config.py

NETWORK_SUBNET = "172.20.0.0/16"

DRONES = {
    "realdrone1": {"ip": "172.20.0.11", "role": "mission"},
    "realdrone2": {"ip": "172.20.0.12", "role": "mission"},
    "honeydrone1": {"ip": "172.20.0.10", "role": "honeypot"},
    "honeydrone2": {"ip": "172.20.0.13", "role": "honeypot"}
}

PORT_POOL = list(range(2000, 3000))

EVALUATION_METRICS = [
    "diversity",
    "redundancy",
    "shuffle_efficiency",
    "energy",
    "lure_rate",
    "deception_time"
]

DEFAULT_TOPOLOGY_PATH = "topo/topology_json/default.json"