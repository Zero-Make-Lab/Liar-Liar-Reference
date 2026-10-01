"""Download GPT-2 XL (2019, 1.5B) weights to the E: hard drive (safetensors + tokenizer only)."""
import os
os.environ.setdefault("HF_HOME", r"E:\ai-models\huggingface")
from huggingface_hub import snapshot_download

path = snapshot_download(
    "openai-community/gpt2-xl",
    allow_patterns=["*.json", "*.txt", "model.safetensors"],   # skip duplicate TF/Flax/ONNX/bin copies
    local_dir=r"E:\ai-models\gpt2-xl",                          # plain files: Windows blocks HF cache symlinks
)
print("GPT-2 XL ready at", path, flush=True)
