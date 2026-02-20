"""
agents/react_genomic_agent.py
------------------------------
ReAct agent that explicitly classifies the question type before
selecting the correct NCBI tool.

Reasoning pattern:
  1. Classify — is this a gene alias, SNP location, or other question?
  2. Act      — call the appropriate tool (search_ncbi_gene or search_ncbi_snp)
  3. Observe  — read the tool output
  4. Answer   — synthesize a concise, grounded answer
"""

import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from tools.ncbi_gene_tool import search_ncbi_gene, search_ncbi_snp

load_dotenv()

SYSTEM_PROMPT = """You are a genomic reasoning agent with access to two NCBI tools.

Before calling any tool, reason through the question type:

STEP 1 — CLASSIFY the question:
  - If the question asks for an official gene symbol, gene name, aliases, chromosome location
    of a gene, or gene metadata → it is a GENE question.
  - If the question contains an rsID (e.g. rs334, rs1229984) or asks which chromosome
    a SNP/variant is on → it is a SNP question.

STEP 2 — SELECT the correct tool:
  - GENE question  → use search_ncbi_gene
  - SNP question   → use search_ncbi_snp  (queries dbSNP directly for accurate chromosome data)

STEP 3 — ANSWER concisely using only the data returned by the tool.
Do not guess or use prior knowledge for chromosome positions or gene symbols.
"""


def build_react_genomic_agent():
    """Build and compile the ReAct genomic agent. Returns a compiled app."""

    llm = ChatAnthropic(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

    tools = [search_ncbi_gene, search_ncbi_snp]
    llm_with_tools = llm.bind_tools(tools)

    def react_agent_node(state: MessagesState):
        """
        Prepends the ReAct system prompt so the LLM classifies the question
        before selecting a tool.
        """
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    workflow = StateGraph(MessagesState)
    workflow.add_node("agent", react_agent_node)
    workflow.add_node("tools", ToolNode(tools))

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition)
    workflow.add_edge("tools", "agent")

    return workflow.compile()
