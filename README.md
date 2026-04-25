# ECG Arrhythmia Classification CLI

## The Idea
This project is a lightweight, pure-Python Command Line Interface (CLI) application designed to classify Electrocardiogram (ECG) signals for arrhythmias. The overarching goal was to create a standalone tool that relies entirely on a pre-trained Hugging Face deep learning model (`dheerajthuvara/ecg-arrhythmia-detection`).

It is designed for rapid inference: you feed it raw ECG data manually, via CSV, or by selecting a row from the **MIT-BIH Heartbeat Categorization Dataset**.

## How We Did It
The Hugging Face repository provides the trained weights (`best_model.pt`), but lacks the actual PyTorch class implementation.

To solve this, we:
1. **Engineered a Fallback Architecture:** We reverse-engineered a compatible `ECGModel` wrapper structure (`model_wrapper.py`) matching the exact layers found in the saved checkpoint, including a CNN, BiLSTM, and an Attention mechanism.
2. **Kaggle Integration:** Added automatic downloading and extraction of the MIT-BIH dataset using the Kaggle API.
3. **Built Robust Preprocessing:** Real-world ECG signals are automatically padded/trimmed to 180 sequence steps and Z-score normalized.
4. **Automated the Pipeline:** We integrated `huggingface_hub` to programmatically download the required model files locally.

## How It Works
1. **Input Source:** Choose between a row from the MIT-BIH dataset (`--row`), a generic CSV (`--csv`), or manual values (`--manual`).
2. **Setup:** The script ensures all datasets and model weights are downloaded and extracted.
3. **Preprocessing:** The signal is standardized for the CNN input.
4. **Inference:** A PyTorch forward pass calculates the probability of different arrhythmia classes.
5. **Decoding:** Results are mapped to human-readable statuses (Normal vs Abnormal).

## Design System & Architecture
The project follows a modular CLI architecture:

* **`requirements.txt`**: Project dependencies.
* **`main.py`**: The central orchestrator handling CLI, I/O, and inference logic.
* **`model_wrapper.py`**: The neural network blueprint (CNN-BiLSTM-Attention).

### Classes Handled:
- **N** = Normal
- **S** = Abnormal (Supraventricular)
- **V** = Abnormal (Ventricular)
- **F** = Abnormal (Fusion)
- **Q** = Abnormal (Unknown/Other)

### MIT-BIH Mapping:
- **0**: Normal
- **1, 2, 3, 4**: Abnormal
