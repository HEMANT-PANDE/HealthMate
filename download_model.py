# download_model.py
import gdown


MODEL_ID = "1JVvjBG2lNHe7eV-jkGt4Qnofk0-B2Ic4"
OUTPUT_PATH = "model/tinyllama-1.1b-chat-v1.0.Q3_K_M.gguf"

# Download from Google Drive to the model folder
gdown.download(id=MODEL_ID, output=OUTPUT_PATH, quiet=False)
