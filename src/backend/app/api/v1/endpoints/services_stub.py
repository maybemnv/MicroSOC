def analyze_log(log_data: dict):
    # Stub for Gemini Analysis
    # Logic: if entropy > 5 -> High, Ransomware
    entropy = log_data.get("entropy", 0)
    if entropy > 5.0:
        return {
            "severity": "High",
            "explanation": "High entropy detected in file operations, indicating potential encryption/ransomware.",
            "mitre_ttp": "T1486 - Data Encrypted for Impact"
        }
    return {
        "severity": "Low",
        "explanation": "Normal operation detected.",
        "mitre_ttp": None
    }
