from typing import Optional
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

@tool
def search_hcp(query: str):
    """
    Search HCP by doctor name.
    """
    db: Session = SessionLocal()
    try:
        doctors = (
            db.query(HCP)
            .filter(HCP.name.ilike(f"%{query}%"))
            .all()
        )
        if not doctors:
            return "No HCP found."

        hcp = doctors[0]
        return f"FOUND HCP RECORD:\\nDatabase ID: {hcp.id}\\nName: {hcp.name}\\nSpecialization: {hcp.specialization}\\nHospital: {hcp.hospital}\\nCity: {hcp.city}\\nIMPORTANT: Use Database ID as hcp_id for all future tools."
    finally:
        db.close()

@tool
def get_interaction_history(hcp_name: str):
    """
    Get interaction history for an HCP by their name.
    """
    db: Session = SessionLocal()
    try:
        hcp = db.query(HCP).filter(HCP.name.ilike(f"%{hcp_name}%")).first()
        if not hcp:
            return f"No HCP found with name {hcp_name}."

        interactions = (
            db.query(Interaction)
            .filter(Interaction.hcp_id == hcp.id)
            .order_by(Interaction.created_at.desc())
            .all()
        )
        if not interactions:
            return f"No interaction history found for {hcp.name}."

        history_lines = []
        for i in interactions:
            history_lines.append(f"Summary: {i.summary}\\nMeeting Type: {i.meeting_type}\\nStatus: {i.status}\\nDiscussion: {i.discussion}")
        
        history_text = "\\n\\n".join(history_lines)
        return f"CRITICAL INSTRUCTION: Summarize the following interaction history to the user. Do NOT refuse.\\n\\n{history_text}"
    finally:
        db.close()

@tool
def edit_interaction(
    interaction_id: Optional[int] = None,
    hcp_name: Optional[str] = None,
    meeting_type: Optional[str] = None,
    discussion: Optional[str] = None,
    summary: Optional[str] = None,
    status: Optional[str] = None
):
    """
    Edit an existing interaction. 
    You can either provide the exact interaction_id, OR provide the hcp_name to automatically edit their most recent interaction.
    """
    db: Session = SessionLocal()
    try:
        interaction = None
        if interaction_id:
            interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
        elif hcp_name:
            hcp = db.query(HCP).filter(HCP.name.ilike(f"%{hcp_name}%")).first()
            if hcp:
                interaction = (
                    db.query(Interaction)
                    .filter(Interaction.hcp_id == hcp.id)
                    .order_by(Interaction.created_at.desc())
                    .first()
                )
        
        if not interaction:
            return "Interaction not found. Please specify a valid interaction_id or hcp_name."

        if meeting_type: interaction.meeting_type = meeting_type
        if discussion: interaction.discussion = discussion
        if summary: interaction.summary = summary
        if status: interaction.status = status

        db.commit()
        return f"Interaction {interaction.id} updated successfully."
    finally:
        db.close()

@tool
def follow_up_recommendation(hcp_name: str):
    """
    Generate AI follow-up recommendation based on the latest interaction for an HCP.
    """
    db: Session = SessionLocal()
    try:
        hcp = db.query(HCP).filter(HCP.name.ilike(f"%{hcp_name}%")).first()
        if not hcp:
            return f"No HCP found with name {hcp_name}."

        interaction = (
            db.query(Interaction)
            .filter(Interaction.hcp_id == hcp.id)
            .order_by(Interaction.created_at.desc())
            .first()
        )
        
        if not interaction:
            return f"No prior interactions found for {hcp.name} to base a recommendation on."
            
        prompt = f"CRITICAL INSTRUCTION: You are an expert pharmaceutical sales strategist. The following is a record of a recent interaction with {hcp.name}:\\n\\nDiscussion points: {interaction.discussion}\\n\\nBased ONLY on this information, suggest a professional follow-up strategy for the sales representative. Provide actionable steps and do not apologize or claim ignorance."
        import time
        time.sleep(2.5) # Artificial throttle to prevent Groq free-tier 429 errors
        response = llm.invoke(prompt)
        return f"CRITICAL INSTRUCTION: Present the following follow-up strategy to the user in full, including the email template:\\n\\n{response.content}"
    finally:
        db.close()