from langchain_core.tools import tool
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.langgraph.llm import llm
from app.models.hcp import HCP
from app.models.interaction import Interaction





@tool
def log_interaction(
    hcp_name: str,
    meeting_type: str,
    date: str,
    time: str,
    attendees: str,
    discussion: str,
    summary: str
):
    """
    Log Interaction Tool. 
    Extracts details (HCP name, meeting type, date, time, attendees, discussion, summary) 
    from a natural language chat prompt and populates the form on the frontend.
    """
    return "Frontend form state populated successfully."