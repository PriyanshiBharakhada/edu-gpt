# 🚀 Edu-gpt

**Hybrid Chatbot (Edu + Interview) with PDF QA using LLaMA.cpp**

Edu-gpt is an intelligent hybrid chatbot built with Django and LLaMA.cpp that allows users to:
- Choose between education or interview modes.
- Get mock interview responses.
- Upload PDFs and ask questions based on the content.
- 🔒 Your data stays private — everything runs locally.

---

## 🎬 Demo Video

Watch the demo: https://drive.google.com/file/d/1blHc8lH9Z3Waop4q8_DIRl0oajg-OLTi/view?usp=drive_link

---

## 🧠 Features

- 📄 PDF-based QA using FAISS + LLaMA.cpp
- 💬 Chat with educational or interview-focused responses
- 👤 Login/Register to see chat history
- 🔐 Secure & clean backend with Django + SQLite

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/PriyanshiBharakhada/edu-gpt.git
cd edu-gpt

2. Setup Virtual Environment

python -m venv venv
venv\Scripts\activate      # For Windows

3. Install Requirements
pip install -r requirements.txt

4. Download the LLaMA Model
Download a .gguf LLaMA model (e.g., LLaMA 2 7B) from Hugging Face and place it at:


/models/llama-2-7b-chat.Q4_K_M.gguf
🛑 Not included in repo due to size.

5. Run Django Server
python manage.py runserver

6.Techstack:

| Layer         | Technology        |
| ------------- | ----------------- |
| Backend       | Django (Python)   |
| LLM Inference | LLaMA.cpp         |
| Indexing      | FAISS             |
| UI            | HTML,CSS,JS       |
| Database      | SQLite            |


👩‍💻 Author
Priyanshi Bharakhada
📌 B.Tech CSE (AIML) – GLS University
🌐 LinkedIn : https://www.linkedin.com/in/priyanshi-bharakhada/

