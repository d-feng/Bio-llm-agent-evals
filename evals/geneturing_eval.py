"""
evals/geneturing_eval.py
------------------------
Evaluation loop that runs a LangGraph genomic agent against GeneTuring tasks
and scores its answers using exact-match and Jaccard Index.

GeneTuring repo: https://github.com/Winnie09/GeneTuring
Covers 8 of the 16 GeneTuring modules in the built-in mock dataset.
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

AVAILABLE_MODULES = sorted(set(d["module"] for d in MOCK_DATA))


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
    it will be loaded directly. Otherwise falls back to the built-in mock dataset.

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
        df = pd.DataFrame(MOCK_DATA)

    if module_name == "all":
        return df.head(sample_size).to_dict("records")

    subset = df[df["module"] == module_name].head(sample_size)
    if subset.empty:
        available = ", ".join(f'"{m}"' for m in AVAILABLE_MODULES)
        raise ValueError(f"Module '{module_name}' not found. Available: {available}")

    return subset.to_dict("records")


# ---------------------------------------------------------------------------
# Single-module evaluation loop
# ---------------------------------------------------------------------------

def run_eval(app, module_name: str = "Gene alias", sample_size: int = 5, path: str = None) -> pd.DataFrame:
    """
    Run the compiled LangGraph agent against GeneTuring tasks and return a scored DataFrame.
    Use module_name='all' to run across all built-in modules.
    """
    tasks = load_geneturing_tasks(path=path, module_name=module_name, sample_size=sample_size)
    label = "ALL modules" if module_name == "all" else f"[{module_name}]"
    print(f"Evaluating agent on {len(tasks)} GeneTuring {label} tasks...\n")

    results = []
    for task in tasks:
        question      = task["question"]
        gold_standard = task["gold_standard"]

        output_state = app.invoke({"messages": [HumanMessage(content=question)]})
        agent_answer = output_state["messages"][-1].content

        results.append({
            "Module":       task["module"],
            "Question":     question,
            "Expected":     gold_standard,
            "Agent_Output": agent_answer,
            "ExactMatch":   exact_match(agent_answer, gold_standard),
            "Jaccard":      round(jaccard_score(agent_answer, gold_standard), 3),
        })

    df = pd.DataFrame(results)
    _print_summary(df, module_name)
    return df


# ---------------------------------------------------------------------------
# All-modules benchmark
# ---------------------------------------------------------------------------

def run_benchmark(app, sample_per_module: int = 3, path: str = None) -> pd.DataFrame:
    """
    Run the agent across all available GeneTuring modules and print a
    per-module accuracy table plus an overall score.
    """
    df_all = pd.DataFrame(MOCK_DATA) if not path else _load_external(path)
    all_results = []

    for module in AVAILABLE_MODULES:
        subset = df_all[df_all["module"] == module].head(sample_per_module).to_dict("records")
        if not subset:
            continue
        print(f"\n-- {module} ({len(subset)} tasks) --")
        for task in subset:
            output_state = app.invoke({"messages": [HumanMessage(content=task["question"])]})
            agent_answer = output_state["messages"][-1].content
            all_results.append({
                "Module":       module,
                "Question":     task["question"],
                "Expected":     task["gold_standard"],
                "Agent_Output": agent_answer,
                "ExactMatch":   exact_match(agent_answer, task["gold_standard"]),
                "Jaccard":      round(jaccard_score(agent_answer, task["gold_standard"]), 3),
            })
            status = "PASS" if all_results[-1]["ExactMatch"] else "FAIL"
            print(f"  [{status}] {task['question'][:60]:<60} -> {task['gold_standard']}")

    df = pd.DataFrame(all_results)
    print("\n" + "-" * 60)
    print("BENCHMARK SUMMARY")
    print("-" * 60)

    summary = df.groupby("Module").agg(
        Tasks=("ExactMatch", "count"),
        ExactMatch=("ExactMatch", "mean"),
        AvgJaccard=("Jaccard", "mean"),
    ).round(3)
    summary["ExactMatch"] = summary["ExactMatch"].map(lambda x: f"{x:.1%}")
    print(summary.to_string())
    print(f"\nOverall Exact Match: {df['ExactMatch'].mean():.1%}  ({df['ExactMatch'].sum():.0f}/{len(df)} correct)")

    return df


def _print_summary(df: pd.DataFrame, module_name: str):
    print(df[["Module", "Question", "Expected", "Agent_Output", "ExactMatch", "Jaccard"]].to_string(index=False))
    print(f"\nExact Match Accuracy : {df['ExactMatch'].mean():.1%}")
    print(f"Avg Jaccard Score    : {df['Jaccard'].mean():.3f}")


def _load_external(path: str) -> pd.DataFrame:
    if path.endswith(".json"):
        with open(path, encoding="utf-8") as f:
            return pd.DataFrame(json.load(f))
    return pd.read_csv(path)
