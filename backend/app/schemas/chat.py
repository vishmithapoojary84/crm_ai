from pydantic import BaseModel
from typing import Optional, Dict, Any

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    extracted_data: Optional[Dict[str, Any]] = None