"""
evals/geneturing_eval.py
------------------------
Evaluation loop that runs a LangGraph genomic agent against GeneTuring tasks
and scores its answers using exact-match and Jaccard Index.

GeneTuring repo: https://github.com/Winnie09/GeneTuring
Uses the official Q&A dataset (data/Q_A_dataset.csv, 1600 questions across 16
modules) when available; falls back to the built-in 25-question mock dataset.
"""

import os
import json
import re
import pandas as pd
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

# Path to the official GeneTuring CSV (downloaded from the GeneTuring repo)
_HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA_PATH = os.path.join(_HERE, "..", "data", "Q_A_dataset.csv")


# ---------------------------------------------------------------------------
# Scoring helpers
# ---------------------------------------------------------------------------

def exact_match(prediction: str, gold) -> bool:
    if gold is None or (isinstance(gold, float) and gold != gold):  # NaN check
        return False
    return str(gold).strip().lower() in str(prediction).strip().lower()


def jaccard_score(prediction: str, gold) -> float:
    """
    Jaccard Index over token sets — used for multi-gene alias questions
    where the answer may contain several gene names.
    """
    if gold is None or (isinstance(gold, float) and gold != gold):  # NaN check
        return 0.0
    pred_tokens = set(str(prediction).lower().split())
    gold_tokens = set(str(gold).lower().split())
    if not pred_tokens and not gold_tokens:
        return 1.0
    intersection = pred_tokens & gold_tokens
    union = pred_tokens | gold_tokens
    return len(intersection) / len(union)


def llm_judge(question: str, prediction: str, gold: str, judge_llm=None) -> dict:
    """
    Use an LLM as a judge to score semantic correctness when exact match fails.

    Returns a dict with:
        correct  : bool   — judge verdict
        score    : float  — 0.0 or 1.0
        reason   : str    — judge's one-line explanation
    """
    if judge_llm is None:
        from langchain_anthropic import ChatAnthropic
        judge_llm = ChatAnthropic(
            model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            max_tokens=256,
        )

    prompt = f"""You are an expert biomedical evaluator. Judge whether the agent's answer is correct.

Question      : {question}
Gold standard : {gold}
Agent answer  : {prediction}

Rules:
- Numeric answers are correct if they are within 10% of the gold standard value.
- Gene symbols are correct only if the official HGNC symbol matches exactly (case-insensitive).
- Partial or approximate answers that convey the correct fact count as correct.
- Answers that are clearly wrong or contradict the gold standard are incorrect.

Respond in this exact format:
VERDICT: CORRECT or INCORRECT
REASON: <one sentence>"""

    response = judge_llm.invoke([HumanMessage(content=prompt)])
    text = response.content.strip()

    verdict_match = re.search(r"VERDICT:\s*(CORRECT|INCORRECT)", text, re.IGNORECASE)
    reason_match  = re.search(r"REASON:\s*(.+)", text, re.IGNORECASE)

    correct = verdict_match.group(1).upper() == "CORRECT" if verdict_match else False
    reason  = reason_match.group(1).strip() if reason_match else text[:120]

    return {"correct": correct, "score": 1.0 if correct else 0.0, "reason": reason}


def score_answer(question: str, prediction: str, gold: str,
                 use_llm_judge: bool = False, judge_llm=None) -> dict:
    """
    Primary scoring function. Tries exact match first; falls back to LLM judge
    if use_llm_judge=True and exact match fails.

    Returns:
        ExactMatch     : bool
        LLMJudge       : bool or None
        LLMJudgeReason : str or None
        FinalScore     : bool  — the authoritative pass/fail used in reporting
    """
    em = exact_match(prediction, gold)
    result = {
        "ExactMatch":      em,
        "LLMJudge":        None,
        "LLMJudgeReason":  None,
        "FinalScore":      em,
    }

    if not em and use_llm_judge:
        judgement = llm_judge(question, prediction, gold, judge_llm)
        result["LLMJudge"]       = judgement["correct"]
        result["LLMJudgeReason"] = judgement["reason"]
        result["FinalScore"]     = judgement["correct"]

    return result


# ---------------------------------------------------------------------------
# Built-in mock dataset (8 GeneTuring modules)
# ---------------------------------------------------------------------------

