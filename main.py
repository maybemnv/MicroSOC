# main.py – Write this EXACTLY
from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

class Log(BaseModel):
    event: str
    hostname: str
    file: str
    entropy: float

@app.post("/ingest")
def ingest(log: Log):
    # P0: Just classify ransomware
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Analyze this log: {log.dict()}
    1. Is this ransomware? (yes/no)
    2. Confidence (0-100)
    3. Action (isolate_host/none)
    Return JSON only.
    """
    response = model.generate_content(prompt)
    # Mock response for speed:
    verdict = {"is_ransomware": True, "confidence": 95, "action": "isolate_host"}
    # In real: parse response.text
    return verdict