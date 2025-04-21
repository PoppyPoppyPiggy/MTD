#!/bin/bash

# launcher.sh

echo "[INIT] Launching MTD Drone Simulation Testbed"

# 1. Docker Compose (drone containers)
echo "[STEP 1] Starting drone fleet with Docker..."
docker-compose -f drone_fleet/docker-compose.yml up -d
sleep 5

# 2. Ryu controller (run in background)
echo "[STEP 2] Launching Ryu controller..."
ryu-manager ryu_app/ryu_app.py &
RYU_PID=$!
sleep 3

# 3. Simulation Run
echo "[STEP 3] Running simulation.py"
python3 simulation.py

# 4. Visualization
echo "[STEP 4] Visualizing results..."
python3 visualize.py

# 5. Cleanup Ryu Controller
echo "[CLEANUP] Killing Ryu controller..."
kill $RYU_PID

echo "[COMPLETE] All steps finished."
