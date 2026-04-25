# How to Run This Project

This document outlines the steps to configure your environment, run the CLI tool, and classify ECG signals.

## 1. Prerequisites
Ensure you have the following installed on your system:
- **Python 3.8+** (64-bit recommended)
- **pip** (Python package installer)

## 2. Installation
Open your terminal (Command Prompt, PowerShell, or bash), navigate to the project folder, and install the required dependencies:

```cmd
pip install -r requirements.txt
```
*(This will install `torch`, `numpy`, `pandas`, `huggingface_hub`, `scikit-learn`, and `kaggle`)*

---

## 3. Usage Guide

The CLI application is operated through the `main.py` file. It supports three input methods:

### Option A: MIT-BIH Dataset Row (`--row`)
Use this to test a specific heartbeat from the MIT-BIH dataset. The script will automatically download and extract the dataset from Kaggle if needed.

**Command:**
```cmd
python main.py --row 0
```

### Option B: Manual Entry (`--manual`)
If you want to quickly test an array of ECG readings, you can supply them directly as a comma-separated string in quotes.

**Command:**
```cmd
python main.py --manual "0.12,0.18,0.25,0.10,-0.05,0.02"
```

### Option C: CSV File Entry (`--csv`)
If you have a dataset saved in a CSV format (a single row or column of signal values), you can pass the file path.

**Command:**
```cmd
python main.py --csv sample_ecg.csv
```

---

## 4. Expected Output

On your first run, the script will automatically download the necessary model weights and configuration files from Hugging Face. If using `--row`, it will also set up the Kaggle dataset.

The terminal will print the inference sequence and display the final diagnosis.

**Example Output (Normal):**
```text
Downloading/Loading model files from Hugging Face...

Running inference...

========================================
        CLASSIFICATION RESULTS
========================================
Predicted Class  : N
Predicted Status : Normal ECG
========================================
```

**Example Output (Abnormal):**
```text
Downloading/Loading model files from Hugging Face...

Running inference...

========================================
        CLASSIFICATION RESULTS
========================================
Predicted Class  : V
Predicted Status : Abnormal ECG
========================================
```

## Troubleshooting
- **Kaggle API Credentials**: If using `--row`, ensure your `kaggle.json` is placed in `~/.kaggle/`.
- **ModuleNotFoundError**: Make sure you ran `pip install -r requirements.txt`.
- **Direct model loading failed**: This is normal; the script uses a fallback wrapper to load the weights correctly.
