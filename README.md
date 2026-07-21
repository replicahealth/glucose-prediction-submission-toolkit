# Glucose Prediction Submission ToolKit

This repository contains the evaluation script for the MetaboNet-Glucose prediction benchmark. 

[🏆 View Leaderboard 🏆](https://huggingface.co/spaces/MetabonetBench/leaderboard-space)

## Installation

> ⚠️ **Read this first — this repo uses [Git LFS](https://git-lfs.com) for the parquet files in `data/`.**
> If you clone without Git LFS installed, you will get tiny pointer files (a few hundred bytes) instead of the actual data, and `run.py` will not work.

### Step 1 — Install Git LFS (once per machine)

Install the Git LFS client:

- **macOS:** `brew install git-lfs`
- **Ubuntu / Debian:** `sudo apt-get install git-lfs`
- **Windows / other:** download from [git-lfs.com](https://git-lfs.com)

Then register it with your Git install (only needed once per machine):

```bash
git lfs install
```

### Step 2 — Clone the repo

With LFS installed, a normal `git clone` will automatically download the real parquet files:

```bash
git clone https://github.com/replicahealth/glucose-prediction-submission-toolkit.git
cd glucose-prediction-submission-toolkit
```

**Sanity check:** `ls -lh data/` should show `template.parquet` at ~19 MB and `targets.parquet` at ~33 MB. If they're only a few hundred bytes, you got pointer files — see "Already cloned without LFS?" below.

### Step 3 — Install Python dependencies

```bash
uv venv .env
source .env/bin/activate  # On Windows: .env\Scripts\activate
uv pip install -r requirements.txt
```

### Already cloned without LFS?

Don't re-clone. Install Git LFS as in Step 1, then from inside the repo run:

```bash
git lfs install
git lfs pull
```

This replaces the pointer files with the actual parquet contents in place.


## Quick Start

The steps below are for submitting to the **live leaderboard**. Steps for the **annual competition** will be added soon.

1. **Generate and format predictions**: Use your model to create predictions for the MetaboNet test set, then save them as a parquet file. Each row must include:
   - `pred_30`: 30-minute ahead glucose prediction
   - `pred_60`: 60-minute ahead glucose prediction
   - `pred_90`: 90-minute ahead glucose prediction
   - `pred_120`: 120-minute ahead glucose prediction

   The file must:
   - Be in parquet format
   - Have the exact same rows and columns as `data/template.parquet` (same `id`, `source_file`, and `date` combinations)
   - Keep rows in the same order as the template
   - Include all four prediction columns (`pred_30`, `pred_60`, `pred_90`, `pred_120`)
   - Fully populate **at least one** prediction column. You can compete on a single horizon or any subset. Each populated column must contain no missing values, and any horizons you skip must be left **entirely empty** (all NaN). Partially filled columns are rejected.

   For details on what's in `data/` and how the test set was built, see [`data/README.md`](data/README.md).

   **Preview of submission format:**

   | id | source_file | date                | pred_30 | pred_60 | pred_90 | pred_120 |
   |----|-------------|---------------------|---------|---------|---------|----------|
   | 16 | AZT1D       | 2024-01-18 01:00:00 | NaN     | NaN     | NaN     | NaN      |
   | 16 | AZT1D       | 2024-01-18 01:05:00 | NaN     | NaN     | NaN     | NaN      |
   | 16 | AZT1D       | 2024-01-18 01:10:00 | NaN     | NaN     | NaN     | NaN      |
   | 16 | AZT1D       | 2024-01-18 01:15:00 | NaN     | NaN     | NaN     | NaN      |
   | 16 | AZT1D       | 2024-01-18 01:20:00 | NaN     | NaN     | NaN     | NaN      |

2. **Validate and evaluate**:
   ```bash
   python run.py your_predictions.parquet        # Default: 60-minute horizon
   python run.py your_predictions.parquet 30     # Evaluate 30-minute horizon only
   python run.py your_predictions.parquet all    # Evaluate all horizons + overall (all horizons combined)
   ```
   
   Available horizon options: `30`, `60`, `90`, `120`, or `all` (defaults to `60`)

   Example output:
   ```
   🔍 Loading files...
   ✅ Files loaded successfully

   📋 Validating format...
   ✅ Format validation passed!

   📊 Calculating metrics for horizon: 60...

   ============================================================
                       EVALUATION RESULTS
   ============================================================

   📈 60 Min Ahead Predictions:
      RMSE: 57.24 mg/dL
      MAE:  44.28 mg/dL

      DTS Error Grid Zones:
      • Zone A (Clinically Accurate):     37.5%
      • Zone B (Benign Errors):           49.8%
      • Zone C (Overcorrection):          11.6%
      • Zone D (Failure to Detect):       1.1%
      • Zone E (Erroneous Treatment):     0.0%

   ============================================================

   ✅ Format is valid! You are ready to submit!
   🚀 Submit your predictions at:
      https://huggingface.co/spaces/MetabonetBench/leaderboard-space

   ============================================================
   ```

3. **Submit**: Once validation passes, submit your predictions at:
https://huggingface.co/spaces/MetabonetBench/leaderboard-space




## Files

- `run.py` - Validation and evaluation script
- `inspect_data.py` - Helper to print the format of `data/template.parquet` and `data/targets.parquet`
- `metrics.py` - Metric calculation functions (RMSE, MAE, DTS Error Grid)
- `data/template.parquet` - Template showing required format for submissions
- `data/targets.parquet` - Ground truth values for evaluation


