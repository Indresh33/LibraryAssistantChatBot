import os
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# -------------------- CONFIG --------------------

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"
MODEL = "openai/gpt-oss-20b"

if not API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY not found")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

app = FastAPI(title="Library Assistant Bot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- IN-MEMORY BOOK CATALOG --------------------

BOOKS = [
    {"id": 1, "title": "Deep Learning", "author": "Ian Goodfellow", "available": True, "desc": "Comprehensive deep learning theory and practice."},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin", "available": True, "desc": "Best practices for writing clean, maintainable software."},
    {"id": 3, "title": "Python Crash Course", "author": "Eric Matthes", "available": False, "desc": "Beginner-friendly introduction to Python programming."},
    {"id": 4, "title": "Artificial Intelligence: A Modern Approach", "author": "Russell & Norvig", "available": True, "desc": "Definitive textbook on AI concepts and methods."},
    {"id": 5, "title": "Design Patterns", "author": "Erich Gamma", "available": True, "desc": "Classic guide to reusable object-oriented design patterns."},
]

RULES = """
📚 Library Rules:
• Maximum 3 books per user
• Loan period: 14 days
• Late fee: ₹2 per day
• One renewal allowed per book
"""

# -------------------- REQUEST MODEL --------------------

class ChatRequest(BaseModel):
    message: str

# -------------------- LIBRARY CORE --------------------

def normalize(text: str):
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()

def find_book_by_title(query: str):
    q = normalize(query)
    for b in BOOKS:
        if q in normalize(b["title"]):
            return b
    return None

def search_books(query: str):
    q = normalize(query)
    results = [
        b for b in BOOKS
        if q in normalize(b["title"]) or q in normalize(b["author"])
    ]
    if not results:
        return "❌ I couldn’t find any books matching that."

    reply = "📚 Here are the books I found:\n\n"
    for b in results:
        status = "Available ✅" if b["available"] else "Currently issued ❌"
        reply += f"{b['id']}. **{b['title']}** by {b['author']} — {status}\n   {b['desc']}\n\n"
    return reply.strip()

def issue_book(book_id: int):
    for b in BOOKS:
        if b["id"] == book_id:
            if not b["available"]:
                return f"❌ '{b['title']}' is already issued."
            b["available"] = False
            return f"✅ You have successfully borrowed **{b['title']}**. Please return it within 14 days."
    return "❌ I couldn’t find that book ID."

def return_book(book_id: int):
    for b in BOOKS:
        if b["id"] == book_id:
            if b["available"]:
                return f"ℹ️ **{b['title']}** was not currently issued."
            b["available"] = True
            return f"✅ **{b['title']}** has been returned successfully. Thank you!"
    return "❌ I couldn’t find that book ID."

def renew_book(book_id: int):
    for b in BOOKS:
        if b["id"] == book_id:
            if b["available"]:
                return f"❌ **{b['title']}** is not currently borrowed."
            return f"🔄 **{b['title']}** has been renewed for another 14 days."
    return "❌ I couldn’t find that book ID."

# -------------------- SMART COMMAND PARSER --------------------

def parse_command(text: str):
    t = normalize(text)

    issue = re.search(r"(issue|borrow)\s+(?:book\s*)?(\d+)", t)
    if issue:
        return ("issue", int(issue.group(2)))

    ret = re.search(r"(return)\s+(?:book\s*)?(\d+)", t)
    if ret:
        return ("return", int(ret.group(2)))

    renew = re.search(r"(renew)\s+(?:book\s*)?(\d+)", t)
    if renew:
        return ("renew", int(renew.group(2)))

    if "rule" in t or "policy" in t:
        return ("rules", None)

    if t.startswith("search") or t.startswith("find"):
        return ("search", t.replace("search", "").replace("find", "").strip())

    return (None, None)

# -------------------- HEALTH --------------------

@app.get("/")
def health():
    return {"status": "Library Assistant running"}

# -------------------- CHAT --------------------

conversation_memory = []

@app.post("/chat")
def chat(req: ChatRequest):
    user_msg = req.message.strip()
    intent, value = parse_command(user_msg)

    # ---------- Deterministic actions ----------
    if intent == "issue":
        return {"reply": issue_book(value)}

    if intent == "return":
        return {"reply": return_book(value)}

    if intent == "renew":
        return {"reply": renew_book(value)}

    if intent == "rules":
        return {"reply": RULES}

    if intent == "search":
        return {"reply": search_books(value)}

    # ---------- LLM conversational mode ----------
    catalog_text = "\n".join(
        f"{b['id']}. {b['title']} by {b['author']} — "
        f"{'Available' if b['available'] else 'Issued'} — {b['desc']}"
        for b in BOOKS
    )

    system_prompt = f"""
You are a friendly and knowledgeable library assistant.

Library catalog:
{catalog_text}

Rules:
{RULES}

Your job:
- Explain books clearly when asked
- Recommend books based on user interests
- Mention availability
- Suggest actions like issuing, returning, or searching
- Be concise but helpful
"""

    conversation_memory.append({"role": "user", "content": user_msg})

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system_prompt}] + conversation_memory[-8:],
        temperature=0.6,
        max_tokens=400,
    )

    reply = response.choices[0].message.content
    conversation_memory.append({"role": "assistant", "content": reply})

    return {"reply": reply}
