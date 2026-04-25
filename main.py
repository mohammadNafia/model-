import argparse
import json
import os
import pickle
import sys
import zipfile
import subprocess
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from huggingface_hub import hf_hub_download
from sklearn.preprocessing import StandardScaler

# Import the fallback model wrapper
try:
    from model_wrapper import ECGModel
except ImportError:
    ECGModel = None

# --- Constants ---
MODEL_REPO = "dheerajthuvara/ecg-arrhythmia-detection"
KAGGLE_DATASET = "shayanfazeli/heartbeat"
TEST_FILE = "mitbih_test.csv"
LOW_CONF_THRESHOLD = 0.60

# MIT-BIH numeric label to status mapping
# 0 = N (Normal), 1 = S, 2 = V, 3 = F, 4 = Q (Abnormal)
LABEL_STATUS_MAP = {
    0: ("N", "Normal ECG"),
    1: ("S", "Abnormal ECG"),
    2: ("V", "Abnormal ECG"),
    3: ("F", "Abnormal ECG"),
    4: ("Q", "Abnormal ECG")
}

def download_and_extract_dataset():
    """Download the heartbeat dataset from Kaggle and unzip it."""
    if not os.path.exists(TEST_FILE):
        print(f"Dataset {TEST_FILE} not found. Downloading from Kaggle...")
        try:
            # Check if kaggle.json exists
            kaggle_path = os.path.expanduser("~/.kaggle/kaggle.json")
            if not os.path.exists(kaggle_path) and "KAGGLE_USERNAME" not in os.environ:
                print("\n[Error] Kaggle API credentials not found.")
                print("Please place your 'kaggle.json' in '~/.kaggle/' or set KAGGLE_USERNAME and KAGGLE_KEY environment variables.")
                sys.exit(1)

            # Download using CLI command
            subprocess.run(["kaggle", "datasets", "download", "-d", KAGGLE_DATASET], check=True)
            
            # Unzip
            zip_file = "heartbeat.zip"
            if os.path.exists(zip_file):
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(".")
                os.remove(zip_file)
                print("Dataset downloaded and extracted successfully.")
            else:
                print("[Error] Downloaded file heartbeat.zip not found.")
                sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"[Error] Failed to download dataset via Kaggle CLI: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"[Error] An error occurred during dataset setup: {e}")
            sys.exit(1)
    else:
        print(f"Dataset {TEST_FILE} already exists.")

def download_model_files():
    """Download required model files from Hugging Face Hub."""
    print("Downloading/Loading model files from Hugging Face...")
    try:
        config_path = hf_hub_download(repo_id=MODEL_REPO, filename="models/model_config.json")
        encoder_path = hf_hub_download(repo_id=MODEL_REPO, filename="models/label_encoder.pkl")
        model_path = hf_hub_download(repo_id=MODEL_REPO, filename="models/best_model.pt")
        return config_path, encoder_path, model_path
    except Exception as e:
        print(f"Error downloading files from Hugging Face: {e}")
        sys.exit(1)

def preprocess_ecg(signal, window_size):
    """
    Preprocess the ECG signal:
    1. Convert to numpy float32
    2. Pad/Trim to match window_size
    3. Z-score normalize
    4. Reshape to (1, 1, window_size)
    """
    signal = np.array(signal, dtype=np.float32)
    actual_len = len(signal)
    
    if actual_len > window_size:
        signal = signal[:window_size]
        print(f"  [Preprocess] Signal trimmed from {actual_len} to {window_size} samples.")
    elif actual_len < window_size:
        padding = window_size - actual_len
        signal = np.pad(signal, (0, padding), 'constant', constant_values=0)
        print(f"  [Preprocess] Signal padded from {actual_len} to {window_size} samples.")
        
    # Z-score normalization
    scaler = StandardScaler()
    signal = scaler.fit_transform(signal.reshape(-1, 1)).flatten()
    
    # Reshape for PyTorch: (batch, channels, length)
    signal = signal.reshape(1, 1, window_size)
    return torch.tensor(signal, dtype=torch.float32)

