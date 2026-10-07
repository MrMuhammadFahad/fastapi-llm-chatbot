# 🤖 FastAPI Qwen Chatbot

A full-stack chatbot application powered by **FastAPI** and **Hugging Face Transformers (Qwen)** with a modern web UI.

---

## Features

-  FastAPI backend with LLM (Qwen)
-  Chat UI (HTML, CSS, JS)
-  Streaming typing effect
-  Markdown rendering (code blocks, bold, etc.)
-  Dark mode toggle
-  Chat history persistence (localStorage)
-  Conversation memory (backend)

---

Create virtual environment

python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\\Scripts\\activate     # (Windows)

Install dependencies
pip install fastapi uvicorn transformers torch

Run the App
Start FastAPI server
uvicorn main:app --reload
