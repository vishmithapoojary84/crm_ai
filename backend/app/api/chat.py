from fastapi import APIRouter
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from app.langgraph.graph import graph
from app.prompts.system_prompt import SYSTEM_PROMPT
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.logger import logger

router = APIRouter(tags=["AI Chat"])


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = graph.invoke(
        {
            "messages": [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=request.message),
            ]
        }
    )

    logger.info("--- NEW CHAT TRACE ---")
    extracted_data = None
    for msg in result["messages"]:
        if isinstance(msg, HumanMessage):
            logger.info(f"USER: {msg.content}")
        elif isinstance(msg, AIMessage):
            if msg.content:
                logger.info(f"AI: {msg.content}")
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    logger.info(f"AI TOOL CALL: {tc['name']} with args {tc['args']}")
                    if tc["name"] in ["log_interaction", "edit_interaction", "submit_interaction"]:
                        # Extract non-empty fields
                        extracted_data = {k: v for k, v in tc["args"].items() if v not in [None, ""]}
                    elif tc["name"] == "reset_form":
                        extracted_data = {
                            "hcp_name": "",
                            "date": "",
                            "sentiment": "",
                            "product_discussed": "",
                            "brochures_shared": False
                        }
                        
        elif isinstance(msg, ToolMessage):
            logger.info(f"TOOL RESPONSE ({msg.name}): {msg.content}")

    ai_message = result["messages"][-1]

    return ChatResponse(
        response=ai_message.content,
        extracted_data=extracted_data
    )