MOCK_DATA = [
    # --- Gene alias ---
    {"module": "Gene alias",        "question": "What is the official gene symbol of HER2?",                              "gold_standard": "ERBB2"},
    {"module": "Gene alias",        "question": "What is the official gene symbol of p53?",                               "gold_standard": "TP53"},
    {"module": "Gene alias",        "question": "What is the official gene symbol of VEGF?",                              "gold_standard": "VEGFA"},
    {"module": "Gene alias",        "question": "What is the official gene symbol of PD-L1?",                             "gold_standard": "CD274"},
    {"module": "Gene alias",        "question": "What is the official gene symbol of c-MET?",                             "gold_standard": "MET"},

    # --- SNP location ---
    {"module": "SNP location",      "question": "What chromosome is rs1229984 located on?",                               "gold_standard": "Chromosome 4"},
    {"module": "SNP location",      "question": "What chromosome is rs334 located on?",                                   "gold_standard": "Chromosome 11"},
    {"module": "SNP location",      "question": "What chromosome is rs7412 located on?",                                  "gold_standard": "Chromosome 19"},
    {"module": "SNP location",      "question": "What chromosome is rs429358 located on?",                                "gold_standard": "Chromosome 19"},

    # --- Gene location ---
    {"module": "Gene location",     "question": "What chromosome is BRCA1 located on?",                                   "gold_standard": "Chromosome 17"},
    {"module": "Gene location",     "question": "What chromosome is EGFR located on?",                                    "gold_standard": "Chromosome 7"},
    {"module": "Gene location",     "question": "What chromosome is KRAS located on?",                                    "gold_standard": "Chromosome 12"},
    {"module": "Gene location",     "question": "What chromosome is PTEN located on?",                                    "gold_standard": "Chromosome 10"},

    # --- Gene disease association ---
    {"module": "Gene disease",      "question": "Which gene is most associated with cystic fibrosis?",                    "gold_standard": "CFTR"},
    {"module": "Gene disease",      "question": "Which gene is most associated with Huntington's disease?",               "gold_standard": "HTT"},
    {"module": "Gene disease",      "question": "Which gene is mutated in sickle cell disease?",                          "gold_standard": "HBB"},

    # --- Gene function ---
    {"module": "Gene function",     "question": "What is the primary function of the TP53 gene?",                         "gold_standard": "tumor suppressor"},
    {"module": "Gene function",     "question": "What type of protein does BRCA1 encode?",                                "gold_standard": "DNA repair"},
    {"module": "Gene function",     "question": "What is the function of the VEGFA gene?",                                "gold_standard": "angiogenesis"},

    # --- Chromosome gene count ---
    {"module": "Chromosome gene count", "question": "Which chromosome has the most protein-coding genes?",                "gold_standard": "Chromosome 1"},
    {"module": "Chromosome gene count", "question": "Which human chromosome is the smallest?",                            "gold_standard": "Chromosome 21"},

    # --- Human genome reference ---
    {"module": "Human genome",      "question": "How many chromosomes does a normal human cell have?",                    "gold_standard": "46"},
    {"module": "Human genome",      "question": "What is the approximate number of protein-coding genes in the human genome?", "gold_standard": "20000"},

    # --- Multi-species homolog ---
    {"module": "Multi-species",     "question": "What is the mouse homolog of the human EGFR gene?",                      "gold_standard": "Egfr"},
    {"module": "Multi-species",     "question": "What is the zebrafish homolog of the human TP53 gene?",                  "gold_standard": "tp53"},
]

AVAILABLE_MODULES = sorted(set(d["module"] for d in MOCK_DATA))  # mock fallback list; real list loaded dynamically


# ---------------------------------------------------------------------------
# Data loader
# ---------------------------------------------------------------------------

def load_geneturing_tasks(
    path: str = None,
    module_name: str = "Gene alias",
    sample_size: int = 5,
) -> list[dict]:
    """
    Load GeneTuring Q&A tasks.

    If `path` points to a local JSON/CSV file it will be loaded directly.
    Otherwise uses the official GeneTuring CSV (data/Q_A_dataset.csv) if present,
    falling back to the built-in 25-question mock dataset.

    GeneTuring JSON schema: [{"module": str, "question": str, "gold_standard": str}]
    """
    if path:
        df = _load_external(path)
    else:
        df = _default_df()

    if module_name == "all":
        return df.head(sample_size).to_dict("records")

    subset = df[df["module"] == module_name].head(sample_size)
    if subset.empty:
        available = ", ".join(f'"{m}"' for m in sorted(df["module"].unique()))
        raise ValueError(f"Module '{module_name}' not found. Available: {available}")

    return subset.to_dict("records")


# ---------------------------------------------------------------------------
# Single-module evaluation loop
# ---------------------------------------------------------------------------

def run_eval(app, module_name: str = "Gene alias", sample_size: int = 5,
             path: str = None, use_llm_judge: bool = False, judge_llm=None) -> pd.DataFrame:
    """
    Run the compiled LangGraph agent against GeneTuring tasks and return a scored DataFrame.
    Use module_name='all' to run across all built-in modules.
    Set use_llm_judge=True to enable LLM-as-judge fallback when exact match fails.
    """
    tasks = load_geneturing_tasks(path=path, module_name=module_name, sample_size=sample_size)
    label = "ALL modules" if module_name == "all" else f"[{module_name}]"
    judge_label = " + LLM judge" if use_llm_judge else ""
    print(f"Evaluating agent on {len(tasks)} GeneTuring {label} tasks{judge_label}...\n")

    results = []
    for task in tasks:
        question      = task["question"]
        gold_standard = task["gold_standard"]

        output_state = app.invoke({"messages": [HumanMessage(content=question)]})
        agent_answer = output_state["messages"][-1].content

        scores = score_answer(question, agent_answer, gold_standard, use_llm_judge, judge_llm)

        results.append({
            "Module":          task["module"],
            "Question":        question,
            "Expected":        gold_standard,
            "Agent_Output":    agent_answer,
            "ExactMatch":      scores["ExactMatch"],
            "LLMJudge":        scores["LLMJudge"],
            "LLMJudgeReason":  scores["LLMJudgeReason"],
            "FinalScore":      scores["FinalScore"],
            "Jaccard":         round(jaccard_score(agent_answer, gold_standard), 3),
        })

    df = pd.DataFrame(results)
    _print_summary(df, module_name, use_llm_judge)
    return df


