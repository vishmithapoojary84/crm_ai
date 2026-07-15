from langgraph.prebuilt import ToolNode

from app.langgraph.llm import llm
from app.langgraph.tools import log_interaction

tools = [
    log_interaction
]

llm_with_tools = llm.bind_tools(tools)

tool_node = ToolNode(tools)