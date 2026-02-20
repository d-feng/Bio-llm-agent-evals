"""
evals/geneturing_eval.py
------------------------
Evaluation loop that runs a LangGraph genomic agent against GeneTuring tasks
and scores its answers using exact-match (and optionally Jaccard Index).

GeneTuring repo: https://github.com/Winnie09/GeneTuring
"""

import json
import pandas as pd
from langchain_core.messages import HumanMessage


# ---------------------------------------------------------------------------
# Scoring helpers
# ---------------------------------------------------------------------------

def exact_match(prediction: str, gold: str) -> bool:
    return gold.strip().lower() in prediction.strip().lower()


def jaccard_score(prediction: str, gold: str) -> float:
    """
    Jaccard Index over token sets — used for multi-gene alias questions
    where the answer may contain several gene names.
    """
    pred_tokens = set(prediction.lower().split())
    gold_tokens = set(gold.lower().split())
    if not pred_tokens and not gold_tokens:
        return 1.0
    intersection = pred_tokens & gold_tokens
    union = pred_tokens | gold_tokens
    return len(intersection) / len(union)


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

    If `path` points to a local JSON/CSV file exported from the GeneTuring repo,
    it will be loaded directly. Otherwise falls back to a built-in mock subset
    for quick testing without downloading the full dataset.

    GeneTuring JSON schema: [{"module": str, "question": str, "gold_standard": str}]
    """
    if path:
        if path.endswith(".json"):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            df = pd.DataFrame(data)
        elif path.endswith(".csv"):
            df = pd.read_csv(path)
        else:
            raise ValueError("Unsupported file format. Use .json or .csv")
    else:
        # Built-in mock subset covering Gene alias and SNP location modules
        mock_data = [
            {"module": "Gene alias", "question": "What is the official gene symbol of HER2?",      "gold_standard": "ERBB2"},
            {"module": "Gene alias", "question": "What is the official gene symbol of p53?",       "gold_standard": "TP53"},
            {"module": "Gene alias", "question": "What is the official gene symbol of VEGF?",      "gold_standard": "VEGFA"},
            {"module": "Gene alias", "question": "What is the official gene symbol of PD-L1?",     "gold_standard": "CD274"},
            {"module": "Gene alias", "question": "What is the official gene symbol of c-MET?",     "gold_standard": "MET"},
            {"module": "SNP location", "question": "What chromosome is rs1229984 located on?",     "gold_standard": "Chromosome 4"},
            {"module": "SNP location", "question": "What chromosome is rs334 located on?",         "gold_standard": "Chromosome 11"},
        ]
        df = pd.DataFrame(mock_data)

    subset = df[df["module"] == module_name].head(sample_size)
    return subset.to_dict("records")


# ---------------------------------------------------------------------------
# Evaluation loop
# ---------------------------------------------------------------------------

def run_eval(app, module_name: str = "Gene alias", sample_size: int = 5, path: str = None) -> pd.DataFrame:
    """
    Run the compiled LangGraph agent against GeneTuring tasks and return a
    scored results DataFrame.

    Parameters
    ----------
    app         : compiled LangGraph app (from agents/genomic_agent.py)
    module_name : GeneTuring module to evaluate (e.g. "Gene alias", "SNP location")
    sample_size : number of tasks to evaluate
    path        : optional path to a local GeneTuring JSON/CSV file
    """
    tasks = load_geneturing_tasks(path=path, module_name=module_name, sample_size=sample_size)
    print(f"Evaluating agent on {len(tasks)} GeneTuring [{module_name}] tasks...\n")

    results = []
    for task in tasks:
        question     = task["question"]
        gold_standard = task["gold_standard"]

        output_state = app.invoke({"messages": [HumanMessage(content=question)]})
        agent_answer = output_state["messages"][-1].content

        results.append({
            "Module":       module_name,
            "Question":     question,
            "Expected":     gold_standard,
            "Agent_Output": agent_answer,
            "ExactMatch":   exact_match(agent_answer, gold_standard),
            "Jaccard":      round(jaccard_score(agent_answer, gold_standard), 3),
        })

    df = pd.DataFrame(results)

    # Summary
    accuracy = df["ExactMatch"].mean()
    avg_jaccard = df["Jaccard"].mean()
    print(df[["Question", "Expected", "Agent_Output", "ExactMatch", "Jaccard"]].to_string(index=False))
    print(f"\nExact Match Accuracy : {accuracy:.1%}")
    print(f"Avg Jaccard Score    : {avg_jaccard:.3f}")

    return df
