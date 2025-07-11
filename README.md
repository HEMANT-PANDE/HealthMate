# 🧠 HealthMate – AI-Based Personalized Health Advisor

HealthMate is a lightweight, AI-powered chatbot that offers personalized health and wellness advice based on user input. It leverages a local LLM (TinyLLaMA 1.1B) integrated via `llama-cpp-python`, along with a contextual dataset (EHR + simulated wearable data) to deliver lifestyle-based recommendations.

---

## 🚀 Features

- Conversational health assistant powered by an open-source LLM
- Personalized advice based on biometric and lifestyle patterns
- Streamlit-based chat interface for ease of use
- Handles fuzzy inputs, common questions, and contextual follow-ups
- Lightweight deployment on Render using Google Drive model hosting

---

## 📊 Dataset

- **EHR Source:** PIMA Indians Diabetes Dataset
- **Wearable Data:** Simulated step count, sleep, and heart rate data
- **Purpose:** Risk estimation and lifestyle advisory for diabetes, inactivity, poor sleep, etc.

---

## 🧠 Model Details

- **Model Used:** TinyLLaMA 1.1B Chat (`.gguf` format)
- **Inference Engine:** llama-cpp-python
- **Tokens:** 2048 context tokens
- **Deployment:** CPU-optimized, offline-ready

---

## 🛠️ Tech Stack

| Component        | Technology            |
|------------------|------------------------|
| Frontend         | Streamlit              |
| Backend Model    | llama-cpp-python       |
| Data Handling    | Pandas                 |
| Deployment       | Render.com             |
| Model Storage    | Google Drive (downloaded at runtime) |
| Version Control  | Git & GitHub           |

---


## ⚙️ Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HEMANT-PANDE/HealthMate.git
   cd HealthMate
2. **Create a virtual environment :**

   python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install dependencies :**
pip install -r requirements.txt

4. **Run the app :**
streamlit run app.py




