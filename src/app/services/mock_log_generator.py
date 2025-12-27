import random
import time
import json
from datetime import datetime

class MockLogGenerator:
    """
    Generates simulated security logs for demonstration purposes.
    Simulates: Failed Logins, brute force, malware entropy, etc.
    """
    
    SOURCES = ["Workstation-01", "Workstation-02", "Server-DB-01", "Firewall-Main"]
    USERS = ["admin", "guest", "jdoe", "service_account"]
    
    @staticmethod
    def generate_log(threat_type="normal"):
        base_log = {
            "timestamp": datetime.utcnow().isoformat(),
            "hostname": random.choice(MockLogGenerator.SOURCES),
            "user": random.choice(MockLogGenerator.USERS),
        }
        
        if threat_type == "ransomware":
            base_log.update({
                "event": "File Modification",
                "file": "C:\\Users\\Data\\important.docx.enc",
                "entropy": round(random.uniform(7.5, 8.0), 2),
                "process": "unknown_crypto.exe",
                "action": "write"
            })
        elif threat_type == "bruteforce":
            base_log.update({
                "event": "Failed Login",
                "source_ip": f"192.168.1.{random.randint(100, 200)}",
                "reason": "Bad Password",
                "count": random.randint(5, 50)
            })
        elif threat_type == "pfsense_block":
            base_log.update({
                "event": "Firewall Deny",
                "source_ip": f"45.33.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "destination_port": 22,
                "protocol": "TCP"
            })
        else: # Normal
            base_log.update({
                "event": "User Login",
                "source_ip": "10.0.0.5",
                "action": "success"
            })
            
        return base_log

mock_generator = MockLogGenerator()
