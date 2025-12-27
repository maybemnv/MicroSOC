from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any, Dict

class LogIngest(BaseModel):
    hostname: str
    log_file: str
    log_message: str
    timestamp: Optional[datetime] = None
    context: Optional[Dict[str, Any]] = None
