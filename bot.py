import json, urllib.request, time, os, threading
from http.server import BaseHTTPRequestHandler, HTTPServer

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_KEY = os.environ.get("GROQ_KEY")

def send(chat_id, text):
    data = {"chat_id": chat_id, "text": text}
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req)

def ask_groq(q):
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "انت بوت اسمه يازد بوت. جاوب دايما بالعربي الفلسطيني العامي تبع غزة، بلهجة شبابية وودودة. ممنوع تجاوب بالانجليزي ابدا، حتى لو سألوك بالانجليزي جاوب بالعربي. خلي اجاباتك قصيرة وواضحة ومفهومة."},
            {"role": "user", "content": q}
        ]
    }
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(data).encode(),
        headers={"Authorization": "Bearer " + GROQ_KEY, "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read())
        return res["choices"][0]["message"]["content"]

def keep_alive():
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200); self.end_headers(); self.wfile.write(b"Bot is alive")
        def log_message(self, *a): pass
    port = int(os.environ.get("PORT", 10000))
    HTTP
