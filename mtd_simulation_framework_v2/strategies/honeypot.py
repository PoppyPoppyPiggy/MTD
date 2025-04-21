# strategies/honeypot.py
import subprocess
import os

def deploy_honeydrone(container_name, ip_address, ports=[22, 80]):
    port_flags = ' '.join([f"-p {p}:{p}" for p in ports])
    command = f"docker run -d --name {container_name} --network drone_net --ip {ip_address} \
        {port_flags} -e DECOY=true honeydrone_image"
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"[HONEYPOT] Deployed honeydrone: {container_name} at {ip_address}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to deploy {container_name}: {str(e)}")

def remove_honeydrone(container_name):
    try:
        subprocess.run(f"docker stop {container_name}", shell=True, check=True)
        subprocess.run(f"docker rm {container_name}", shell=True, check=True)
        print(f"[HONEYPOT] Removed {container_name}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Could not remove {container_name}: {str(e)}")

def list_honeydrones():
    result = subprocess.run("docker ps --filter \"ancestor=honeydrone_image\" --format '{{.Names}}'", 
                            shell=True, stdout=subprocess.PIPE, text=True)
    names = result.stdout.strip().split('\n')
    return [n for n in names if n]

# 예시 실행 (테스트용)
if __name__ == "__main__":
    deploy_honeydrone("honeydrone1", "172.20.0.10")
    print("Active honeydrones:", list_honeydrones())
    remove_honeydrone("honeydrone1")
