# Genomic Agent Benchmark Report

**Date:** 2026-02-20 20:00  
**Agent:** react  
**Scoring:** Exact Match + LLM Judge fallback

---

## Overall Results

| Metric | Score |
|---|---|
| Exact Match Accuracy | 42.0% (42/100) |
| Final Score (+ LLM judge) | **78.0% (78/100)** |
| Total Tasks | 100 |

## Per-Module Results

| Module | Tasks | Exact Match | Final Score | Avg Jaccard |
|---|---|---|---|---|
| Gene SNP association | 10 | 100.0% | 100.0% | 0.003 |
| Gene alias | 10 | 100.0% | 100.0% | 0.016 |
| Gene disease association | 10 | 50.0% | 60.0% | 0.000 |
| Gene location | 10 | 0.0% | 60.0% | 0.000 |
| Gene name conversion | 10 | 100.0% | 100.0% | 0.000 |
| Gene name extraction | 10 | 40.0% | 90.0% | 0.019 |
| Gene ontology | 10 | 0.0% | 40.0% | 0.017 |
| Protein-coding genes | 10 | 0.0% | 80.0% | 0.000 |
| SNP location | 10 | 0.0% | 100.0% | 0.000 |
| TF regulation | 10 | 30.0% | 50.0% | 0.002 |

## Detailed Results

### Gene SNP association

| Question | Expected | Agent Output | Exact | Judge | Reason | 
|---|---|---|---|---|---|
| The name of the gene associated with SNP rs1217074595 is | LINC01270 | STEP 3 — ANSWER: The gene associated with SNP rs1217074595 is **LINC01270**. | PASS |
| The name of the gene associated with SNP rs1241371358 is | LRRC23 | STEP 3 — ANSWER: The gene associated with SNP rs1241371358 is **LRRC23**. | PASS |
| The name of the gene associated with SNP rs1481036795 is | SEPTIN11 | STEP 3 — ANSWER: The gene associated with SNP rs1481036795 is **SEPTIN11**. | PASS |
| The name of the gene associated with SNP rs1318850293 is | PLEKHG7 | STEP 3 — ANSWER: Based on the NCBI dbSNP data, the gene associated with SNP rs13 | PASS |
| The name of the gene associated with SNP rs996319727 is | USP39 | STEP 3 — ANSWER: The name of the gene associated with SNP rs996319727 is **USP39 | PASS |
| The name of the gene associated with SNP rs577757681 is | OXR1 | STEP 3 — ANSWER: The name of the gene associated with SNP rs577757681 is **OXR1* | PASS |
| The name of the gene associated with SNP rs1294482311 is | DMXL1 | STEP 3 — ANSWER: The gene associated with SNP rs1294482311 is **DMXL1**. | PASS |
| The name of the gene associated with SNP rs979970652 is | KHDRBS2 | STEP 3 — ANSWER: Based on the NCBI dbSNP data, the gene associated with SNP rs97 | PASS |
| The name of the gene associated with SNP rs1029002401 is | MAJIN | STEP 3 — ANSWER: The name of the gene associated with SNP rs1029002401 is **MAJI | PASS |
| The name of the gene associated with SNP rs1015227 is | SCHLAP1 | STEP 3 — ANSWER: Based on the dbSNP database search, the gene associated with SN | PASS |

### Gene alias

