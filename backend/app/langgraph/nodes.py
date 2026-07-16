from langgraph.prebuilt import ToolNode

from app.langgraph.llm import llm
from app.langgraph.tools import (
    log_interaction,
    search_hcp,
    get_interaction_history,
    edit_interaction,
    follow_up_recommendation
)

tools = [
    log_interaction,
    search_hcp,
    get_interaction_history,
    edit_interaction,
    follow_up_recommendation
]

llm_with_tools = llm.bind_tools(tools)

tool_node = ToolNode(tools)