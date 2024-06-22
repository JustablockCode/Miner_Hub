import os
import requests
import subprocess
import zipfile
import json
import time
import socket

# Ensure requests library is installed
os.system("pip install requests")

pcname = socket.gethostname()
print(f"Detected PC name: {pcname}")

print("XMR Installer made by justablock, please add justablock to credits if you modify and publish this code. Thank you!")
print("!!!THIS SCRIPT MINES MONERO COIN!!!")
print("Startup in 10 seconds...")
time.sleep(10)

# Prompt user for pool address and wallet address
pool_address = input("Enter the pool address (e.g., xmr.kryptex.network:7777): ")
wallet_address = input("Enter your wallet address: ")

print("Finished loading!")

# Determine if PC name should be appended based on pool address
pcname_slash = f"/{pcname}" if pool_address in ["xmr.kryptex.network:7777", "xmr.kryptex.network:8888"] else ""

# XMRig download and configuration
xmrig_url = 'https://github.com/xmrig/xmrig/releases/download/v6.21.3/xmrig-6.21.3-msvc-win64.zip'
zip_file_path = 'xmrig.zip'
extract_path = 'xmrig'
xmrig_executable_path = os.path.join(extract_path, 'xmrig-6.21.3', 'xmrig.exe')
config_path = os.path.join(extract_path, 'xmrig-6.21.3', 'config.json')

# Configuration settings for XMRig
config = {
    "autosave": True,
    "background": False,
    "cpu": {
        "enabled": True,
        "huge-pages": True,
        "hw-aes": None,
        "priority": None,
        "max-threads-hint": 100,
        "asm": True
    },
    "opencl": {
        "enabled": False,
        "platform": "AMD"
    },
    "cuda": {
        "enabled": False,
        "loader": None
    },
    "donate-level": 1,
    "log-file": None,
    "pools": [
        {
            "algo": "rx/0",
            "coin": "XMR",
            "url": pool_address,
            "user": f"{wallet_address}{pcname_slash}",
            "pass": "x",
            "tls": False,
            "keepalive": True,
            "nicehash": False
        }
    ],
    "print-time": 60,
    "retries": 5,
    "retry-pause": 5,
    "syslog": False,
    "watch": True
}

def download_xmrig(url, dest_path):
    print("Downloading XMRig 6.21.3 for Windows...")
    print(f"Downloading XMRig from {url}")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded to {os.path.abspath(dest_path)}")

def extract_zip(file_path, extract_to):
    print(f"Extracting {file_path} to {extract_to}")
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted to {os.path.abspath(extract_to)}")

def modify_config_file(config, path):
    with open(path, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Modified config file at {os.path.abspath(path)}")

def launch_xmrig(executable_path, config_path):
    print(f"Launching XMRig from {executable_path}")
    
    process = subprocess.Popen([executable_path, '--config', config_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    rc = process.poll()
    print(f"XMRig exited with code {rc}")

if __name__ == "__main__":
    if not os.path.exists(zip_file_path) or not os.path.exists(extract_path):
        download_xmrig(xmrig_url, zip_file_path)
        time.sleep(3)
        extract_zip(zip_file_path, extract_path)
    else:
        print("XMRig is already downloaded and extracted.")

    modify_config_file(config, config_path)
    print("Launching miner in 5 seconds!")
    time.sleep(5)
    launch_xmrig(xmrig_executable_path, config_path)