# ---------------------------------------------------------------------------
# All-modules benchmark
# ---------------------------------------------------------------------------

def run_benchmark(app, sample_per_module: int = 3, path: str = None,
                  use_llm_judge: bool = False, judge_llm=None,
                  modules: list = None) -> pd.DataFrame:
    """
    Run the agent across all available GeneTuring modules and print a
    per-module accuracy table plus an overall score.

    modules: optional list of module names to restrict the run (default = all).
    """
    df_all = _load_external(path) if path else _default_df()
    available_modules = sorted(df_all["module"].unique())
    if modules:
        available_modules = [m for m in available_modules if m in modules]
    all_results = []

    for module in available_modules:
        subset = df_all[df_all["module"] == module].head(sample_per_module).to_dict("records")
        if not subset:
            continue
        print(f"\n-- {module} ({len(subset)} tasks) --")
        for task in subset:
            output_state = app.invoke({"messages": [HumanMessage(content=task["question"])]})
            agent_answer = output_state["messages"][-1].content
            scores = score_answer(task["question"], agent_answer, task["gold_standard"],
                                  use_llm_judge, judge_llm)
            all_results.append({
                "Module":         module,
                "Question":       task["question"],
                "Expected":       task["gold_standard"],
                "Agent_Output":   agent_answer,
                "ExactMatch":     scores["ExactMatch"],
                "LLMJudge":       scores["LLMJudge"],
                "LLMJudgeReason": scores["LLMJudgeReason"],
                "FinalScore":     scores["FinalScore"],
                "Jaccard":        round(jaccard_score(agent_answer, task["gold_standard"]), 3),
            })
            status = "PASS" if all_results[-1]["FinalScore"] else "FAIL"
            print(f"  [{status}] {task['question'][:60]:<60} -> {task['gold_standard']}")

    df = pd.DataFrame(all_results)
    print("\n" + "-" * 60)
    print("BENCHMARK SUMMARY")
    print("-" * 60)

    summary = df.groupby("Module").agg(
        Tasks=("FinalScore", "count"),
        ExactMatch=("ExactMatch", "mean"),
        FinalScore=("FinalScore", "mean"),
        AvgJaccard=("Jaccard", "mean"),
    ).round(3)
    summary["ExactMatch"] = summary["ExactMatch"].map(lambda x: f"{x:.1%}")
    summary["FinalScore"] = summary["FinalScore"].map(lambda x: f"{x:.1%}")
    print(summary.to_string())
    print(f"\nOverall Exact Match : {df['ExactMatch'].mean():.1%}  ({df['ExactMatch'].sum():.0f}/{len(df)} correct)")
    if use_llm_judge:
        print(f"Overall Final Score : {df['FinalScore'].mean():.1%}  ({df['FinalScore'].sum():.0f}/{len(df)} correct)  [with LLM judge]")

    return df


def _print_summary(df: pd.DataFrame, module_name: str, use_llm_judge: bool = False):
    cols = ["Module", "Question", "Expected", "Agent_Output", "ExactMatch"]
    if use_llm_judge:
        cols += ["LLMJudge", "LLMJudgeReason", "FinalScore"]
    cols += ["Jaccard"]
    print(df[cols].to_string(index=False))
    print(f"\nExact Match Accuracy : {df['ExactMatch'].mean():.1%}")
    if use_llm_judge:
        print(f"Final Score (+ judge): {df['FinalScore'].mean():.1%}")
    print(f"Avg Jaccard Score    : {df['Jaccard'].mean():.3f}")


def _load_external(path: str) -> pd.DataFrame:
    """Load CSV or JSON and normalize column names to lowercase snake_case."""
    if path.endswith(".json"):
        with open(path, encoding="utf-8") as f:
            df = pd.DataFrame(json.load(f))
    else:
        df = pd.read_csv(path)
    # Normalize GeneTuring CSV column names: Module/Question/Goldstandard -> module/question/gold_standard
    rename = {"Module": "module", "Question": "question", "Goldstandard": "gold_standard"}
    df = df.rename(columns={k: v for k, v in rename.items() if k in df.columns})
    return df


def _default_df() -> pd.DataFrame:
    """Return the official GeneTuring CSV if present, else the built-in mock data."""
    if os.path.exists(DEFAULT_DATA_PATH):
        return _load_external(DEFAULT_DATA_PATH)
    return pd.DataFrame(MOCK_DATA)
