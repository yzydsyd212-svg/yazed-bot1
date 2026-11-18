import os
import time
import json
import threading
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_KEY = os.environ.get("GROQ_KEY")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=data, timeout=10)
    except:
        pass

def ask_groq(q):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "انت مساعد ذكي، جاوب بالعربي، خلي اجابتك قصيرة وواضحة ومفهومة."},
            {"role": "user", "content": q}
        ]
    }
    try:
        res = requests.post(url, headers=headers, json=data, timeout=30)
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return "صار خطأ، جرب مرة تانية."

def keep_alive():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is alive!")
        def log_message(self, *args):
            pass
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

keep_alive()

offset = 0
print("Bot started...")
while True:
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
        res = requests.get(url, params={"offset": offset, "timeout": 30}, timeout=35).json()
        for update in res.get("result", []):
            offset = update["update_id"] + 1
            msg = update.get("message", {})
            chat_id = msg.get("chat", {}).get("id")
            text = msg.get("text", "")
            if chat_id and text:
                if text == "/start":
                    send_message(chat_id, "اهلا! انا بوتك، ابعتلي اي سؤال.")
                else:
                    reply = ask_groq(text)
                    send_message(chat_id, reply)
    except Exception as e:
        print("Error:", e)
        time.sleep(3)
