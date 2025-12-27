import sys
import os
import requests
import time
import json

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

API_URL = "http://localhost:8000/api/v1/logs"

def simulate():
    print("🚀 Starting Attack Simulation...")
    
    scenarios = [
        {"type": "normal", "count": 2},
        {"type": "bruteforce", "count": 1},
        {"type": "normal", "count": 1},
        {"type": "ransomware", "count": 1}
    ]
    
    for scen in scenarios:
        for _ in range(scen["count"]):
            # 1. Generate Log (Client side simulation for now, or calling generator via API if exposed)
            # We'll use the internal generator logic by manually creating dicts here 
            # OR better, let's call the generator service if we implement an endpoint or just import it.
            # Importing here to keep it self-contained script
            
            payload = {}
            if scen["type"] == "ransomware":
                 payload = {
                    "event": "File Modification",
                    "hostname": "Finance-PC-01",
                    "file": "budget.xlsx.enc",
                    "entropy": 7.9,
                    "process": "unknown.exe"
                }
            elif scen["type"] == "bruteforce":
                payload = {
                    "event": "Failed Login",
                    "hostname": "Gateway-01",
                    "file": "auth.log",
                    "entropy": 3.0,
                    "reason": "Bad Password",
                    "count": 50
                }
            else:
                 payload = {
                    "event": "User Login",
                    "hostname": "Workstation-02",
                    "file": "auth.log",
                    "entropy": 2.1,
                    "status": "Success"
                }

            print(f"Sending {scen['type']} log...")
            try:
                resp = requests.post(f"{API_URL}/ingest", json=payload)
                data = resp.json()
                print(f"✅ Alert ID: {data.get('alert_id')} | Severity: {data['analysis'].get('severity')}")
            except Exception as e:
                print(f"❌ Failed: {e}")
            
            time.sleep(1)

if __name__ == "__main__":
    simulate()