def load_model(model_path, config_path):
    """Load model with fallback to wrapper."""
    with open(config_path, "r") as f:
        config = json.load(f)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    try:
        # Attempt direct load
        model = torch.load(model_path, map_location=device, weights_only=False)
        model.eval()
        print("  Model loaded successfully as full object.")
        return model
    except Exception as e:
        print(f"  [Warning] Direct load failed: {e}. Falling back to state_dict load.")
        
        if ECGModel is None:
            print("  [Error] model_wrapper.py missing. Aborting.")
            sys.exit(1)
            
        model = ECGModel(config)
        state_dict = torch.load(model_path, map_location=device, weights_only=False)
        
        # Extract state_dict if object was loaded
        if isinstance(state_dict, torch.nn.Module):
            state_dict = state_dict.state_dict()
            
        # Report keys
        keys_result = model.load_state_dict(state_dict, strict=False)
        if keys_result.missing_keys:
            print(f"  Missing keys: {len(keys_result.missing_keys)}")
        if keys_result.unexpected_keys:
            print(f"  Unexpected keys: {len(keys_result.unexpected_keys)}")
            
        # Check mismatch ratio
        missing_ratio = len(keys_result.missing_keys) / len(model.state_dict())
        if missing_ratio > 0.3:
            print(f"  [Error] Too many missing keys ({missing_ratio:.1%}). Wrapper architecture mismatch.")
            sys.exit(1)
            
        model.to(device)
        model.eval()
        print("  Fallback model loaded successfully.")
        return model

def main():
    parser = argparse.ArgumentParser(description="ECG Arrhythmia Classification CLI")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--row", type=int, help="Row index from mitbih_test.csv to process")
    group.add_argument("--manual", type=str, help="Comma-separated ECG signal values")
    group.add_argument("--csv", type=str, help="Path to CSV file containing ECG signal values")
    
    args = parser.parse_args()

    # 1. Handle Input Source
    true_label_numeric = None
    true_class_char = "N/A"
    true_status = "Unknown"
    
    if args.row is not None:
        # Download Dataset if needed
        download_and_extract_dataset()
        try:
            df = pd.read_csv(TEST_FILE, header=None)
            if args.row >= len(df):
                print(f"[Error] Row index {args.row} is out of bounds (Max: {len(df)-1}).")
                sys.exit(1)
            
            row_data = df.iloc[args.row].values
            ecg_signal = row_data[:187]
            true_label_numeric = int(row_data[187])
            true_class_char, true_status = LABEL_STATUS_MAP.get(true_label_numeric, ("Unknown", "Unknown"))
        except Exception as e:
            print(f"[Error] Failed to read row {args.row}: {e}")
            sys.exit(1)
            
    elif args.manual:
        try:
            ecg_signal = [float(x.strip()) for x in args.manual.split(",")]
        except ValueError:
            print("Error: --manual input must be comma-separated numbers.")
            sys.exit(1)
            
    elif args.csv:
        if not os.path.isfile(args.csv):
            print(f"Error: CSV file '{args.csv}' not found.")
            sys.exit(1)
        try:
            df = pd.read_csv(args.csv, header=None)
            ecg_signal = df.values.flatten().tolist()
            if not ecg_signal:
                raise ValueError("CSV is empty.")
        except Exception as e:
            print(f"Error reading CSV format: {e}")
            sys.exit(1)

    # 2. Download Model
    config_path, encoder_path, model_path = download_model_files()
    with open(config_path, "r") as f:
        config = json.load(f)
    window_size = config.get("window_size", 187)

    # 3. Preprocess
    print("\nPreprocessing signal...")
    input_tensor = preprocess_ecg(ecg_signal, window_size)

    # 4. Load Model & Label Encoder
    model = load_model(model_path, config_path)
    try:
        with open(encoder_path, "rb") as f:
            label_encoder = pickle.load(f)
    except:
        label_encoder = None

    # 5. Inference
    print("Running inference...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    input_tensor = input_tensor.to(device)
    
    with torch.no_grad():
        outputs = model(input_tensor)
        probs = F.softmax(outputs, dim=1)
        confidence, pred_idx = torch.max(probs, 1)

    # 6. Map Results
    conf_score = confidence.item()
    
    # Predicted class name
    if label_encoder:
        try:
            pred_class = label_encoder.inverse_transform([pred_idx.item()])[0]
        except:
            pred_class = f"Class_{pred_idx.item()}"
    else:
        pred_class = f"Class_{pred_idx.item()}"

    # Status mapping
    pred_status = "Normal ECG" if pred_class == "N" else "Abnormal ECG"
    
    # Correct/Wrong
    is_correct = "N/A"
    if true_status != "Unknown":
        is_correct = "Correct" if pred_status == true_status else "Wrong"

    # 7. Print Output
    print("\n" + "="*40)
    print("        CLASSIFICATION RESULTS")
    print("="*40)
    print(f"Predicted Class  : {pred_class}")
    
    if conf_score < LOW_CONF_THRESHOLD:
        print("Low confidence: result is not reliable")
        
    if true_label_numeric is not None:
        print(f"True Label       : {true_label_numeric} ({true_class_char})")
        print(f"True Status      : {true_status}")
        
    print(f"Predicted Status : {pred_status}")
    
    if true_label_numeric is not None:
        print(f"Result           : {is_correct}")
    print("="*40)

if __name__ == "__main__":
    main()
