# Bio LLM Agent Evals

A curated collection of benchmarks and evaluation frameworks for testing LLM and autonomous AI agent performance in drug discovery and bioinformatics.

When architecting autonomous AI systems for drug discovery, having evaluations that test both raw multi-omics reasoning and the ability to execute API calls or code is critical. The benchmarks below are organized by the type of capability they assess.

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
