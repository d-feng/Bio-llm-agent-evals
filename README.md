# Bio LLM Agent Evals

A curated collection of benchmarks and evaluation frameworks for testing LLM and autonomous AI agent performance in drug discovery and bioinformatics.

When architecting autonomous AI systems for drug discovery, having evaluations that test both raw multi-omics reasoning and the ability to execute API calls or code is critical. The benchmarks below are organized by the type of capability they assess.

---

## Eval Scripts

Ready-to-run evaluation scripts using LangGraph + Claude against GeneTuring.

### Project layout

```
Bio-llm-agent-evals/
├── tools/
│   └── ncbi_gene_tool.py       # LangChain tools: NCBI Gene, NCBI dbSNP, Ensembl REST API
├── agents/
│   ├── genomic_agent.py        # Basic LangGraph agent
│   └── react_genomic_agent.py  # ReAct agent with question classifier (recommended)
├── evals/
│   ├── geneturing_eval.py      # Data loader + scoring (exact match, Jaccard, LLM judge)
│   └── report.py               # Markdown and Word report generation
├── data/
│   └── Q_A_dataset.csv         # Official GeneTuring dataset (1,600 questions, 16 modules)
├── run_eval.py                  # CLI entrypoint
└── requirements.txt
```

### Quick start

```bash
pip install -r requirements.txt
cp .env.example .env             # add your ANTHROPIC_API_KEY

# Single module (Gene alias, 5 questions)
python run_eval.py

# Run a specific module
python run_eval.py --module "SNP location" --sample 10

# Full benchmark across all 16 modules with LLM judge + report
python run_eval.py --benchmark --llm-judge --report report.md

# Select specific modules (100-question run across 10 modules)
python run_eval.py --benchmark --sample 10 --llm-judge \
  --modules "Gene alias,SNP location,Gene location,Gene disease association,Gene SNP association,Gene name conversion,Gene name extraction,Gene ontology,Protein-coding genes,TF regulation" \
  --report report_100.md --output results_100.csv
```

### Scoring

| Metric | Use case |
|---|---|
| Exact match | Single-answer questions (e.g. official gene symbol) |
| Jaccard Index | Multi-gene alias questions where partial credit applies |
| LLM judge | Fallback for format mismatches and verbose answers (e.g. "Chromosome 8" vs "chr8") |

### Benchmark results (100 questions, ReAct agent + LLM judge)

| Module | Exact Match | Final Score |
|---|---|---|
| Gene alias | 100% | 100% |
| Gene SNP association | 100% | 100% |
| Gene name conversion | 100% | 100% |
| SNP location | 0%* | 100% |
| Gene name extraction | 40% | 90% |
| Protein-coding genes | 0%* | 80% |
| Gene disease association | 50% | 60% |
| Gene location | 0%* | 60% |
| TF regulation | 30% | 50% |
| Gene ontology | 0% | 40% |
| **Overall** | **42%** | **78%** |

*Low exact match due to format mismatch — agent returns "Chromosome 8", dataset expects "chr8". LLM judge resolves these correctly.

### Known limitations

**GeneTuring Gene location module — unresolvable identifiers**

Four identifier types in the dataset cannot be resolved via any public REST API:

| Identifier | Type | Expected | Issue |
|---|---|---|---|
| `LA16c-329F2.2` | BAC clone (LLNL library) | chr16 | Not indexed in NCBI Gene or Ensembl |
| `RP11-17A4.3` | BAC clone (RPCI-11 library) | chr8 | Not indexed in NCBI Gene or Ensembl |
| `ENSG10010137169.1` | Non-standard Ensembl ID | chr4 | Invalid/retired ID — not found in GRCh37 or GRCh38 |
| `AC018712.2` | GenBank contig accession | chr2 | Sequence accession, not a gene record |

These were resolvable via older UCSC Genome Browser tracks or legacy genome assembly databases that no longer have public REST endpoints. The agent's Gene location score is capped at ~60% on this module due to these dataset-level limitations, not agent reasoning errors.

**Modules requiring specialized tools (excluded from standard benchmark)**

The following 6 GeneTuring modules require tools beyond NCBI/Ensembl APIs and are excluded from the default benchmark run:

| Module | Requirement |
|---|---|
| Amino acid translation | Codon translation tool (long nucleotide sequences) |
| DNA sequence extraction | NCBI sequence fetch by genomic coordinates |
| Human genome DNA alignment | BLAST against GRCh38 |
| Human genome DNA alignment programming | BLAST + code execution |
| Multi-species DNA alignment | Cross-species BLAST |
| Multi-species DNA alignment programming | Cross-species BLAST + code execution |

---

## Benchmark Resources

---

## Agentic & Workflow-Driven Benchmarks

Benchmarks that evaluate autonomous agents — tool use, API calls, code execution, and multi-step reasoning.

