import torch
from huggingface_hub import hf_hub_download

MODEL_REPO = "dheerajthuvara/ecg-arrhythmia-detection"
model_path = hf_hub_download(repo_id=MODEL_REPO, filename="models/best_model.pt")

state_dict = torch.load(model_path, map_location="cpu", weights_only=False)

print("Keys in state_dict:")
for key in state_dict.keys():
    print(key)
