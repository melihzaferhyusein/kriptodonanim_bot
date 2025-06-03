from flask import Flask, request
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from datetime import datetime

app = Flask(__name__)

# ======= BOT AYARLARI =======
TOKEN = '8080531240:AAE-_U1QaQOx5BXRuQGugxHnJ_nmo1cbYVo'
API_URL = f'https://api.telegram.org/bot{TOKEN}'
CHANNEL_ID = '@kriptodonanim'
GROUP_ID = '-1002251019196'

# ======= MESAJ GÖNDERME =======
def send_to_telegram(chat_id, text, reply_markup=None):
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
    if reply_markup:
        data['reply_markup'] = reply_markup
    requests.post(f"{API_URL}/sendMessage", json=data)

# ======= BAŞLANGIÇ SELAMI + BUTON =======
def send_welcome_message():
    text = (
        "👋 *Selam millet!*\n\n"
        "Ben sizin kripto dostunuz *Kripto Donanım Botuyum!*\n"
        "Güncel sinyaller, analizler ve otomatik mesajlarla hep yanınızdayım! 🤖📈"
    )
    button = {
        "inline_keyboard": [[
            {"text": "📢 Kanalı Takip Et", "url": "https://t.me/kriptodonanim"},
            {"text": "💬 Grubumuza Katıl", "url": "https://t.me/kriptodonanim"}
        ]]
    }
    send_to_telegram(CHANNEL_ID, text, button)
    send_to_telegram(GROUP_ID, text, button)

# ======= ZAMANLANMIŞ MESAJLAR =======
TZ = pytz.timezone('Europe/Istanbul')

def send_morning_message():
    text = "🌞 *Günaydın dostlar!*\n\nYeni bir gün, yeni fırsatlar. Bol kazançlar dilerim! 💸📈"
    send_to_telegram(CHANNEL_ID, text)
    send_to_telegram(GROUP_ID, text)

def send_evening_message():
    text = (
        "🌙 *İyi akşamlar kripto dostları!*\n\n"
        "Biraz dinlenme vakti geldi sanırım... ama merak etmeyin, *ben uyumuyorum!* 😴❌\n"
        "Sinyal bekleyenler için fırsat kollamaya devam edeceğim.\n"
        "Ne de olsa 7/24 çalışan bir bottan fazlasıyım, *ben bir yaşam tarzıyım*! 🤖💹"
    )
    send_to_telegram(CHANNEL_ID, text)
    send_to_telegram(GROUP_ID, text)

def send_friday_message():
    weekday = datetime.now(TZ).weekday()
    if weekday == 4:  # Cuma
        text = "🕌 *Hayırlı Cumalar!*\n\nBu mübarek günde bol bereketli kazançlar dilerim. 🙏💹"
        send_to_telegram(CHANNEL_ID, text)
        send_to_telegram(GROUP_ID, text)

scheduler = BackgroundScheduler(timezone=TZ)
scheduler.add_job(send_morning_message, trigger='cron', hour=9, minute=0)
scheduler.add_job(send_evening_message, trigger='cron', hour=23, minute=0)
scheduler.add_job(send_friday_message, trigger='cron', hour=12, minute=0)
scheduler.start()

# ======= WEBHOOK (TradingView vs için) =======
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = request.json
        message = data.get('message', '📡 Yeni bir sinyal geldi!')
        send_to_telegram(CHANNEL_ID, message)
        send_to_telegram(GROUP_ID, message)
        return 'OK', 200
    return 'BOT AKTİF ✅', 200

# ======= BAŞLATMA =======
if __name__ == '__main__':
    send_welcome_message()
    app.run(host='0.0.0.0', port=5000)
