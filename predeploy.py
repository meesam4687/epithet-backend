import os
import requests

# Define the URL of the file to download
GITHUB_RELEASE_URL = "https://github.com/meesam4687/epithet-backend/releases/download/v0.0.1/model.safetensors"

# Define the target directory and file path
MODEL_DIR = "models"
MODEL_FILE_PATH = os.path.join(MODEL_DIR, "model.safetensors")

# Create the models directory if it doesn't exist
os.makedirs(MODEL_DIR, exist_ok=True)

# Download the file
print(f"Downloading model from {GITHUB_RELEASE_URL}...")
response = requests.get(GITHUB_RELEASE_URL, stream=True)

if response.status_code == 200:
    with open(MODEL_FILE_PATH, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Model downloaded successfully to {MODEL_FILE_PATH}")
else:
    print(f"Failed to download model. HTTP Status Code: {response.status_code}")