| Question | Expected | Agent Output | Exact | Judge | Reason | 
|---|---|---|---|---|---|
| The official gene symbol of gene LMP10 is | PSMB10 | STEP 3 — ANSWER: The official gene symbol of gene LMP10 is **PSMB10**. LMP10 is  | PASS |
| The official gene symbol of gene SNAT6 is | SLC38A6 | STEP 3 — ANSWER: The official gene symbol of gene SNAT6 is **SLC38A6**. SNAT6 is | PASS |
| The official gene symbol of gene IMD20 is | FCGR3A | STEP 3 — ANSWER: The official gene symbol of gene IMD20 is **FCGR3A**. IMD20 is  | PASS |
| The official gene symbol of gene C20orf195 is | FNDC11 | STEP 3 — ANSWER: The official gene symbol of gene C20orf195 is **FNDC11** (fibro | PASS |
| The official gene symbol of gene CXorf40B is | EOLA2 | STEP 3 — ANSWER: Based on the NCBI Gene database results, the official gene symb | PASS |
| The official gene symbol of gene QSCN6L1 is | QSOX2 | STEP 3 — ANSWER: The official gene symbol of gene QSCN6L1 is **QSOX2** (quiescin | PASS |
| The official gene symbol of gene OR11-86 is | OR10A2 | STEP 3 — ANSWER: The official gene symbol of gene OR11-86 is **OR10A2**. OR11-86 | PASS |
| The official gene symbol of gene NPAP60L is | NUP50 | STEP 3 — ANSWER: Based on the NCBI Gene database results, the official gene symb | PASS |
| The official gene symbol of gene AF10 is | MLLT10 | STEP 3 — ANSWER: The official gene symbol of gene AF10 is **MLLT10**. AF10 is an | PASS |
| The official gene symbol of gene bMRP63 is | MRPL57 | STEP 3 — ANSWER: The official gene symbol of gene bMRP63 is **MRPL57** (mitochon | PASS |

### Gene disease association

| Question | Expected | Agent Output | Exact | Judge | Reason | 
|---|---|---|---|---|---|
| The name of the gene related to Hemolytic anemia due to phosphofructok | PFKL | The search results are not returning the expected phosphofructokinase genes. Bas | FAIL | FAIL | The agent provided PFKM as the gene symbol, but the gold standard is PFKL, and g |
| The name of the gene related to Distal renal tubular acidosis is | SLC4A1, ATP6V0A4 | STEP 3 — ANSWER: Based on the NCBI Gene database search, the primary gene relate | FAIL | FAIL | The agent only identified SLC4A1 but missed ATP6V0A4, which is also a key gene r |
| The name of the gene related to Pseudohypoparathyroidism Ic is | GNAS | STEP 3 — ANSWER: Based on the NCBI Gene database search, the gene related to Pse | PASS |
| The name of the gene related to Glycine N-methyltransferase deficiency | GNMT | STEP 3 — ANSWER: The name of the gene related to Glycine N-methyltransferase def | PASS |
| The name of the gene related to Meesmann corneal dystrophy is | KRT12, KRT3 | STEP 3 — ANSWER: Based on the NCBI Gene database results, the gene related to Me | FAIL | FAIL | The agent only provided KRT12 but missed KRT3, which is also a gene related to M |
| The name of the gene related to Chronic atrial and intestinal dysrhyth | SGO1 | STEP 3 — ANSWER: Based on the NCBI Gene database search, the gene related to Chr | PASS |
| The name of the gene related to Sensorineural deafness with mild renal | BSND | STEP 3 — ANSWER: Based on the search results, the gene related to Sensorineural  | FAIL | FAIL | The agent answered GATA3 but the gold standard is BSND, which are different gene |
| The name of the gene related to Bile acid malabsorption is | SLC10A2, SLC51B | STEP 3 — ANSWER: The gene related to bile acid malabsorption is **SLC10A2** (sol | FAIL | PASS | The agent correctly identified SLC10A2 as a gene related to bile acid malabsorpt |
| The name of the gene related to Immunodeficiency due to defect in MAPB | LAMTOR2 | STEP 3 — ANSWER: The gene related to Immunodeficiency due to defect in MAPBP-int | PASS |
| The name of the gene related to Currarino syndrome is | MNX1 | STEP 3 — ANSWER: The gene related to Currarino syndrome is **MNX1** (motor neuro | PASS |

### Gene location

| Question | Expected | Agent Output | Exact | Judge | Reason | 
|---|---|---|---|---|---|
| FAM66D gene is located on human genome chromosome | chr8 | STEP 3 — ANSWER: The FAM66D gene is located on human genome chromosome 8, specif | FAIL | PASS | The agent correctly identified that FAM66D is located on chromosome 8, which mat |
| TTTY7 gene is located on human genome chromosome | chrY | STEP 3 — ANSWER: The TTTY7 gene is located on chromosome Y of the human genome,  | FAIL | PASS | The agent correctly identified that the TTTY7 gene is located on chromosome Y, w |
| LA16c-329F2.2 gene is located on human genome chromosome | chr16 | STEP 3 — ANSWER: Based on the NCBI Gene database search, I could not find a gene | FAIL | FAIL | The agent failed to identify that the LA16c-329F2.2 gene is located on chromosom |
| RGS16 gene is located on human genome chromosome | chr1 | STEP 3 — ANSWER: The RGS16 gene is located on human chromosome 1, specifically a | FAIL | PASS | The agent correctly identified that RGS16 is located on chromosome 1, which matc |
| FOXL2NB gene is located on human genome chromosome | chr3 | STEP 3 — ANSWER: The FOXL2NB gene is located on human chromosome 3, specifically | FAIL | PASS | The agent correctly identified that FOXL2NB is located on chromosome 3, which ma |
| RP11-17A4.3 gene is located on human genome chromosome | chr8 | STEP 3 — ANSWER: The search did not return specific results for RP11-17A4.3 in t | FAIL | FAIL | The agent failed to provide the chromosome location (chr8) and instead stated th |
| EML3 gene is located on human genome chromosome | chr11 | STEP 3 — ANSWER: The EML3 gene is located on human chromosome 11, specifically a | FAIL | PASS | The agent correctly identified that the EML3 gene is located on chromosome 11, w |
| LPAR2 gene is located on human genome chromosome | chr19 | STEP 3 — ANSWER: The LPAR2 gene is located on human chromosome 19, specifically  | FAIL | PASS | The agent correctly identified that the LPAR2 gene is located on chromosome 19,  |
| ENSG10010137169.1 gene is located on human genome chromosome | chr4 | The NCBI Gene database doesn't return any results for "ENSG10010137169.1". This  | FAIL | FAIL | The agent failed to provide the chromosome location (chr4) and instead only expl |
| AC018712.2 gene is located on human genome chromosome | chr2 | STEP 3 — ANSWER: No results were found for "AC018712.2" in the NCBI Gene databas | FAIL | FAIL | The agent failed to provide the correct chromosome location (chr2) and instead s |

### Gene name conversion

| Question | Expected | Agent Output | Exact | Judge | Reason | 
|---|---|---|---|---|---|
| The official gene symbol of ENSG00000215251 is | FASTKD5 | STEP 3 — ANSWER: The official gene symbol of ENSG00000215251 is **FASTKD5**. | PASS |
| The official gene symbol of ENSG00000205403 is | CFI | STEP 3 — ANSWER: The official gene symbol of ENSG00000205403 is **CFI** (complem | PASS |
| The official gene symbol of ENSG00000140199 is | SLC12A6 | STEP 3 — ANSWER: The official gene symbol of ENSG00000140199 is **SLC12A6**. | PASS |
| The official gene symbol of ENSG00000149476 is | TKFC | STEP 3 — ANSWER: The official gene symbol of ENSG00000149476 is **TKFC** (trioki | PASS |
| The official gene symbol of ENSG00000291317 is | TMEM276 | STEP 3 — ANSWER: The official gene symbol of ENSG00000291317 is **TMEM276**. | PASS |
| The official gene symbol of ENSG00000174944 is | P2RY14 | STEP 3 — ANSWER: The official gene symbol of ENSG00000174944 is **P2RY14**. | PASS |
| The official gene symbol of ENSG00000138604 is | GLCE | STEP 3 — ANSWER: The official gene symbol of ENSG00000138604 is **GLCE** (glucur | PASS |
| The official gene symbol of ENSG00000174233 is | ADCY6 | STEP 3 — ANSWER: The official gene symbol of ENSG00000174233 is **ADCY6** (adeny | PASS |
| The official gene symbol of ENSG00000165487 is | MICU2 | STEP 3 — ANSWER: The official gene symbol of ENSG00000165487 is **MICU2**. | PASS |
| The official gene symbol of ENSG00000124157 is | SEMG2 | STEP 3 — ANSWER: The official gene symbol of ENSG00000124157 is **SEMG2**. | PASS |

### Gene name extraction

| Question | Expected | Agent Output | Exact | Judge | Reason | 
|---|---|---|---|---|---|
| The gene and protein names in the sentence 'Comparative analyses indic | No gene | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking me to identify gene and p | FAIL | PASS | The agent correctly identified that there are no gene or protein names in the se |
| The gene and protein names in the sentence 'Microscopic examination of | No gene | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking for gene and protein name | FAIL | PASS | The agent correctly identified that the sentence contains no gene or protein nam |
| The gene and protein names in the sentence 'Deletion analysis of the 3 | Sp1 binding site, embigin gene | Looking at this sentence, I can identify the following gene and protein names:   | FAIL | PASS | The agent correctly identified both "embigin" as a gene name and "Sp1" as a prot |
| The gene and protein names in the sentence 'To investigate the effect  | No gene | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking me to identify gene and p | PASS |
| The gene and protein names in the sentence 'All patients received marr | HLA | The gene/protein name identified in the sentence is:  **HLA** - Human Leukocyte  | PASS |
| The gene and protein names in the sentence 'Expression of the Asp but  | gB, gB | Looking at this sentence, I can identify the following gene and protein names:   | FAIL | PASS | The agent correctly identified "gB" as the gene/protein name appearing twice in  |
| The gene and protein names in the sentence 'We conclude that clonidine | No gene | Looking at the sentence you provided: "We conclude that clonidine 3 micrograms/k | FAIL | PASS | The agent correctly identified that the sentence contains no gene or protein nam |
| The gene and protein names in the sentence 'In addition, WR-3689, WR-1 | No gene | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking me to identify gene and p | PASS |
| The gene and protein names in the sentence 'Acute intoxication with cy | No gene | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking me to identify gene and p | PASS |
| The gene and protein names in the sentence 'This deletion disrupts the | PU.1, Ets domain | STEP 3 — ANSWER:  The gene and protein name in the sentence 'This deletion disru | FAIL | FAIL | The agent only identified "PU.1" but missed "Ets domain" which is also a protein |

### Gene ontology

| Question | Expected | Agent Output | Exact | Judge | Reason | 
|---|---|---|---|---|---|
| The enriched gene ontology term associated with SLC27A5, AKT1, AKT2, A | long chain fatty acid import across plasma membrane | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking about gene ontology (GO)  | FAIL | PASS | The agent's answer of "fatty acid metabolic process" or "lipid metabolic process |
| The enriched gene ontology term associated with FMR1, FBXL2, TMEM41B,  | modulation by host of viral rna genome replication | I'm experiencing API rate limiting issues with the NCBI tools. However, I can pr | FAIL | FAIL | The agent provided general GO terms like "RNA metabolism" and "cellular protein  |
| The enriched gene ontology term associated with GPER1, HRH1, LHCGR, P2 | positive regulation of inositol trisphosphate biosynthetic process | I'm encountering API rate limiting errors, but I can answer this question based  | FAIL | FAIL | The agent answered "G protein-coupled receptor signaling pathway" but the gold s |
| The enriched gene ontology term associated with CNTFR, ERBB3, KCNB1, R | regulation of motor neuron apoptotic process | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking about gene ontology enric | FAIL | PASS | The agent correctly identified that the gene set is enriched for apoptosis-relat |
| The enriched gene ontology term associated with ACSM1, ACOT4, CRAT, AC | short chain fatty acid metabolic process | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking about gene ontology enric | FAIL | PASS | The agent correctly identified that the enriched GO term is related to fatty aci |
| The enriched gene ontology term associated with ADA, NOC2L, FOXP1, IL2 | negative regulation of b cell apoptotic process | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking about Gene Ontology (GO)  | FAIL | FAIL | The agent identified general immune system processes but failed to identify the  |
| The enriched gene ontology term associated with CTNNB1, MUSTN1, TCF7L2 | positive regulation of proteoglycan biosynthetic process | I'm unable to retrieve the specific gene information due to API rate limits. How | FAIL | FAIL | The agent's answer focuses on Wnt signaling pathway and cell adhesion, which doe |
| The enriched gene ontology term associated with OSR1, FOXC2, GPR4, NOT | mesangial cell development | I'm experiencing API rate limiting issues with the NCBI tools. However, based on | FAIL | FAIL | The agent answered "blood vessel development" or "angiogenesis" while the gold s |
| The enriched gene ontology term associated with TTC36, GPS2, MIR138-1, | negative regulation of protein polyubiquitination | I need to classify this question first.  STEP 1 — CLASSIFY: This is a KNOWLEDGE  | FAIL | FAIL | The agent provided multiple related GO terms about general ubiquitination proces |
| The enriched gene ontology term associated with TLR6, MALT1, COPS8, CH | activation of nf kappab inducing kinase activity | I need to classify this question first.  STEP 1 — CLASSIFY: This is a **KNOWLEDG | FAIL | PASS | The agent's answer of "NF-kappaB signaling pathway" correctly identifies the sam |

### Protein-coding genes

| Question | Expected | Agent Output | Exact | Judge | Reason | 
|---|---|---|---|---|---|
| Regarding if the gene codes a protein, ATP5F1EP2 is | nan | STEP 3 — ANSWER: Based on the NCBI Gene database results, ATP5F1EP2 is a **pseud | FAIL | PASS | The agent correctly identifies ATP5F1EP2 as a pseudogene that does not code for  |
| Regarding if the gene codes a protein, LOC124907753 is | nan | STEP 3 — ANSWER: Based on the NCBI Gene database, LOC124907753 is described as " | FAIL | PASS | The agent's answer appropriately identifies that LOC124907753 is an uncharacteri |
| Regarding if the gene codes a protein, AMD1P4 is | nan | STEP 3 — ANSWER: Based on the NCBI Gene database, AMD1P4 is a **pseudogene** (ad | FAIL | PASS | The agent correctly identifies AMD1P4 as a pseudogene that does not code for a p |
| Regarding if the gene codes a protein, NODAL is | TRUE | STEP 3 — ANSWER: Based on the NCBI Gene database, NODAL is a protein-coding gene | FAIL | PASS | The agent correctly identifies that NODAL is a protein-coding gene, which matche |
| Regarding if the gene codes a protein, MIR4436B2 is | nan | STEP 3 — ANSWER: Based on the NCBI Gene database, MIR4436B2 is a **non-protein-c | FAIL | FAIL | The gold standard is "nan" (not available/no answer), but the agent provided a d |
| Regarding if the gene codes a protein, NAXE is | TRUE | STEP 3 — ANSWER: Based on the NCBI Gene database, NAXE is a protein-coding gene. | FAIL | PASS | The agent correctly identifies that NAXE is a protein-coding gene, which matches |
| Regarding if the gene codes a protein, LOC124909477 is | nan | STEP 3 — ANSWER: Based on the NCBI Gene database, LOC124909477 is described as " | FAIL | PASS | The agent correctly identifies that LOC124909477 is uncharacterized and acknowle |
| Regarding if the gene codes a protein, LINC01560 is | nan | STEP 3 — ANSWER: Based on the NCBI Gene database, LINC01560 is a **non-protein c | FAIL | FAIL | The gold standard is "nan" (not available/no answer expected), but the agent pro |
| Regarding if the gene codes a protein, UCKL1-AS1 is | nan | STEP 3 — ANSWER: Based on the NCBI Gene database results, UCKL1-AS1 is a **non-p | FAIL | PASS | The agent correctly identified that UCKL1-AS1 is a non-protein-coding gene that  |
| Regarding if the gene codes a protein, MIR6843 is | nan | STEP 3 — ANSWER: Based on the NCBI Gene database, MIR6843 is a microRNA gene (mi | FAIL | PASS | The agent correctly identifies that MIR6843 is a microRNA gene that does not cod |

### SNP location

| Question | Expected | Agent Output | Exact | Judge | Reason | 
|---|---|---|---|---|---|
| SNP rs1430464868 is located on human genome chromosome | chr13 | STEP 3 — ANSWER: SNP rs1430464868 is located on human genome chromosome **13**. | FAIL | PASS | The agent correctly identified that SNP rs1430464868 is located on chromosome 13 |
| SNP rs545148486 is located on human genome chromosome | chr16 | STEP 3 — ANSWER: SNP rs545148486 is located on human genome chromosome 16. | FAIL | PASS | The agent correctly identified that SNP rs545148486 is located on chromosome 16, |
| SNP rs895485955 is located on human genome chromosome | chr19 | STEP 3 — ANSWER: SNP rs895485955 is located on chromosome 19 of the human genome | FAIL | PASS | The agent correctly identified that SNP rs895485955 is located on chromosome 19, |
| SNP rs1376217783 is located on human genome chromosome | chr11 | STEP 3 — ANSWER: SNP rs1376217783 is located on human genome chromosome 11. | FAIL | PASS | The agent correctly identified that SNP rs1376217783 is located on chromosome 11 |
| SNP rs1420724913 is located on human genome chromosome | chr16 | STEP 3 — ANSWER: SNP rs1420724913 is located on human genome chromosome 16. | FAIL | PASS | The agent correctly identified that SNP rs1420724913 is located on chromosome 16 |
| SNP rs992486373 is located on human genome chromosome | chr15 | STEP 3 — ANSWER: SNP rs992486373 is located on chromosome 15 of the human genome | FAIL | PASS | The agent correctly identified that SNP rs992486373 is located on chromosome 15, |
| SNP rs975300764 is located on human genome chromosome | chr4 | STEP 3 — ANSWER: SNP rs975300764 is located on human genome chromosome 4. | FAIL | PASS | The agent correctly identified that SNP rs975300764 is located on chromosome 4,  |
| SNP rs993131098 is located on human genome chromosome | chr14 | STEP 3 — ANSWER: SNP rs993131098 is located on human genome chromosome 14. | FAIL | PASS | The agent correctly identified that SNP rs993131098 is located on chromosome 14, |
| SNP rs899883800 is located on human genome chromosome | chr1 | STEP 3 — ANSWER: SNP rs899883800 is located on human genome chromosome 1. | FAIL | PASS | The agent correctly identified that SNP rs899883800 is located on chromosome 1,  |
| SNP rs547832386 is located on human genome chromosome | chr15 | STEP 3 — ANSWER: SNP rs547832386 is located on chromosome 15 of the human genome | FAIL | PASS | The agent correctly identified that SNP rs547832386 is located on chromosome 15, |

### TF regulation

| Question | Expected | Agent Output | Exact | Judge | Reason | 
|---|---|---|---|---|---|
| The regulatory relationship between transcription factor ETV4 and gene | Repression | I need to classify this question first:  STEP 1 — CLASSIFY: This appears to be a | FAIL | FAIL | The agent states that ETV4 acts as a transcriptional activator of ERBB2, which d |
| The regulatory relationship between transcription factor USF1 and gene | Repression | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking about the regulatory rela | FAIL | FAIL | The agent states that USF1 acts as a positive transcriptional regulator of TERT, |
| The regulatory relationship between transcription factor MSC and gene  | Repression | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking about the regulatory rela | PASS |
| The regulatory relationship between transcription factor ZIC1 and gene | Activation | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking about the regulatory rela | FAIL | FAIL | The agent claims the regulatory relationship is not well-characterized and canno |
| The regulatory relationship between transcription factor HIF1A and gen | Repression | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking about the regulatory rela | FAIL | FAIL | The agent states that HIF1A positively regulates APEX1, which directly contradic |
| The regulatory relationship between transcription factor TP53 and gene | Activation | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking about the regulatory rela | FAIL | PASS | The agent correctly identifies that TP53 acts as a transcriptional activator of  |
| The regulatory relationship between transcription factor MYCN and gene | Repression | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking about the regulatory rela | PASS |
| The regulatory relationship between transcription factor BRCA1 and gen | Activation | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking about the regulatory rela | FAIL | FAIL | The agent states that BRCA1 negatively regulates (represses) FST expression, whi |
| The regulatory relationship between transcription factor SP2 and gene  | Activation | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking about the regulatory rela | FAIL | PASS | The agent correctly identifies that SP2 acts as a transcriptional activator of D |
| The regulatory relationship between transcription factor RELA and gene | Activation | STEP 1 — CLASSIFY: This is a KNOWLEDGE question asking about the regulatory rela | PASS |

---
*Generated by Bio-llm-agent-evals*