import torch
import json
import numpy as np
import os
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2
from src.model import PlantDiseaseClassifier
from huggingface_hub import hf_hub_download

MODEL_PATH = "models/best_model.pth"
CLASS_PATH = "models/class_names.json"
HF_REPO    = "ankit2293/plant-disease-efficientnet"

os.makedirs("models", exist_ok=True)

if not os.path.exists(MODEL_PATH):
    print("📥 Downloading model...")
    hf_hub_download(
        repo_id=HF_REPO,
        filename="best_model.pth",
        local_dir="models"
    )

if not os.path.exists(CLASS_PATH):
    hf_hub_download(
        repo_id=HF_REPO,
        filename="class_names.json",
        local_dir="models"
    )

with open(CLASS_PATH, 'r') as f:
    CLASS_NAMES = json.load(f)

# ✅ Force CPU + reduce memory
torch.set_num_threads(1)
device = torch.device('cpu')

model = PlantDiseaseClassifier(num_classes=38, pretrained=False).to(device)
checkpoint = torch.load(MODEL_PATH, map_location=device, weights_only=True)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# ✅ Free checkpoint memory immediately
del checkpoint
import gc
gc.collect()

print(f"✅ Model loaded")

inference_transforms = A.Compose([
    A.Resize(300, 300),
    A.CenterCrop(260, 260),
    A.Normalize(mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]),
    ToTensorV2()
])

def predict_disease(image_path: str):
    image  = np.array(Image.open(image_path).convert('RGB'))
    tensor = inference_transforms(image=image)['image']
    tensor = tensor.unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(tensor)
        probs   = torch.softmax(outputs, dim=1)
        top3_probs, top3_idx = probs.topk(3, dim=1)

    disease    = CLASS_NAMES[top3_idx[0][0].item()]
    confidence = top3_probs[0][0].item()

    top3 = [
        {
            "disease"   : CLASS_NAMES[top3_idx[0][i].item()],
            "confidence": round(top3_probs[0][i].item(), 4)
        }
        for i in range(3)
    ]
    return disease, round(confidence, 4), top3