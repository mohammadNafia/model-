# ECG Arrhythmia Classification CLI

## The Idea
This project is a lightweight, pure-Python Command Line Interface (CLI) application designed to classify Electrocardiogram (ECG) signals for arrhythmias. The overarching goal was to create a standalone, UI-less, and backend-less tool that relies entirely on a pre-trained Hugging Face deep learning model (`dheerajthuvara/ecg-arrhythmia-detection`). 

It is designed for rapid inference: you feed it raw ECG data either manually or through a CSV file, and it instantly returns whether the heartbeat is **Normal** or **Abnormal** (with the exact detected condition).

## How We Did It
The Hugging Face repository provides the trained weights (`best_model.pt`), a label encoder (`label_encoder.pkl`), and a structural configuration (`model_config.json`). However, it lacks the actual PyTorch class implementation. 

To solve this, we:
1. **Engineered a Fallback Architecture:** We analyzed the parameters inside `model_config.json` (window size of 180, CNN filter channels, LSTM hidden units, etc.) and reverse-engineered a compatible `ECGModel` wrapper structure (`model_wrapper.py`) using `torch.nn`. 
2. **Built Robust Preprocessing:** Real-world ECG signals vary in length and scale. The system automatically converts inputs to numpy arrays, pads/trims them to exactly 180 sequence steps, and applies Z-score normalization using `sklearn.preprocessing.StandardScaler`.
3. **Automated the Pipeline:** We integrated `huggingface_hub` to programmatically download the required model files locally into a cache without user intervention.

## How It Works
When you execute the application, the following pipeline activates:
1. **Input Parsing:** `argparse` reads your comma-separated string or CSV file.
2. **Download & Cache:** `hf_hub_download` fetches the model components from Hugging Face if they are not already cached.
3. **Preprocessing:** The raw array is normalized and reshaped to `(1, 1, 180)` to match the expected input layer of the CNN.
4. **Model Initialization:** The script attempts to load the model. It automatically falls back to our custom `ECGModel` class to inject the weights safely.
5. **Inference:** A PyTorch forward pass generates raw logits, which are converted to probabilities using a Softmax function. The highest probability determines the predicted index.
6. **Decoding:** The index is passed through the downloaded `label_encoder.pkl` to translate it into a human-readable medical class.

## Design System & Architecture
The project follows a strictly modular, monolithic CLI architecture designed for maintainability:

* **`requirements.txt`**: Standardized environment definition.
* **`main.py`**: The central orchestrator. It handles I/O operations, invokes preprocessing, interacts with the Hugging Face API, and prints cleanly formatted terminal outputs.
* **`model_wrapper.py`**: The neural network blueprint. It isolates the PyTorch `nn.Module` definition (a 1D CNN followed by a Bidirectional LSTM) away from the data processing logic, ensuring separation of concerns.

### Classes Handled:
- **N** = Normal
- **L** = Left bundle branch block (LBBB)
- **R** = Right bundle branch block (RBBB)
- **V** = Premature ventricular contraction (PVC)
- **A** = Atrial premature contraction (APC)
