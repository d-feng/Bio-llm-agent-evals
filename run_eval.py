"""
run_eval.py
-----------
Entrypoint for running the genomic agent evaluation against GeneTuring.

Usage:
    python run_eval.py
    python run_eval.py --module "SNP location" --sample 10
    python run_eval.py --path data/geneturing.json --module "Gene alias"
"""

import argparse
from agents.genomic_agent import build_genomic_agent
from evals.geneturing_eval import run_eval


def parse_args():
    parser = argparse.ArgumentParser(description="Run genomic agent eval on GeneTuring")
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

    print("Building genomic agent...")
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
