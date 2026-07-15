import sys
import logging
from app.langgraph.graph import graph
from langchain_core.messages import SystemMessage, HumanMessage
from app.prompts.system_prompt import SYSTEM_PROMPT

logging.basicConfig(level=logging.INFO)

print("Starting test...")
result = graph.invoke(
    {
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content="Met Dr. Smith yesterday, discussed Prodo-X efficacy, positive response, shared brochure.")
        ]
    }
)

print("\n--- MESSAGES ---")
for msg in result["messages"]:
    print(type(msg).__name__)
    if hasattr(msg, "tool_calls"):
        print("  TOOL CALLS:", msg.tool_calls)
    print("  CONTENT:", msg.content)
