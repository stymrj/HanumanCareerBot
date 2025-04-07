# HanumanCareerBot

A Telegram bot that sends daily reminders for spiritual practices and career motivation, combining devotion to Hanuman ji with daily career guidance. The bot is designed to send devotional messages, pooja reminders, and motivational tips at various times of the day.

## Features

- **Spiritual Reminders**: Sends Hanuman-related pooja reminders and devotional content.
- **Career Motivation**: Provides tips and advice for job seekers, including career guidance and job search tips.
- **Commands**:
  - `/chalisa` - Sends the Hanuman Chalisa.
  - `/mantra` - Sends the Hanuman Mantra.
  - `/bajrangbaan` - Sends the Bajrang Baan.
  - `/aarti` - Sends the Hanuman Aarti.
  - `/tip` - Sends a motivational career tip.

## Requirements

- Python 3.8+
- Flask
- APScheduler
- Telebot
- pytz
- SSL (for production deployment)
- A Telegram bot token

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/HanumanCareerBot.git
cd HanumanCareerBot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Set Environment Variables
Create a .env file in the root directory and add the following environment variables:
```bash
BOT_TOKEN=<your-telegram-bot-token>
WEBHOOK_URL=<your-webhook-url>
```
### 4. Run the Bot Locally
Start the Flask server:
```bash
python bot.py
```
This will run the bot on http://localhost:5000. To set up production, you can use platforms like Heroku, Railway, or AWS.

## How It Works
The bot uses APScheduler to schedule daily reminders at different times of the day.

Each reminder is sent as a random message from a predefined list of messages.

The Flask web server handles incoming webhook requests from Telegram.

The bot handles multiple commands to send various devotional and career-related content.

#### Scheduling Messages
The bot sends a variety of messages at specific times during the day. Here’s the schedule:

- 05:30 AM: Morning reminder to wake up and begin the day with Hanuman's blessings.

- 05:35 AM: Reminder to brush and prepare for pooja.

- 05:45 AM: Reminder to clean the pooja area.

- 05:56 AM: Bath reminder to purify the body for pooja.

- 06:00 AM: Poja preparation check (check diya, kapoor, mala).

- 06:20 AM: Time to start the pooja with Hanuman's blessings.

- 07:30 AM: Inspirational message after pooja.

- 09:40 AM: Career tip for job seekers.

- 01:10 PM: Midday thoughts for motivation.

- 03:42 PM: Afternoon reminder for continuous effort.

- 06:30 PM: Aarti reminder in the evening.

- 09:00 PM: Final thoughts and goodnight wish.

### Contributing
Feel free to fork the repository and submit pull requests. If you want to add more features or improve the bot, feel free to contribute.

### License
```bash
This project is licensed under the MIT License - see the LICENSE file for details.
```
Jai Shree Ram! 🙏
```bash
This README provides a clear and concise guide for users to set up and run the bot, contributing instructions, and an overview of the bot's functionality.
```