### GeneTuring
A comprehensive Q&A benchmarking suite evaluating genomic reasoning and knowledge retrieval. It consists of over 1,600 curated questions across 16 genomics modules, such as SNP locations, gene-disease associations, and multi-species DNA alignment. Also explores augmenting LLMs with domain-specific tools (GeneGPT, SeqSnap) to test API-driven execution against NCBI databases.

- **Link:** [github.com/Winnie09/GeneTuring](https://github.com/Winnie09/GeneTuring)
- **Tests:** Genomic Q&A, tool-augmented LLMs, NCBI API execution

---

### BixBench
A rigorous benchmark that drops the model into a Jupyter environment with real biological data files and tasks it with solving 53 complex scenarios (e.g., single-cell annotation, differential expression). Tests the model's ability to write, execute, and debug data science code (Python/R) rather than just answering multiple-choice questions.

- **Link:** [huggingface.co/datasets/futurehouse/BixBench](https://huggingface.co/datasets/futurehouse/BixBench)
- **Tests:** Autonomous agent code execution, scRNA-seq analysis, debugging

---

## Multi-Omics & Sequence-Level Benchmarks

Benchmarks that evaluate an LLM's ability to reason over raw biological sequences and multi-omics data.

### Biology-Instructions
The first large-scale dataset engineered specifically to test multi-omics sequence understanding. Evaluates an LLM's capacity to process and reason over actual biological syntax — DNA, RNA, proteins, and multi-molecular interactions — rather than just interpreting natural language text about biology.

- **Link:** [github.com/hhnqqq/Biology-Instructions](https://github.com/hhnqqq/Biology-Instructions)
- **Tests:** DNA/RNA/protein sequence reasoning, multi-omics understanding

---

### Bioinfo-Bench
A benchmark framework assessing academic knowledge and data mining skills across 10 distinct bioinformatics domains (including phylogenetics, systems biology, and genome analysis). Evaluates models across three cognitive tiers: knowledge acquisition, knowledge analysis, and knowledge application.

- **Link:** [huggingface.co/datasets/Qiyuan04/bioinfo-bench](https://huggingface.co/datasets/Qiyuan04/bioinfo-bench)
- **Tests:** Bioinformatics domain knowledge, phylogenetics, genome analysis

---

## Biomedical Literature & Protocol Benchmarks

Benchmarks that evaluate comprehension of scientific literature, wet-lab protocols, and clinical reasoning.

### BioProBench
A massive dataset constructed from 27,000 biological protocols, resulting in over 550,000 structured instances. Evaluates a model's ability to comprehend wet-lab laboratory procedures, correctly order experimental steps, and troubleshoot protocol errors.

- **Link:** [huggingface.co/datasets/BioProBench/BioProBench](https://huggingface.co/datasets/BioProBench/BioProBench)
- **Tests:** Protocol comprehension, step ordering, error troubleshooting

---

### CARDBiomedBench
Featuring over 68,000 question-answer pairs focused on biomedical research, this dataset rigorously tests complex reasoning and identifies hallucination risks in high-stakes medical literature contexts.

- **Link:** [huggingface.co/datasets/NIH-CARD/CARDBiomedBench](https://huggingface.co/datasets/NIH-CARD/CARDBiomedBench)
- **Tests:** Biomedical QA, hallucination detection, complex reasoning

---

## Summary Table

| Benchmark | Category | Scale | Key Capability Tested |
|---|---|---|---|
| [GeneTuring](https://github.com/Winnie09/GeneTuring) | Agentic | 1,600+ questions | Genomic Q&A + API tool use |
| [BixBench](https://huggingface.co/datasets/futurehouse/BixBench) | Agentic | 53 scenarios | Code execution + debugging |
| [Biology-Instructions](https://github.com/hhnqqq/Biology-Instructions) | Multi-omics | Large-scale | Sequence-level reasoning |
| [Bioinfo-Bench](https://huggingface.co/datasets/Qiyuan04/bioinfo-bench) | Multi-omics | 10 domains | Domain knowledge tiers |
| [BioProBench](https://huggingface.co/datasets/BioProBench/BioProBench) | Protocol | 550,000+ instances | Wet-lab protocol reasoning |
| [CARDBiomedBench](https://huggingface.co/datasets/NIH-CARD/CARDBiomedBench) | Literature | 68,000+ QA pairs | Hallucination + reasoning |

---

## Contributing

Pull requests welcome. Please follow the format above when adding a new benchmark:
- Category (Agentic / Multi-omics / Literature / Clinical / Other)
- Scale (dataset size)
- Link
- 2–3 sentence description
- Key capability tested

---

## Related repos

- [AskDocs](https://github.com/d-feng/AskDocs) — RAG chat app for document Q&A
- [LangGraph-cookbook](https://github.com/d-feng/LangGraph-cookbook) — LangGraph + Claude agent recipes
- [Agent-connector](https://github.com/d-feng/Agent-connector) — Biomni agent orchestration framework
