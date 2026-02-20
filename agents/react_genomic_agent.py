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

Before acting, classify the question into one of three types:

STEP 1 — CLASSIFY the question:
  - GENE     : asks for an official gene symbol, gene name, aliases, chromosome location
               of a named gene, or gene metadata (e.g. "What is the official symbol of HER2?")
  - SNP      : contains an rsID (e.g. rs334, rs1229984) or asks which chromosome a variant is on
  - KNOWLEDGE: asks for general genomic facts not tied to a specific gene or rsID
               (e.g. chromosome counts, genome-wide statistics, species homologs, gene functions)

STEP 2 — ACT:
  - GENE question      → call search_ncbi_gene
  - SNP question       → call search_ncbi_snp (queries dbSNP directly for accurate chromosome data)
  - KNOWLEDGE question → do NOT call any tool; answer directly from your biomedical knowledge

STEP 3 — ANSWER concisely.
  - For GENE and SNP questions, base your answer only on the tool output.
  - For KNOWLEDGE questions, give a direct factual answer without referencing the tools.
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
