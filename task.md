Assignment #4. Experiment Execution, Results and Discussion
Student(s): Write full name(s)
Group: Write your group
Objective: This assignment turns the methodology and initial implementation from Assignment 3 into a completed study. Students freeze the experimental protocol, run the full experiment, evaluation, or analysis, report the results honestly with appropriate statistical evidence, explain why the results occur, and interpret them in relation to previous research. Together with Assignments 1-3, this assignment produces the Results and Discussion sections of the final research manuscript.
By the end of this assignment, students should be able to:
•	Freeze the key experimental decisions before final results are obtained
•	Execute a fair comparison against appropriate baselines or comparison conditions
•	Report results with variability, uncertainty, and appropriate statistical evidence
•	Use ablation, sensitivity, subgroup, or error analysis to explain why the results occur
•	State clearly whether each hypothesis is supported and how the evidence answers the research question
•	Interpret the findings in relation to previous studies and identify threats to validity
•	Package code, data access instructions, and settings so that another person can reproduce the main results
•	Defend every reported number, comparison, and conclusion during the oral defence
Rules for Submission:
1. The assignment is completed individually or in the same team of no more than two students used for Assignments 1-3. Both members are responsible for the complete work.
2. The research question, aim, objectives, and design from Assignments 2-3 must remain. Any change must be approved by the instructor and reported in the section "Deviations from the frozen protocol".
3. Do NOT invent, adjust, or selectively remove results, runs, participants, data points, or failed experiments. Report every planned run, including unfavourable ones. Fabrication or falsification of results is a serious violation of academic integrity.
4. Negative, mixed, or unexpected results are fully acceptable. The grade depends on the rigour, fairness, and honesty of the study, not on whether your method "wins".
5. The test set (or final evaluation data) must not be used for model selection, hyperparameter tuning, prompt engineering, threshold selection, or feature selection. All development decisions use the training/validation data only.
6. Human-participant data may be collected only with informed consent and the required ethical approval. Important for publication: data collected without prior ethical approval may be acceptable for course assessment but usually cannot be used in a journal article.
7. Every number reported in the text, tables, and figures must be traceable to a log file, notebook output, or results file in the repository.
8. AI tools may be used only according to the course rules. Students remain responsible for every result and interpretation and must verify all AI-assisted content.
9. Each student defends the complete assignment individually. In team submissions, the instructor may ask either student about any part of the work.
You must submit:
•	Experiment Protocol Freeze form (Appendix A) uploaded to Moodle BEFORE the final experiments start, by the deadline set by the instructor. The upload timestamp is part of the evidence.
•	Main report: Assignment4_YourFullName.docx or Assignment4_Surname1_Surname2.docx
•	Results and Discussion sections: approximately 1,800-2,500 words, excluding tables, figures, references, and appendices
•	Repository link (GitHub/GitLab) with a tagged release named "assignment-4"
•	Raw result logs/files for every reported number
•	Appendix: error analysis table, reproduction test record, additional tables and figures
Part 1: Experiment Protocol Freeze (before the final runs)
Goal: Fix the key decisions before you see the final results, so that the results cannot be shaped after the fact. Complete Appendix A and upload it before running the final experiments.
1. Restate the final hypotheses or expected comparisons.
2. Name ONE primary outcome/metric and a small number of secondary metrics, and justify the primary metric (for example macro-F1 instead of accuracy for imbalanced classes).
3. List all baselines or comparison conditions.
4. Fix the final dataset version and the test set (number of items and, where possible, a file hash).
5. State the number of runs, random seeds, folds, trials, or participants.
6. State the statistical analysis you will use (see Table 2).
7. Write what result would support and what result would NOT support each hypothesis.
Any later change is allowed only if it is reported, with reasons, in "Deviations from the frozen protocol". Undeclared changes are treated as a quality problem in grading.
Questions for defence:
Q1. Show your frozen protocol. Which decisions did you fix before running the experiments?
Q2. Why did you choose this primary metric?
Q3. Did you deviate from the protocol? Why?
Part 2: Final Experimental Setup
Goal: Describe the final setup precisely enough that another researcher could repeat the study.
1. Data: source, version, size, splits, class/group distribution, and any changes since Assignment 3.
2. Comparison conditions: at least TWO baselines: (a) a simple baseline (majority class, rule-based method, random, keyword search, existing system, or no intervention), and (b) a strong or commonly used method from the literature. For software/system studies, use an existing solution, previous version, or alternative architecture.
3. Proposed method/condition and its final configuration.
4. Fairness: same data, same preprocessing, comparable tuning effort, and the same hardware/time limits for all compared conditions.
5. Implementation details: hardware, software and library versions, hyperparameters, prompts/configuration files, seeds, and run time.
Recommended length: 250-350 words plus one setup table.
Part 3: Main Results
Goal: Report what happened objectively. Interpretation belongs to Part 6.
1. Main results table: every condition x primary and secondary metrics.
2. Variability: report mean +/- standard deviation over at least 3 runs/seeds or k-fold cross-validation. For a single deterministic run, report a 95% confidence interval (for example by bootstrap).
3. Statistical comparison using an appropriate test from Table 2. Report the test, statistic, p-value, and correction for multiple comparisons when several comparisons are made.
4. Practical significance: report the absolute difference and/or an effect size, not only p-values.
5. At least TWO informative figures (for example comparison chart, confusion matrix, learning curve, latency distribution, or ROC/PR curve).
Recommended length: 400-600 words plus tables and figures.
Table 2. Statistical reporting guide
Situation	Recommended reporting / test
Two models evaluated on the same test items (correct/incorrect per item)	McNemar test or paired bootstrap confidence interval
Two methods, several runs/seeds or CV folds	Mean +/- SD; paired t-test or Wilcoxon signed-rank test on paired runs/folds
More than two methods compared	Friedman test with post-hoc test, or pairwise tests with Holm correction
Continuous per-item measure (latency, error size, time)	Median and IQR; Wilcoxon or Mann-Whitney test; confidence interval
Two independent groups of participants	t-test or Mann-Whitney test; effect size (Cohen's d or r)
Pre-test / post-test on the same participants	Paired t-test or Wilcoxon signed-rank test; effect size
Categorical survey responses	Frequencies and percentages; chi-square or Fisher's exact test
Multi-item questionnaire scale	Internal consistency (Cronbach's alpha) before analysing the scale score
Qualitative data	Coding scheme, inter-coder agreement (Cohen's kappa) on a subsample, theme table with anonymised quotes
Small samples: if the sample is too small for reliable inference, label the analysis as exploratory and do not claim statistical significance.
Questions for defence:
Q1. What is your main result in one sentence, with numbers?
Q2. Which statistical test did you use and why is it appropriate?
Q3. Is the difference practically meaningful, not only statistically significant?
Part 4: Additional Analysis - Why Does It Work (or Not)?
Goal: Go beyond "method A is better than method B" and explain the result. Error analysis is required for every project where errors can be identified. Choose at least ONE more analysis.
•	Error analysis (required): manually categorise at least 30 failed cases (or all failures if there are fewer) into error types; report counts and give examples (Appendix B).
•	Ablation: remove or replace one component at a time and measure the change.
•	Sensitivity analysis: vary one key factor (data size, threshold, top-k, prompt, load level, noise).
•	Subgroup analysis: results per class, language, difficulty level, device, user group, or data source.
•	Efficiency/cost analysis: training/inference time, memory, latency, energy, or cost per request.
Recommended length: 300-450 words plus one table or figure.
Part 5: Answering the Research Question and Hypotheses
Goal: Connect the evidence directly to the research question.
Hypothesis / Objective	Evidence (table/figure)	Result in numbers	Supported / Partly / Not supported
             
             
             
Then write a direct answer to the primary research question (100-150 words). Do not claim more than the evidence shows.
Part 6: Discussion
Goal: Interpret the findings and position them in the research field.
1. Interpret the main findings: what happened and why, using evidence from Part 4.
2. Compare your results with at least THREE studies from your Assignment 1 literature review: where do you agree or disagree, and what could explain the difference (data, setting, language, metric, model version)?
3. Explain unexpected or negative results.
4. Practical implications: who can use these findings and how.
5. Threats to validity: internal validity, external validity (generalisability), construct validity (do the metrics measure what you claim?), and statistical conclusion validity/reproducibility.
6. Specific limitations and specific future work.
Avoid overclaiming: conclusions apply only to the tested data, conditions, and settings. Recommended length: 600-900 words.
Questions for defence:
Q1. How do your results compare with one study from your literature review?
Q2. What is the most serious threat to the validity of your results?
Q3. What would you change if you repeated the study?
Part 7: Reproducibility Package
Goal: Another person must be able to reproduce your main results table.
•	Repository with README: purpose, structure, installation, and exact commands to reproduce the main results
•	Environment file with versions (requirements.txt, environment.yml, Dockerfile, or equivalent)
•	Scripts/notebooks that regenerate the main results table and figures, configuration files, and seeds
•	Raw result logs; data or clear data-access instructions if the licence does not allow sharing
•	Licence file and tagged release "assignment-4"
•	Reproduction test: the other team member (or, for individual work, a classmate) runs the main experiment from the README in a clean environment and records the outcome in Appendix C
Never upload personal data, passwords, API keys, tokens, or confidential company data.
Part 8: Track-Specific Minimum Evidence
Project Track	Minimum Evidence for Assignment 4
Machine Learning / Deep Learning / AI Model	At least 2 baselines; at least 3 seeds or k-fold CV; untouched test set; metrics suitable for the data (e.g. macro-F1, PR-AUC for imbalance); confusion matrix; error analysis; ablation or sensitivity analysis; statistical comparison.
Software / Information System / Mobile or Web Application	Core features needed for the RQ implemented; test plan; functional test pass rate; at least one quantitative evaluation aligned with the RQ (e.g. latency p50/p95 and throughput under load, security test results, or usability with an approved participant study); comparison with an existing solution, previous version, or alternative design; logs.
Data Analytics / Statistical / Decision-Support Project	Complete pipeline from raw data to results; assumption checks for the chosen tests/models; diagnostics; at least one robustness check (alternative specification, subset, or method); interpretable output.
Computer Vision / NLP / Algorithmic Project	Full test set; at least 2 baselines; per-class/per-language/per-difficulty results; success and failure examples; runtime; statistical comparison; error analysis.
IoT / Robotics / Embedded / Sensor-Based Project	Repeated trials (at least 10 per condition) under documented conditions; accuracy/latency/energy/reliability measures; comparison condition; environmental conditions logged; failure cases.
Cybersecurity / Networks / Optimisation / Other Technical Experiment	Defined threat model or scenarios; baseline configuration; repeated runs; measures such as detection rate and false-positive rate, or throughput/latency/cost; statistical comparison; reproducible configuration.
Human-Participant Component (only with approval)	Approved instrument and consent procedure; response rate; scale reliability; appropriate test with effect size; anonymised data; clear statement of how this evidence complements the technical results.
Results Reporting Self-Check
•	Every number in the text matches the tables and the result logs
•	Baselines received comparable tuning effort and were run on the same data
•	The test set was not used for any development decision
•	Variability or confidence intervals are reported, not single best runs
•	All planned runs are reported, including unfavourable ones
•	Each hypothesis is marked as supported, partly supported, or not supported
•	Claims in the Discussion do not go beyond the evidence
•	Figures have readable labels, units, and self-explanatory captions
Final Submission Structure:
1. Final / Revised Research Title
2. Primary Research Question, Aim, Objectives, and Hypotheses
3. Deviations from the Frozen Protocol
4. Final Experimental Setup
5. Main Results
6. Additional Analysis (Error Analysis + one more)
7. Answering the Research Question and Hypotheses
8. Discussion (including Threats to Validity and Limitations)
9. Reproducibility Statement and Repository Link
10. References
11. Appendices A-C
Individual Oral Defence
Each student defends Assignment 4 individually, even if the report was completed in a team. Recommended defence time: 5-7 minutes. The instructor may open any part of the report, repository, or logs.
"Pick-a-number" check: the instructor selects any number from your results table, and the student must show the log, notebook output, or script that produced it.
Evaluation Criteria:
A. Written Submission - 10 points (50%)
1. Protocol Freeze and Experimental Setup - 2 points. Protocol submitted before the final runs; baselines are appropriate and fair; setup is reproducible; deviations are declared.
2. Main Results and Statistical Evidence - 2 points. Complete results table; variability or confidence intervals; appropriate statistical test; effect size or practical difference; informative figures.
3. Additional Analysis - 2 points. Error analysis plus at least one ablation, sensitivity, subgroup, or efficiency analysis that genuinely explains the results.
4. Answer to the RQ and Discussion - 2 points. Hypotheses evaluated honestly; comparison with at least three prior studies; threats to validity and limitations; no overclaiming.
5. Reproducibility, Integrity, and Presentation - 2 points. Working repository with README, environment, logs, tagged release, reproduction test record; academic writing and references.
B. Individual Oral Defence - 10 points (50%)
Question 1 - Protocol and setup: explain the frozen decisions and why the baselines are fair.
Question 2 - Main result: state the main result with numbers and explain the statistical test.
Question 3 - Explanation: explain one error type, ablation, or sensitivity result.
Question 4 - Interpretation: compare one result with a prior study and name one threat to validity.
Question 5 - Pick-a-number check: show the source of one number chosen by the instructor.
Defence scoring for each question:
•	2 points - clear, accurate, independent explanation using specific details from the submitted work; can answer a follow-up question
•	1 point - partial/general explanation; needs prompting or shows a minor misunderstanding
•	0 points - cannot explain the submitted work, gives an incorrect/contradictory answer, or only repeats text
Important grading rules: A complete written submission can receive up to 10/20; the remaining 10 points are earned only through the individual oral defence. A number that cannot be traced to a log or output receives no credit in the related criterion. Fabricated or falsified results are handled under the university academic integrity policy.
Total: 20 points | Written submission:  points (20%) | Individual oral defence:  points (80%)
Appendix A. Experiment Protocol Freeze Form
Upload before running the final experiments. Date and time of upload: ____________
Item	Your decision
Primary research question	 
Hypotheses / expected comparisons	 
Primary outcome / metric and justification	 
Secondary metrics	 
Baseline 1 (simple)	 
Baseline 2 (strong / literature)	 
Proposed method / condition	 
Final dataset version, size, and test-set identifier (count / hash)	 
Number of runs, seeds, folds, trials, or participants	 
Statistical test(s) and multiple-comparison correction	 
Result that would SUPPORT each hypothesis	 
Result that would NOT support each hypothesis	 
Planned additional analyses (error analysis + ...)	 
Appendix B. Error Analysis Table
Error type	Definition	Count	% of errors	Example (anonymised)	Possible cause
                     
                     
                     
Appendix C. Reproduction Test Record
Item	Record
Person who reproduced the results	 
Date, machine, operating system	 
Commit / release tag used	 
Commands executed	 
Did the main results table reproduce? (Yes / Partly / No)	 
Differences observed and explanation	 
Problems in the README fixed after the test	 

