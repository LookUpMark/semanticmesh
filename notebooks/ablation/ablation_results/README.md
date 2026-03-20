# Ablation Results Layout

This folder stores outputs from ablation experiments.

## Structure

- `meta/`: global state and cross-study summaries.
- `studies/<STUDY_ID>/`: all artifacts for one study (for example AB-00).

Each study should keep files in these subfolders:

- `runs/`: raw run payloads and logs.
- `traces/`: query and RAGAS traces.
- `diagnostics/`: diagnostics JSON files.
- `analyses/`: iterative sample-by-sample analyses and low-score analysis.
- `reports/`: reliability and audit reports.
- `baselines/`: baseline snapshots used for comparisons.
