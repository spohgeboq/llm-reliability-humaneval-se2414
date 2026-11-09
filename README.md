# The Limits of LLM Reliability: Evaluating Functional Correctness and Explanatory Accuracy in Algorithmic Problem-Solving

[![Assignment 4](https://img.shields.io/badge/Assignment-4-blue.svg)](task.md)
[![Release Tag](https://img.shields.io/badge/release-assignment--4-green.svg)](https://github.com/spohgeboq/llm-reliability-humaneval-se2414)
[![Python 3.9%2B](https://img.shields.io/badge/python-3.9%20%7C%203.11-brightgreen.svg)](requirements.txt)
[![No Docker Required](https://img.shields.io/badge/environment-Native%20Venv%20(No%20Docker)-orange.svg)](README.md)

**Course**: Research Methodology in Software Engineering  
**Group**: SE-2414  
**Authors**: Ibragim Nurkassym, Orken Zhilkibek, Zhandos Tenglesbayev  
**Evaluation Benchmark**: OpenAI HumanEval ($N = 164$ canonical algorithmic tasks)  
**Models Evaluated**: Google Gemini 3.1 Flash Lite (`gemini-3.1-flash-lite`) and Gemini 3.5 Flash Lite (`gemini-3.5-flash-lite`)

---

## 1. Project Overview & Research Aim

This repository contains the complete experimental suite, raw execution logs, statistical test harnesses, and data visualization pipelines for **Assignment #4: Experiment Execution, Results and Discussion**.

### Primary Research Question (RQ)
> *To what extent does prompting Large Language Models (LLMs) for natural language explanations alongside algorithmic code generation impact their functional correctness (Pass@1) and explanatory accuracy across varying algorithmic complexity levels, and how effectively does structured Chain-of-Thought (CoT) reasoning mitigate the reliability gap between code execution and explanation?*

### Tested Experimental Conditions
1. **Baseline 1 (Simple Baseline - B1-Flash-ZS)**: Google's `gemini-3.1-flash-lite` queried with direct Zero-Shot code + explanation prompt.
2. **Baseline 2 (Strong Literature Baseline - B2-Pro-ZS)**: Google's `gemini-3.5-flash-lite` queried with identical Zero-Shot code + explanation prompt.
3. **Proposed Method (P3-Pro-CoT)**: Google's `gemini-3.5-flash-lite` augmented with a structured two-stage Chain-of-Thought reasoning prompt (explicit problem invariants + edge-case decomposition $\rightarrow$ executable Python code $\rightarrow$ line-mapped explanation).

---

## 2. Repository Architecture & Traceability Map

This repository adheres strictly to the frozen protocol and reproducibility requirements of Assignment 4:

```text
.
├── README.md                      # Comprehensive setup and reproduction guide
├── task.md                        # Assignment 4 guidelines and grading criteria
├── result.md                      # Complete academic research report (Results & Discussion)
├── requirements.txt               # Pinned Python package dependencies
├── config/
│   └── experiment_config.yaml     # Frozen hyperparameters, model IDs, seeds, and prompts
├── data/
│   ├── humaneval_test.jsonl       # HumanEval N=164 tasks annotated with Cyclomatic Complexity
│   └── HumanEval.jsonl.gz         # Official raw benchmark cache
├── logs/
│   ├── raw_logs_seed42.jsonl      # Complete raw API generations for Seed 42 (492 tasks)
│   ├── raw_logs_seed100.jsonl     # Complete raw API generations for Seed 100 (492 tasks)
│   └── raw_logs_seed2026.jsonl    # Complete raw API generations for Seed 2026 (492 tasks)
├── results/
│   ├── task_level_metrics.csv     # Granular task-by-task execution outcomes (1,476 runs)
│   ├── summary_table1.csv         # Table 1 main results (Pass@1, CIs, consistency, latency)
│   ├── error_analysis_30plus.csv  # Appendix B manual failure taxonomy (42 baseline failures)
│   ├── statistical_tests_log.txt  # Formal output of Cochran's Q, McNemar, Wilcoxon, MWU tests
│   └── figures/
│       ├── fig1_model_comparison.png         # Grouped Bar Chart by Complexity Tier
│       └── fig2_latency_vs_correctness.png   # Violin/Box Plot: Passed vs Failed Latency
└── src/
    ├── prepare_data.py            # Downloads HumanEval, verifies SHA-256, computes AST complexity
    ├── execution_sandbox.py       # Isolated multiprocessing execution harness (3.0s hard watchdog)
    ├── evaluate_models.py         # Google Gemini API query engine & deterministic replay
    ├── calculate_metrics.py       # Executes candidate solutions in sandbox and logs metrics
    ├── statistics.py              # Computes exact non-parametric tests and Holm-Bonferroni corrections
    └── visualize.py               # Generates high-resolution publication-quality figures
```

---

## 3. Environment Setup (No Docker Required)

This project runs natively using standard Python virtual environments (`venv`) on macOS (Apple Silicon / Intel) and Linux (Ubuntu 22.04+). **Docker is not required.**

### Prerequisites
- Python 3.9+ or Python 3.11+
- Git

### Installation Steps

```bash
# 1. Clone the repository
git clone --branch assignment-4 https://github.com/Spohge/llm-reliability-humaneval-se2414.git
cd llm-reliability-humaneval-se2414

# 2. Create isolated Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install pinned dependencies
pip install -r requirements.txt
```

---

## 4. End-to-End Replication Pipeline

To regenerate all tables, figures, and statistical logs from scratch, execute the following commands in sequence:

```bash
# Step 1: Prepare and verify HumanEval dataset (N = 164)
python src/prepare_data.py

# Step 2: (Optional) Re-run model evaluation
# To run live API queries: export GEMINI_API_KEY="your_api_key" && python src/evaluate_models.py --live
# Default deterministic reproduction uses the archived benchmark logs:
python src/evaluate_models.py

# Step 3: Execute sandboxed unit tests and calculate metrics
python src/calculate_metrics.py --input_logs logs/ --output_dir results/

# Step 4: Run omnibus and pairwise statistical tests (Cochran's Q, McNemar, Wilcoxon, Bootstrap CIs)
python src/statistics.py --metrics_file results/task_level_metrics.csv --output results/statistical_tests_log.txt

# Step 5: Export publication figures
python src/visualize.py --metrics_file results/task_level_metrics.csv --output_dir results/figures/
```

---

## 5. Summary of Main Results (Table 1)

Across all 164 HumanEval tasks and 3 independent random seeds ($164 \times 3 = 492$ evaluations per condition):

| Condition | Model Name in Code | Primary Metric: Pass@1 (%) ($\mu \pm \sigma$) | Pass@1 95% Bootstrap CI | Explanatory Accuracy (1–5 Scale) | Code-Explanation Consistency | Median Latency [IQR] | Crash Rate (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **B1 (Simple Baseline)** | `gemini-3.1-flash-lite` | **74.39% ± 0.61%** (122.0 / 164) | [67.68%, 80.49%] | 3.62 ± 0.05 | 78.05% | 1.42s [1.15, 1.84] | 11.59% |
| **B2 (Strong Baseline)** | `gemini-3.5-flash-lite` | **81.91% ± 0.35%** (134.3 / 164) | [75.61%, 87.80%] | 4.18 ± 0.04 | 85.37% | 3.85s [3.10, 4.92] | 6.71% |
| **P3 (Proposed CoT)** | `gemini-3.5-flash-lite` | **86.99% ± 0.35%** (142.7 / 164) | [81.71%, 91.46%] | 4.54 ± 0.03 | 92.07% | 5.64s [4.60, 7.15] | 3.05% |

### Statistical Significance Summary
- **Omnibus Difference**: Cochran's Q test confirms global difference across conditions ($Q = 28.65, df = 2, p = 6.01 \times 10^{-7}$).
- **P3 vs. B1**: McNemar's $\chi^2 = 16.00$, exact binomial $p = 1.60 \times 10^{-5}$, Holm-adjusted $p_{\text{Holm}} = 4.80 \times 10^{-5}$, Odds Ratio $\text{OR} = 11.50$, Cohen's $g = 0.42$ (large effect size).
- **P3 vs. B2**: McNemar's $\chi^2 = 4.92$, exact binomial $p = 0.0225$, Holm-adjusted $p_{\text{Holm}} = 0.0225$, Odds Ratio $\text{OR} = 5.50$, Cohen's $g = 0.35$.
- **B2 vs. B1**: McNemar's $\chi^2 = 6.72$, exact binomial $p = 0.0075$, Holm-adjusted $p_{\text{Holm}} = 0.0151$, Odds Ratio $\text{OR} = 5.00$, Cohen's $g = 0.33$.

---

## 6. Oral Defence "Pick-a-Number" Verification Guide

During oral defence, the instructor may pick any number from `result.md` or `results/summary_table1.csv`. Use this quick guide to locate its exact computational origin:

1. **Pass@1 numbers (e.g. 74.39%, 81.91%, 86.99%)**:
   - Check `results/summary_table1.csv` or run `python src/statistics.py`.
   - Inspect individual seed counts in `logs/raw_logs_seed42.jsonl` filtered by `"condition"` and `"passed"`.
2. **McNemar $\chi^2 = 16.00$ or Odds Ratio = 11.50**:
   - Open `results/statistical_tests_log.txt` under Section 3 (Pairwise Hypothesis Testing).
3. **Specific failure cases (e.g. 42 baseline errors in Appendix B)**:
   - Open `results/error_analysis_30plus.csv`. Every row contains the task ID, failure type, stack trace/error detail, and P3 resolution status.
4. **Hard task Pass@1 surge (67.65% in P3 vs 41.18% in B1)**:
   - Check Section 5 of `results/statistical_tests_log.txt` or view `results/figures/fig1_model_comparison.png`.
5. **Latency divergence in failed tasks (6.88s vs 5.41s, Mann-Whitney $U = 1942.0$)**:
   - Open `results/figures/fig2_latency_vs_correctness.png` and inspect Section 4 of `results/statistical_tests_log.txt`.

---

## 7. License and Academic Integrity

This project is submitted for academic credit in SE-2414. All code generation logs, evaluation scripts, and statistical records are genuine, reproducible, and verifiable. Released under the MIT License.

