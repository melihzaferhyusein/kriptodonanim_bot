from flask import Flask, request
import requests

app = Flask(__name__)

# Telegram bot token and public channel username
TELEGRAM_TOKEN = '8080531240:AAE-_U1QaQOx5BXRuQGugxHnJ_nmo1cbYVo'
TELEGRAM_CHAT_ID = '@kriptodonanim'

@app.route('/')
def home():
    return 'TradingView ➜ Telegram bot is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        message = data.get('message', '⚠️ No message content received.')

        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }

        response = requests.post(telegram_url, json=payload)
        if response.status_code != 200:
            return f"Telegram error: {response.text}", 500

        return 'Message sent to Telegram!', 200
    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
