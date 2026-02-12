# 📚 Library Assistant Bot

A modern **AI-powered Library Assistant Chatbot** built with **FastAPI** and **Groq LLMs** using the **OpenAI Python SDK**.  
This bot helps users search books, get recommendations, issue/return/renew books, and understand library rules — all without a database.

---

## 🚀 Features

✅ AI-powered conversational assistant  
✅ Book search with availability status  
✅ Issue, return, and renew books  
✅ Book recommendations and descriptions  
✅ Library rules and policies  
✅ In-memory catalog (no database)  
✅ Groq LLM integration using OpenAI SDK  
✅ Clean modern chat UI  
✅ Windows-safe FastAPI backend  

---

## 🏗️ Tech Stack

| Layer | Technology |
|------|------------|
| Backend | FastAPI |
| AI Model | `openai/gpt-oss-20b` via Groq |
| SDK | OpenAI Python SDK |
| Frontend | HTML + CSS + JavaScript |
| Storage | In-memory (no DB) |

---

## 📁 Project Structure

```
LibraryBot/
│
├── backend/
│   ├── app.py
│   └── .env
│
└── frontend/
    └── index.html
```

---

## 🔐 Setup

### 1️⃣ Clone Project
```bash
git clone <your-repo-url>
cd LibraryBot
```

---

### 2️⃣ Backend Setup

```bash
cd backend
pip install fastapi uvicorn openai python-dotenv
```

Create a `.env` file:

```
OPENAI_API_KEY=your_groq_api_key_here
```

---

### 3️⃣ Run Backend

```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --workers 1
```

You should see:

```
Uvicorn running on http://127.0.0.1:8000
```

---

### 4️⃣ Run Frontend

Open:

```
frontend/index.html
```

in your browser.

---

## 🧪 Example Prompts

```
Tell me about Clean Code
Search Python books
Is Deep Learning available?
Recommend me an AI book
Issue book 2
Return book 2
Renew book 3
Library rules
```

---

## 🤖 Supported AI Model

This project uses:

```
openai/gpt-oss-20b
```

via Groq’s OpenAI-compatible API.

---

## 🔧 API Endpoint

### POST `/chat`

Request:
```json
{
  "message": "Tell me about Clean Code"
}
```

Response:
```json
{
  "reply": "Clean Code by Robert C. Martin focuses on..."
}
```

---

## 🛡️ Error Handling

- Gracefully handles invalid book IDs
- Safe fallback for model/API failures
- Windows multiprocessing safe
- No database crashes

---

## 🌟 Future Enhancements

- User login & borrowing history
- Admin dashboard
- PDF receipts
- Voice input/output
- Streaming responses
- Database integration

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

## 👨‍💻 Author

Built by **Ashwath Nagarajan** with ❤️ using FastAPI and Groq AI.