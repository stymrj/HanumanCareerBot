import ssl
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from pytz import timezone
from flask import Flask, request
import os
import json
import random

# Set environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
IST = timezone("Asia/Kolkata")

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Create Flask app
app = Flask(__name__)

# Path to store user data
USER_FILE = "users.json"

# Load users from file
def load_users():
    # Check if the file exists, if not create it
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return set(json.load(f))
    else:
        # If the file doesn't exist, create it with an empty list
        with open(USER_FILE, "w") as f:
            json.dump([], f)  # Create an empty list
        return set()

# Save users to file
def save_users():
    with open(USER_FILE, "w") as f:
        json.dump(list(user_ids), f)

# Initialize user_ids from the file
user_ids = load_users()

@app.route('/webhook', methods=['POST'])
def webhook():
    print("📩 Webhook received!")  # Debug message
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_ids.add(message.chat.id)
    save_users()
    print(f"User added: {message.chat.id}")  # Log when a user is added
    welcome_msg = (
        "🚩 *Jai Shree Ram!* 🙏\n\n"
        "Aapka *HanumanBhakti* mein hardik swagat hai! 🔥\n\n"
        "Yeh bot aapko har roz subah se raat tak yaad dilayega:\n"
        "🕉️ Pooja, \n🙏 Bhakti, \n🔥 Career Motivation, \n💡 Life Guidance!\n\n"
        "Menu se command try karo!"
    )
    bot.reply_to(message, welcome_msg, parse_mode='Markdown')

@bot.message_handler(commands=['chalisa'])
def send_chalisa(message):
    bot.reply_to(
        message,
        "📖 *Hanuman Chalisa:*\n[Click here to read](https://www.hindutemplealbany.org/wp-content/uploads/2016/08/Sri_Hanuman_Chalisa_Hindi.pdf)",
        parse_mode='Markdown'
    )
    

@bot.message_handler(commands=['mantra'])
def send_mantra(message):
    bot.reply_to(
        message,
        "🔱 *Hanuman Mantra:*\n_ॐ हनुमते नमः_ 🙏\n\nRepeat with faith, feel the divine energy!",
        parse_mode='Markdown'
    )
    
@bot.message_handler(commands=['bajrangbaan'])
def send_bajrangbaan(message):
    bot.reply_to(
        message,
        "🕉️ *Bajrang Baan:*\n[Click here to read](https://sanskritdocuments.org/doc_z_otherlang_hindi/bajarangabaaNHindi.pdf)",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['aarti'])
def send_aarti(message):
    bot.reply_to(
        message,
        "🪔 *Hanuman Aarti:*\n[Click here to read](https://bhrmfjblog.wordpress.com/wp-content/uploads/2016/06/shree-hanuman-aarti.pdf)",
        parse_mode='Markdown'
    )
    
@bot.message_handler(commands=['tip'])
def send_tip(message):
    bot.reply_to(
        message,
        "💼 *Career Tip:*\nNaukri dhoondhna ek tapasya hai.\nRoz thoda sudhar, thoda research aur full faith rakho Hanuman ji par! 💪",
        parse_mode='Markdown'
    )

# At top
forwarded_messages = {}  # admin_msg_id: user_id
ADMIN_ID = 5341298807

# Step 1: Forward-style manual message + store mapping
@bot.message_handler(func=lambda message: True, content_types=['text'])
def forward_non_command(message):
    if not message.text.startswith('/'):
        msg = f"📨 *Message from @{message.from_user.username or 'user'}* (ID: `{message.chat.id}`):\n\n{message.text}"
        sent = bot.send_message(ADMIN_ID, msg, parse_mode='Markdown')
        forwarded_messages[sent.message_id] = message.chat.id
        bot.reply_to(message, "📩 Aapka message admin tak pahucha diya gaya hai. Jaldi reply milega. Jai Shree Ram! 🙏")

# Step 2: Admin reply logic
@bot.message_handler(func=lambda message: message.reply_to_message and message.chat.id == ADMIN_ID)
def handle_admin_reply(message):
    try:
        reply_id = message.reply_to_message.message_id
        user_id = forwarded_messages.get(reply_id)

        if user_id:
            bot.send_message(chat_id=user_id, text=f"📬 *Admin ka reply:*\n{message.text}", parse_mode='Markdown')
        else:
            bot.reply_to(message, "⚠️ Unable to find the original user for this reply.")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Error: {e}")


def send_daily_reminder(msg):
    print(f"Sending message: {msg}")  # Debug message to track execution
    for uid in user_ids:
        try:
            bot.send_message(chat_id=uid, text=msg, parse_mode='Markdown')
        except Exception as e:
            print(f"Error sending to {uid}: {e}")

scheduler = BackgroundScheduler(timezone=IST)

