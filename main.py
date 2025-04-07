import ssl
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from pytz import timezone
from flask import Flask, request
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
IST = timezone("Asia/Kolkata")
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)
user_ids = set()

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_ids.add(message.chat.id)
    welcome_msg = (
        "🚩 *Jai Shree Ram!* 🙏\n"
        "Aapka *HanumanCareerBot* mein hardik swagat hai! 🔥\n\n"
        "Yeh bot aapko har roz subah se raat tak yaad dilayega:\n"
        "🕉️ Pooja, 🙏 Bhakti, 🔥 Career Motivation, aur 💡 Life Guidance!\n\n"
        "Commands try karo:\n"
        "/chalisa /mantra /bajrangbaan /aarti /tip"
    )
    bot.reply_to(message, welcome_msg, parse_mode='Markdown')

@bot.message_handler(commands=['chalisa'])
def send_chalisa(message):
    bot.reply_to(message, "📖 *Hanuman Chalisa*\nhttps://www.hanuman.com/chalisa", parse_mode='Markdown')

@bot.message_handler(commands=['mantra'])
def send_mantra(message):
    bot.reply_to(message, "🔱 *Hanuman Mantra:*\n_ॐ हनुमते नमः_ 🙏\nRepeat with faith, feel the divine energy!", parse_mode='Markdown')

@bot.message_handler(commands=['bajrangbaan'])
def send_bajrangbaan(message):
    bot.reply_to(message, "🕉️ *Bajrang Baan*\nhttps://www.hanuman.com/bajrangbaan", parse_mode='Markdown')

@bot.message_handler(commands=['aarti'])
def send_aarti(message):
    bot.reply_to(message, "🪔 *Hanuman Aarti*\nhttps://www.hanuman.com/aarti", parse_mode='Markdown')

@bot.message_handler(commands=['tip'])
def send_tip(message):
    bot.reply_to(message, "💼 *Career Tip:*\nNaukri dhoondhna ek tapasya hai.\nRoz thoda sudhar, thoda research aur full faith rakho Hanuman ji par! 💪", parse_mode='Markdown')

def send_daily_reminder(msg):
    for uid in user_ids:
        try:
            bot.send_message(chat_id=uid, text=msg, parse_mode='Markdown')
        except Exception as e:
            print(f"Error sending to {uid}: {e}")

scheduler = BackgroundScheduler(timezone=IST)

daily_schedule = [
    ("05:00", "🌞 *Jaag Jaiye!* Ram naam le kar naya din shuru kijiye! Jai Shree Ram 🙏"),
    ("05:05", "🪥 *Brush kiya kya?* Subah ki tayyari shuddh mann se shuru hoti hai."),
    ("05:30", "🧹 *Pooja Sthal Saaf Kiya?* Mandir ya ghar ka ek hissa Hanuman ji ke liye tayyar kijiye."),
    ("05:40", "🚿 *Naha liye kya?* Sharir shuddh, mann pavitra - pooja ke liye ready ho jaiye."),
    ("05:55", "✅ *Sab kuch ready hai?* Diya, kapoor, mala, chalisa sab rakh liya?"),
    ("06:00", "🛕 *Ab shuru ho pooja!* Hanuman ji ko smaran karke prarthna kijiye. Commands: /chalisa /mantra /bajrangbaan"),
    ("07:00", "🌸 *Pooja ho gayi?* To lo ek achha vichar:\n_“Sankat mochan naam tiharo, sumirat hoye anand.”_"),
    ("09:00", "📈 *Career Tip Time:*\nAaj resume bhejna, interview prep karna aur ek naya skill seekhna target rakho!"),
    ("12:00", "🕛 *Madhyahn Vichaar:*\n_“Bhoot pishach nikat nahi aave, Mahavir jab naam sunave.”_"),
    ("16:00", "🧠 *Dopahar ke Baad:* Hanuman ji se seekho: lagataar mehnat aur bhakti se sab mumkin hai!"),
    ("18:30", "🪔 *Shaam ki Aarti Reminder!*\nDeepak jalao, Hanuman ji ki Aarti karo! Use command: /aarti"),
    ("21:00", "🌙 *Raat ka Sandesh:*\nAaj ka din Hanuman ji ko samarpit karke sona.\n_“Ram kaaj karibe ko aatur.”_\nShubh Ratri 🙏")
]

for time_str, message in daily_schedule:
    hour, minute = map(int, time_str.split(":"))
    scheduler.add_job(send_daily_reminder, 'cron', hour=hour, minute=minute, args=[message])

scheduler.start()

@app.route('/', methods=['GET'])
def index():
    return "🚀 Jai Shree Ram! HanumanCareerBot is Live!"

if __name__ == "__main__":
    import logging
    import sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
