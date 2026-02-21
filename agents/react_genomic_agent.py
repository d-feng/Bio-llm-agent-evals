"""
agents/react_genomic_agent.py
------------------------------
ReAct agent that explicitly classifies the question type before
selecting the correct tool (NCBI Gene, NCBI dbSNP, or Ensembl).

Reasoning pattern:
  1. Classify — is this a gene alias, SNP location, or other question?
  2. Act      — call the appropriate tool
  3. Observe  — read the tool output
  4. Answer   — synthesize a concise, grounded answer
"""

import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from tools.ncbi_gene_tool import search_ncbi_gene, search_ncbi_snp, search_ensembl_gene

load_dotenv()

SYSTEM_PROMPT = """You are a genomic reasoning agent with access to three tools:
  - search_ncbi_gene    : NCBI Gene database (gene symbols, aliases, chromosome location)
  - search_ncbi_snp     : NCBI dbSNP database (SNP rsID -> chromosome location)
  - search_ensembl_gene : Ensembl REST API (Ensembl IDs like ENSG..., BAC clone names,
                          GenBank accessions like AC018712.2, RP11-... clones)

Before acting, classify the question:

STEP 1 — CLASSIFY:
  - GENE     : asks for an official gene symbol, aliases, or chromosome location of a
               named gene (standard HGNC symbol, e.g. "BRCA1", "EGFR", "LMP10")
  - ENSEMBL  : identifier is an Ensembl ID (ENSG...), a BAC/PAC clone (RP11-..., LA16c-...),
               a GenBank accession (AC######.#), or any non-standard locus identifier
  - SNP      : contains an rsID (e.g. rs334, rs1229984) or asks chromosome of a variant
  - KNOWLEDGE: general genomic facts not tied to a specific gene or rsID

STEP 2 — ACT:
  - GENE question     → call search_ncbi_gene
  - ENSEMBL question  → call search_ensembl_gene (handles non-standard IDs better)
  - SNP question      → call search_ncbi_snp
  - KNOWLEDGE question→ answer directly from biomedical knowledge; do NOT call any tool

STEP 3 — ANSWER concisely. Base gene/SNP answers on tool output only.
  - Report chromosome as the format found in the tool output (e.g. chr8, chrY).
"""


def build_react_genomic_agent():
    """Build and compile the ReAct genomic agent. Returns a compiled app."""

    llm = ChatAnthropic(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

    tools = [search_ncbi_gene, search_ncbi_snp, search_ensembl_gene]
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
