import google.genai as genai
from google.genai import types
import json
from app.core.config import settings

# Initialize Gemini Client
# Assumes GOOGLE_API_KEY is set in .env
client = genai.Client(api_key=settings.GOOGLE_API_KEY)

def analyze_log_with_gemini(log_data: dict) -> dict:
    """
    Sends log data to Gemini 1.5 Flash for security analysis.
    Returns a standardized JSON dict with severity, explanation, and MITRE TTP.
    """
    
    prompt = f"""
    You are an autonomous Tier 1 Security Analyst (MicroSOC).
    Analyze the following security log JSON and provide a threat assessment.
    
    Log Data:
    {json.dumps(log_data, indent=2)}
    
    Instructions:
    1. Determine if this log represents a security threat.
    2. Assign a Severity: "Low", "Medium", or "High".
    3. Map to a specific MITRE ATT&CK Tactic/Technique (e.g., "T1059 - Command and Scripting Interpreter") if applicable, else null.
    4. Provide a SHORT, plain English explanation (1-2 sentences) suitable for a non-technical manager.
    5. Evaluate "Confidence" (0-100).
    
    Format your response as pure JSON with this schema:
    {{
        "is_threat": boolean,
        "severity": "Low" | "Medium" | "High",
        "mitre_ttp": "string" | null,
        "explanation": "string",
        "confidence": number
    }}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type='application/json'
            )
        )
        
        result = response.parsed
        if not result:
             # Fallback if parsing fails or returns empty
             return _fallback_result("Empty response from AI")
             
        # The SDK might return a dict or object depending on config. 
        # Since response_mime_type='application/json' usually returns a text that needs parsing 
        # or an object if using specific Pydantic integration. 
        # Let's assume standard text behavior with automation or direct generic object access if 'parsed' is available,
        # but safely reload from text if needed for simple dictionary access.
        
        # Adjusting based on standard google-genai behavior for 'application/json':
        # It's safest to load the text.
        return json.loads(response.text)

    except Exception as e:
        print(f"Gemini Analysis Failed: {e}")
        return _fallback_result(str(e))

def _fallback_result(error_msg: str) -> dict:
    return {
        "is_threat": False,
        "severity": "Low",
        "mitre_ttp": None,
        "explanation": f"Analysis failed; log ingested raw. Error: {error_msg}",
        "confidence": 0
    }