# Daily schedule for messages with multiple random messages for each time slot
daily_schedule = {
    "05:30": [
        "🌞 *Jaag Jaiye!* Ram naam le kar naya din shuru kijiye! Jai Shree Ram 🙏",
        "🙏 *Subah ka samay hai!* Hanuman ji ko yaad karte hue apna din shuru kijiye.",
        "🌅 *Naya din hai, nayi umeedein!* Jai Shree Ram! 🙏",
    ],
    "05:35": [
        "🪥 *Brush kiya kya?* Subah ki tayyari shuddh mann se shuru hoti hai.",
        "🪥 *Subah ki safai!* Dhoop me apna chehra chamkayein, aur apne man ko pavitra karein.",
        "🌿 *Swachh rahe apna mann,* safai se shuru hota hai Har kaam! 🪥",
    ],
    "05:45": [
        "🧹 *Pooja Sthal Saaf Kiya?* Mandir ya ghar ka ek hissa Hanuman ji ke liye tayyar kijiye.",
        "🧹 *Pooja ki jagah safai ka waqt hai!* Pooja sthal ka safai bhi ek prakar ki bhakti hai.",
        "🕯️ *Sthal ko pavitra rakhein,* apni pooja ke liye ek pavitra jagah tayar karein.",
    ],
    "05:56": [
        "🚿 *Naha liye kya?* Sharir shuddh, mann pavitra - pooja ke liye ready ho jaiye.",
        "🚿 *Naha lo aur tayar ho jao!* Sharir ko shuddh karna pooja ka pehla kadam hai.",
        "💦 *Naha kar apne aapko shuddh karna hai,* taaki mann aur sharir dono pavitra ho sakein.",
    ],
    "06:00": [
        "✅ *Sab kuch ready hai?* Diya, kapoor, mala, chalisa sab rakh liya?",
        "✅ *Sab kuch check kiya?* Diya, kapoor, aur mala ko tayar rakhna zaroori hai.",
        "🪔 *Sab kuch perfect hona chahiye!* Diya jala ke apne man ko pavitra banaayein.",
    ],
    "06:20": [
        "🛕 *Ab shuru ho pooja!* Hanuman ji ko smaran karke prarthna kijiye. Commands: /chalisa /mantra /bajrangbaan",
        "🙏 *Pooja shuru ho gayi?* Hanuman ji ki aarti aur chalisa se din ki shuruaat kijiye.",
        "🕯️ *Pooja ka samay hai!* Hanuman ji ki pooja karna apne jeevan ko safal banaata hai.",
    ],
    "07:30": [
        "🌸 *Pooja ho gayi?* To lo ek achha vichar:\n_“Sankat mochan naam tiharo, sumirat hoye anand.”_",
        "🌸 *Hanuman Ji ki kirpa se sab kuch safal ho!* Aapka din mangalmay ho.",
        "🕉️ *Jab tak man mein bhakti aur shraddha rahe,* sankat kabhi paas nahi aata.",
    ],
    "09:40": [
        "📈 *Career Tip Time:*\nAaj resume bhejna, interview prep karna aur ek naya skill seekhna target rakho!",
        "📊 *Naye goals set karo,* apne career ko agle level par le jao!",
        "💼 *Job search chal rahi hai?* Apne aapko har din thoda aur behtar banao. Hanuman ji ki kripa hamesha aapke saath hai.",
    ],
    "13:10": [
        "🕛 *Madhyahn Vichaar:*\n_“Bhoot pishach nikat nahi aave, Mahavir jab naam sunave.”_",
        "🌸 *Madhyahn mein, apne kaam ko safalta ki or badhao.* Hanuman ji ki kripa aap par sada rahe.",
        "🌞 *Jab tak aapka man safal hone ki ichha rakhta hai,* har kathinai aapke rasta se hatt jayegi.",
    ],
    "15:42": [
        "🧠 *Dopahar ke Baad:* Hanuman ji se seekho: lagataar mehnat aur bhakti se sab mumkin hai!",
        "💪 *Mehnat karna hai to Hanuman ji se seekho,* apni manzil tak pahuncho!",
        "⏰ *Har pal ka upyog karo,* aur apni manzil ki or kadam badhao.",
    ],
    "18:30": [
        "🪔 *Shaam ki Aarti Reminder!*\nDeepak jalao, Hanuman ji ki Aarti karo! Use command: /aarti",
        "🕯️ *Aarti ki tyari ho gayi?* Aaj ki shaam, apne dil ko safai se bhar lo.",
        "🌟 *Aarti ka waqt hai!* Deepak aur diyas ke saath apne ghar ko roshan karo.",
    ],
    "21:00": [
        "🌙 *Raat ka Sandesh:*\nAaj ka din Hanuman ji ko samarpit karke sona.\n_“Ram kaaj karibe ko aatur.”_\nShubh Ratri 🙏",
        "🌙 *Raat ki shanti* ke liye, apne dil mein Hanuman ji ka naam rakh kar neend aaye.",
        "✨ *Suno Hanuman ji ki aarti,* aur apne sapne ko sach karne ke liye apne mann ko aaram de.",
    ]
}

# Add scheduled jobs for each time with random messages
for time_str, messages in daily_schedule.items():
    hour, minute = map(int, time_str.split(":"))
    scheduler.add_job(send_daily_reminder, 'cron', hour=hour, minute=minute, args=[random.choice(messages)])

scheduler.start()

@app.route('/', methods=['GET'])
def index():
    return "🚀 Jai Shree Ram! HanumanBhakt is Live!"

if __name__ == "__main__":
    import logging
    import sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
