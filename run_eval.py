"""
run_eval.py
-----------
Entrypoint for running genomic agent evaluations against GeneTuring.

Usage:
    python run_eval.py
    python run_eval.py --agent react --module "SNP location" --sample 10
    python run_eval.py --agent react --module "Gene alias" --output results.csv
    python run_eval.py --path data/geneturing.json --module "Gene alias"

Agents:
    basic  — binds both tools, lets the LLM decide (default)
    react  — ReAct agent that classifies the question type before selecting a tool
"""

import argparse
from evals.geneturing_eval import run_eval


def parse_args():
    parser = argparse.ArgumentParser(description="Run genomic agent eval on GeneTuring")
    parser.add_argument("--agent", type=str, default="react",
                        choices=["basic", "react"],
                        help="Agent type: 'basic' or 'react' (default: react — recommended)")
    parser.add_argument("--module", type=str, default="Gene alias",
                        help="GeneTuring module name (default: 'Gene alias')")
    parser.add_argument("--sample", type=int, default=5,
                        help="Number of tasks to evaluate (default: 5)")
    parser.add_argument("--path", type=str, default=None,
                        help="Path to local GeneTuring JSON/CSV file (optional)")
    parser.add_argument("--output", type=str, default=None,
                        help="Save results to CSV (e.g. results.csv)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.agent == "react":
        from agents.react_genomic_agent import build_react_genomic_agent
        print("Building ReAct genomic agent...")
        app = build_react_genomic_agent()
    else:
        from agents.genomic_agent import build_genomic_agent
        print("Building basic genomic agent...")
        app = build_genomic_agent()

    results_df = run_eval(
        app=app,
        module_name=args.module,
        sample_size=args.sample,
        path=args.path,
    )

    if args.output:
        results_df.to_csv(args.output, index=False)
        print(f"\nResults saved to {args.output}")
