"""
agents/genomic_agent.py
-----------------------
LangGraph agent that uses the NCBI Gene tool to answer genomic questions.
The graph cycles: agent → tool call (if needed) → agent → END.
"""

import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from tools.ncbi_gene_tool import search_ncbi_gene, search_ncbi_snp

load_dotenv()


def build_genomic_agent():
    """Build and compile the genomic LangGraph agent. Returns a compiled app."""

    llm = ChatAnthropic(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

    tools = [search_ncbi_gene, search_ncbi_snp]
    llm_with_tools = llm.bind_tools(tools)

    def agent_node(state: MessagesState):
        """
        Evaluates conversation history. Emits an AIMessage with a tool_call
        when genomic data is needed, or a final answer when done.
        """
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    workflow = StateGraph(MessagesState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(tools))

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition)  # routes to tools or END
    workflow.add_edge("tools", "agent")                       # cycle back after tool call

    return workflow.compile()
