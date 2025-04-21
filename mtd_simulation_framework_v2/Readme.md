# 🛰️ HoneyDrone MTD Simulation Framework

A full-stack Moving Target Defense (MTD) simulation testbed for swarm drone security with decoy, honeypot, and deception strategies.

---

## 📦 Structure Overview

```bash
.
├── attack_scenarios/        # Threat automation (DDoS, Jamming, MitM, etc.)
├── drone_fleet/             # Dockerfiles and drone deployment configs
├── modules/                 # Attacker, Defender, Evaluator logic
├── strategies/              # MTD, Honeypot, Decoy algorithms
├── topo/                    # Topology builder + JSON config
├── ryu_app/                 # Ryu SDN controller logic
├── simulation.py            # Integrated simulation runner
├── visualize.py             # Plot metrics from evaluation
├── config.py                # Central config file for IP, ports, metrics
└── launcher.sh              # One-command runner
```

---

## 🚀 Quick Start

### 🔧 Requirements
- Python 3.8+
- Docker + Docker Compose
- Ryu SDN Framework (`pip install ryu`)
- Scapy (`pip install scapy`)

### 🧪 Run Full Simulation
```bash
bash launcher.sh
```

---

## 🎯 Features
- **Docker-based drone deployment** (real + honey drones)
- **Auto-generated threat scenarios** (MitM, Jamming, etc.)
- **Dynamic MTD response** (IP/Port/RSSI shuffle, proxy rotation)
- **Deception logic** (fake banners, password hints, log injection)
- **Metric evaluation** (Diversity, Lure Rate, Shuffle Efficiency, etc.)
- **Topology loading + visualization**

---

## 📈 Sample Metrics Tracked
- `diversity`
- `redundancy`
- `shuffle_efficiency`
- `energy`
- `lure_rate`
- `deception_time`

All stored in `results.csv` and plotted using `visualize.py`

---

## 📁 Key Entry Points
- `simulation.py`: Main orchestration logic
- `launcher.sh`: Full launch script
- `docker-compose.yml`: Drone container definitions

---

## ✍️ Author
> Built for advanced MTD simulation research in autonomous drone swarm security.
