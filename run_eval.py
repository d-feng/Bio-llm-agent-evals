"""
run_eval.py
-----------
Entrypoint for running genomic agent evaluations against GeneTuring.

Usage:
    # Single module (ReAct agent by default)
    python run_eval.py
    python run_eval.py --module "SNP location"
    python run_eval.py --module "Gene location"

    # Full benchmark across all 8 modules
    python run_eval.py --benchmark
    python run_eval.py --benchmark --sample 3

    # Compare agents
    python run_eval.py --agent basic --module "SNP location"

    # Save results
    python run_eval.py --benchmark --output results.csv

Available modules:
    Gene alias, SNP location, Gene location, Gene disease,
    Gene function, Chromosome gene count, Human genome, Multi-species
"""

import argparse
import os
from dotenv import load_dotenv
from evals.geneturing_eval import run_eval, run_benchmark, AVAILABLE_MODULES

load_dotenv()


def parse_args():
    parser = argparse.ArgumentParser(description="Run genomic agent eval on GeneTuring")
    parser.add_argument("--agent", type=str, default="react",
                        choices=["basic", "react"],
                        help="Agent type: 'basic' or 'react' (default: react — recommended)")
    parser.add_argument("--module", type=str, default="Gene alias",
                        help=f"GeneTuring module name. Available: {', '.join(AVAILABLE_MODULES)}")
    parser.add_argument("--sample", type=int, default=5,
                        help="Number of tasks per module (default: 5)")
    parser.add_argument("--benchmark", action="store_true",
                        help="Run full benchmark across all modules")
    parser.add_argument("--path", type=str, default=None,
                        help="Path to local GeneTuring JSON/CSV file (optional)")
    parser.add_argument("--output", type=str, default=None,
                        help="Save results to CSV (e.g. results.csv)")
    parser.add_argument("--llm-judge", action="store_true",
                        help="Use LLM as judge fallback when exact match fails")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.agent == "react":
        from agents.react_genomic_agent import build_react_genomic_agent
        print("Building ReAct genomic agent...\n")
        app = build_react_genomic_agent()
    else:
        from agents.genomic_agent import build_genomic_agent
        print("Building basic genomic agent...\n")
        app = build_genomic_agent()

    use_llm_judge = args.llm_judge
    judge_llm = None
    if use_llm_judge:
        from langchain_anthropic import ChatAnthropic
        judge_llm = ChatAnthropic(
            model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            max_tokens=256,
        )
        print("LLM judge enabled — will score failed exact-match answers semantically.\n")

    if args.benchmark:
        results_df = run_benchmark(app, sample_per_module=args.sample, path=args.path,
                                   use_llm_judge=use_llm_judge, judge_llm=judge_llm)
    else:
        results_df = run_eval(
            app=app,
            module_name=args.module,
            sample_size=args.sample,
            path=args.path,
            use_llm_judge=use_llm_judge,
            judge_llm=judge_llm,
        )

    if args.output:
        results_df.to_csv(args.output, index=False)
        print(f"\nResults saved to {args.output}")
