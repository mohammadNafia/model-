# How to Run This Project

This document outlines the steps to configure your environment, run the CLI tool, and classify ECG signals.

## 1. Prerequisites
Ensure you have the following installed on your system:
- **Python 3.8+** (64-bit recommended)
- **pip** (Python package installer)

## 2. Installation
Open your terminal (Command Prompt, PowerShell, or bash), navigate to the project folder (`C:\Users\Administrator\Desktop\حلا الربه`), and install the required dependencies:

```cmd
pip install -r requirements.txt
```
*(This will install `torch`, `numpy`, `pandas`, `huggingface_hub`, and `scikit-learn`)*

---

## 3. Usage Guide

The CLI application is operated entirely through the `main.py` file. It requires exactly one of the two following input arguments:

### Option A: Manual Entry (`--manual`)
If you want to quickly test an array of ECG readings, you can supply them directly as a comma-separated string in quotes.

**Command:**
```cmd
python main.py --manual "0.12,0.18,0.25,0.10,-0.05,0.02"
```

### Option B: CSV File Entry (`--csv`)
If you have a dataset saved in a CSV format (a single row or column of signal values), you can pass the file path.

**Command:**
```cmd
python main.py --csv sample_ecg.csv
```

---

## 4. Expected Output

On your first run, the script will automatically download the necessary model weights and configuration files from Hugging Face. Subsequent runs will use the cached files and be much faster.

The terminal will print the inference sequence and display the final diagnosis. 

**Example Output (Normal):**
```text
Downloading/Loading model files from Hugging Face...

Running inference...

--- Results ---
Predicted class  : N
Confidence score : 0.9921

Final Status: Normal ECG
```

**Example Output (Abnormal):**
```text
Downloading/Loading model files from Hugging Face...

Running inference...

--- Results ---
Predicted class  : V
Confidence score : 0.9654

Final Status: Abnormal ECG
Detected class: V
```

## Troubleshooting
- **ModuleNotFoundError**: Make sure you ran `pip install -r requirements.txt` and are using the correct Python environment.
- **Direct model loading failed / Error Loading Model**: This occurs if the fallback wrapper cannot perfectly map the Hugging Face weights. Ensure `model_wrapper.py` is in the same directory as `main.py`.
