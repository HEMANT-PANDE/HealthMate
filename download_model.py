import os
import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params={'id': id}, stream=True)

    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    token = get_confirm_token(response)
    if token:
        response = session.get(URL, params={'id': id, 'confirm': token}, stream=True)

    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

# Usage
file_id = "1JVvjBG2lNHe7eV-jkGt4Qnofk0-B2Ic4"
dest_path = "model/tinyllama-1.1b-chat-v1.0.Q3_K_M.gguf"
os.makedirs("model", exist_ok=True)
download_file_from_google_drive(file_id, dest_path)
