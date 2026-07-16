from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition

from app.langgraph.state import CRMState
from app.langgraph.nodes import llm_with_tools, tool_node


import time

def chatbot(state: CRMState):
    time.sleep(2.5) # Artificial throttle to prevent Groq free-tier 429 errors
    return {
        "messages": [
            llm_with_tools.invoke(state["messages"])
        ]
    }


builder = StateGraph(CRMState)

builder.add_node("chatbot", chatbot)

builder.add_node("tools", tool_node)

builder.add_edge(START, "chatbot")

builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

builder.add_edge("tools", "chatbot")

graph = builder.compile()