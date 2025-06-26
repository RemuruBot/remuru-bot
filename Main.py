from flask import Flask, request
import requests
import openai
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route("/", methods=["GET"])
def index():
    return "Bot is running"

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return "No data", 400

    message = data.get("message", {}).get("text")
    chat_id = data.get("message", {}).get("chat", {}).get("id")

    if message and chat_id:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": message}]
            )
            reply = response.choices[0].message["content"]
        except Exception as e:
            reply = f"Ошибка OpenAI: {e}"

        send_message(chat_id, reply)

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)я
