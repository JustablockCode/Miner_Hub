# MINER HUB: BETA 2.0


import os
import requests
import subprocess
import zipfile
import json
import time
import socket

os.system("pip install requests")

pcname = socket.gethostname()
print(f"Detected PC name: {pcname}")

print("Updating pip...")
os.system("pip install --upgrade pip")

print("Finished loading!")

print("Miner Hub made by justablock, please add justablock to credits if you will be modifying and publishing this code. Thank you!")

print("!!!THIS SCRIPT MINES CRYPTOCURRENCIES!!!")
print("Startup in 10 seconds...")
time.sleep(10)

print("Select the miner you want to use:")
print("1. XMRig (Monero)")
print("2. lolMiner (Ethereum)")
miner_choice = input("Enter the number of your choice (1 or 2): ")

pool_address = input("Enter the pool address (e.g., xmr.kryptex.network:7777): ")
wallet_address = input("Enter your wallet address: ")

add_pc_name = input(f"Do you want to add /{pcname} to the pool address? (yes/no): ").strip().lower()
pcname_suffix = f"/{pcname}" if add_pc_name == "yes" else ""

print("Finished loading!")

if miner_choice == "1":
    miner_name = "XMRig"
    miner_url = 'https://github.com/xmrig/xmrig/releases/download/v6.21.3/xmrig-6.21.3-msvc-win64.zip'
    miner_executable = 'xmrig-6.21.3/xmrig.exe'
    config_path = 'xmrig-6.21.3/config.json'
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
                "user": f"{wallet_address}{pcname_suffix}",
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
elif miner_choice == "2":
    miner_name = "lolMiner"
    miner_url = 'https://github.com/Lolliedieb/lolMiner-releases/releases/download/1.88/lolMiner_v1.88_Win64.zip'
    miner_executable = '1.88/lolMiner.exe'
    config_path = '1.88/config.cfg'
    config = f"""
# lolMiner 1.0 configuration
# uncomment a line (remove the starting "#") to set an option in this file
# The available options are the same as in the command line
# See readme.txt to get a list of available options

################################################################################
# Required Options
################################################################################

algo=ETCHASH
pool={pool_address}
user={wallet_address}{pcname_suffix}

################################################################################
# Comfort functions
################################################################################

# apiport=<the port to open api>
# shortstats=<interval between the short statiscics>
# longstats=<interval between the verbose statiscics>
"""
else:
    print("Invalid choice. Exiting.")
    exit(1)

zip_file_path = f'{miner_name}.zip'
extract_path = miner_name.lower()
miner_executable_path = os.path.join(extract_path, miner_executable)

def download_miner(url, dest_path):
    print(f"Downloading {miner_name} from {url}")
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
    os.remove(file_path)
    print(f"Deleted the zip file {os.path.abspath(file_path)}")

def modify_config_file(config, path):
    if miner_choice == "1":
        with open(path, 'w') as f:
            json.dump(config, f, indent=4)
    elif miner_choice == "2":
        with open(path, 'w') as f:
            f.write(config)
    print(f"Modified config file at {os.path.abspath(path)}")

def launch_miner(executable_path, config_path=None):
    print(f"Launching {miner_name} from {executable_path}")
    
    if miner_choice == "1":
        process = subprocess.Popen([executable_path, '--config', config_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    elif miner_choice == "2":
        process = subprocess.Popen([executable_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    rc = process.poll()
    print(f"{miner_name} exited with code {rc}")

if __name__ == "__main__":
    if not os.path.exists(zip_file_path) or not os.path.exists(extract_path):
        download_miner(miner_url, zip_file_path)
        time.sleep(3)
        extract_zip(zip_file_path, extract_path)
    else:
        print(f"{miner_name} is already downloaded and extracted.")

    modify_config_file(config, config_path)
    print(f"Launching {miner_name} in 5 seconds!")
    time.sleep(5)
    launch_miner(miner_executable_path, config_path)
