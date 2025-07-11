import os
import streamlit as st
from llama_cpp import Llama
from utils.prompt_builder import build_prompt
from utils.data_lookup import search_relevant_facts
from utils.preprocess import clean_input
import requests

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

def download_model_from_gdrive(file_id, dest_path):
    if os.path.exists(dest_path):
        return
    print(" Downloading model from Google Drive...")
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url, stream=True)
    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

#  Model Config
MODEL_ID = "1JVvjBG2lNHe7eV-jkGt4Qnofk0-B2Ic4"
MODEL_PATH = "model/tinyllama-1.1b-chat-v1.0.Q3_K_M.gguf"
download_model_from_gdrive(MODEL_ID, MODEL_PATH)
llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=4, verbose=False)

#  Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#  Page UI
st.set_page_config(page_title="HealthMate - Chat", layout="centered")
st.markdown("## 🧠 HealthMate - Personalized Health Assistant")

#  User Input
user_input = st.chat_input("Talk to your health assistant...")

#  Chat Handling
if user_input:
    st.chat_message("user").markdown(user_input)
    cleaned_input = clean_input(user_input)

    # Simple friendly replies
    greetings = ["hi", "hello", "hey"]
    thanks = ["thank", "thanks", "thankyou"]

    if any(word in cleaned_input for word in greetings):
        bot_reply = "👋 Hi there! I'm HealthMate. How can I support your wellness journey today?"
    elif any(word in cleaned_input for word in thanks):
        bot_reply = "You're welcome! 😊 Let me know if you need health suggestions or motivation."
    else:
        try:
            matched_rows = search_relevant_facts(cleaned_input)
        except Exception as e:
            matched_rows = None

        prompt = build_prompt(cleaned_input, matched_rows)
        try:
            response = llm(prompt, max_tokens=256, stop=["</s>"], echo=False)
            bot_reply = response["choices"][0]["text"].strip()
        except Exception:
            bot_reply = "⚠️ Sorry, I'm having trouble processing that. Could you please rephrase?"

    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.chat_history.append((user_input, bot_reply))

# 🔹 Sidebar Removed PDF Export — Now just optional space
with st.sidebar:
    st.header("ℹ️ Tips")
    st.info("Try asking:\n- 'I'm 20 and walk 3000 steps, how to improve health?'\n- 'Suggest better sleep routine for a student.'")
