import os
import streamlit as st
from llama_cpp import Llama
from utils.prompt_builder import build_prompt
from utils.data_lookup import search_relevant_facts
from utils.preprocess import clean_input
import requests
import time

def download_file_from_google_drive(file_id, dest_path):
    # Function for model download is assumed to be skipped or handled manually
    pass


MODEL_ID = "1JVvjBG2lNHe7eV-jkGt4Qnofk0-B2Ic4"
MODEL_PATH = "model/tinyllama-1.1b-chat-v1.0.Q3_K_M.gguf"

# Check if the file exists before attempting to load
if not os.path.exists(MODEL_PATH):
    st.error(f"⚠️ Model File Missing! The model file expected at '{MODEL_PATH}' was not found.")
    st.error("Please manually download the correct GGUF file and place it in the 'model/' folder.")
    st.stop()

# Load the LLM
try:
    llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=4, verbose=False)
except Exception as e:
    st.error(f"⚠️ Model Loading Failed! The file '{MODEL_PATH}' was found, but failed to load.")
    st.error(f"Error details: {e}")
    st.stop()


# Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "performance_log" not in st.session_state:
    st.session_state.performance_log = []

# Page UI
st.set_page_config(page_title="HealthMate - Chat", layout="centered")
st.markdown("## 🧠 HealthMate - Personalized Health Assistant")

# User Input
user_input = st.chat_input("Talk to your health assistant...")

# Chat Handling
if user_input:
    st.chat_message("user").markdown(user_input)
    
    # Check 1: Clean Input Function Failure
    try:
        cleaned_input = clean_input(user_input)
    except Exception as e:
        st.chat_message("assistant").error(f"Error in cleaning input: {e}")
        st.stop()
        
    bot_reply = None
    
    # Simple friendly replies
    greetings = ["hi", "hello", "hey"]
    thanks = ["thank", "thanks", "thankyou"]

    # --- CRITICAL CHANGE: Check if the input starts with a greeting/thanks ---
    # This prevents complex queries that start with "hi," from being classified as a simple greeting
    
    if any(cleaned_input.startswith(word) for word in greetings) and len(cleaned_input) < 10:
        bot_reply = "👋 Hi there! I'm HealthMate. How can I support your wellness journey today?"
    elif any(cleaned_input.startswith(word) for word in thanks) and len(cleaned_input) < 15:
        bot_reply = "You're welcome! 😊 Let me know if you need health suggestions or motivation."
    # --- END CRITICAL CHANGE ---

    # If bot_reply is still None, it means it's a substantive query, so run the LLM logic
    if bot_reply is None:
        # Check 2 & 3: Relevant Facts Search and Prompt Building
        matched_rows = None
        try:
            matched_rows = search_relevant_facts(cleaned_input)
        except Exception as e:
            # Print to console for debugging external helper functions
            print(f"Error during search_relevant_facts: {e}")

        prompt = None
        try:
            prompt = build_prompt(cleaned_input, matched_rows)
        except Exception as e:
            st.chat_message("assistant").error(f"Error in building prompt: {e}")
            st.stop()

        # --- TECHNICAL PERFORMANCE MEASUREMENT START ---
        
        start_time = time.time()
        
        # Check 4: LLM Inference Failure
        try:
            response = llm(prompt, max_tokens=350, stop=["</s>"], echo=False)
            end_time = time.time()
            
            if response and "choices" in response and len(response["choices"]) > 0:
                choice = response["choices"][0]
                
                bot_reply = choice.get("text", "").strip()
                
                # Performance Metric Calculation
                inference_latency = end_time - start_time
                
                # FIX: Check for 'tokens' key first, if missing, estimate tokens using the generated text length
                if "tokens" in choice:
                    generated_tokens = len(choice["tokens"])
                elif bot_reply:
                    # Fallback: Approximate tokens by encoding the final text (rough estimate for performance logging)
                    generated_tokens = len(llm.tokenize(bot_reply.encode('utf-8')))
                    print("WARNING: 'tokens' key missing. Using tokenizer fallback for token count.")
                else:
                    # If both 'tokens' and 'text' are missing/empty, we can't calculate metrics
                    raise ValueError("LLM returned an empty or invalid response structure with no text.")
                
                # Ensure latency is not zero to avoid division by zero
                if inference_latency > 0 and generated_tokens > 0:
                    tokens_per_second = generated_tokens / inference_latency
                else:
                    tokens_per_second = 0.0 # Cannot calculate meaningful TPS
                
                st.session_state.performance_log.append({
                    "latency_s": inference_latency,
                    "tps": tokens_per_second,
                    "tokens": generated_tokens,
                    "input": user_input
                })
                
                # Print metrics to the console
                print("-" * 50)
                print(f"Query: {user_input[:50]}...")
                print(f"| TECHNICAL METRICS |")
                print(f"| Inference Latency: {inference_latency:.2f} seconds")
                print(f"| Generated Tokens: {generated_tokens}")
                print(f"| Tokens Per Second (t/s): {tokens_per_second:.2f}")
                print("-" * 50)
                
            else:
                raise ValueError("LLM returned an empty or invalid response structure.")
            # --- END IMPROVED ERROR HANDLING ---
            
        except Exception as e:
            # This is the final fallback for LLM generation failure
            bot_reply = f"⚠️ Sorry, the LLM failed to generate a response. Error: {e}. Please try again."

    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.chat_history.append((user_input, bot_reply))

# Sidebar displays the average performance metrics
with st.sidebar:
    st.header("ℹ️ Tips")
    st.info("Try asking:\n- My steps per day are usually below 2000, and my blood glucose level is concerningly high. How can I lower my risk for diabetes this week?'\n- 'Suggest better sleep routine for a student.'")
    
    # Calculate and display average performance
    if st.session_state.performance_log:
        all_latency = [item["latency_s"] for item in st.session_state.performance_log]
        all_tps = [item["tps"] for item in st.session_state.performance_log]
        
        avg_latency = sum(all_latency) / len(all_latency)
        avg_tps = sum(all_tps) / len(all_tps)

        st.markdown("---")
        st.subheader("📊 Average Performance")
        st.metric(label="Avg Inference Latency", value=f"{avg_latency:.2f} s")
        st.metric(label="Avg Tokens/Second (t/s)", value=f"{avg_tps:.2f}")
        st.caption(f"Based on {len(st.session_state.performance_log)} completed LLM responses.")
