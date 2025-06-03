from flask import Flask, request
import requests

app = Flask(__name__)

# Bot token
TELEGRAM_TOKEN = '8080531240:AAE-_U1QaQOx5BXRuQGugxHnJ_nmo1cbYVo'

# Hedefler
TELEGRAM_CHANNEL_ID = '@kriptodonanim'          # Kanal username
TELEGRAM_GROUP_ID = '-1002251019196'            # Grup chat ID (negatif sayı)

def send_telegram_message(chat_id, message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    return requests.post(telegram_url, json=payload)

@app.route('/')
def home():
    return 'TradingView ➜ Telegram bot is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Webhook'a gelen JSON
        data = request.json
        message = data.get('message', '⚠️ No message content received.')

        # Kanal ve grup mesaj gönderimi
        resp1 = send_telegram_message(TELEGRAM_CHANNEL_ID, message)
        resp2 = send_telegram_message(TELEGRAM_GROUP_ID, message)

        # Hata kontrol
        if resp1.status_code != 200 or resp2.status_code != 200:
            return f"Telegram error: {resp1.text} | {resp2.text}", 500

        return 'Message sent to both channel and group!', 200

    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
