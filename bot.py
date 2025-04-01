import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import os

BOT_TOKEN = "7770364518:AAHA7DpYLlCamqKZ9CzKmgSDG-14Q1H3fDc"
CHAT_ID = "-1001639511027"
ALLOWED_USER_IDS = [5831487417]  # Replace with your Telegram ID (e.g., 123456789)

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text("Sorry, you’re not authorized to use this bot.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /post <your message here>\nType each line separately.")
        return
    
    # Get the full message text after /post, preserving line breaks
    message = update.message.text[len("/post "):]

    # Raw image URL from GitHub
    image_url = "https://raw.githubusercontent.com/cryptoprofezor/MCTP2P-Bot/main/image.jpg"
    keyboard = [[InlineKeyboardButton("🔹 Contact Admin", url="https://t.me/Crypto_boysss")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await context.bot.send_photo(
            chat_id=CHAT_ID,
            photo=image_url,  # Using the raw GitHub URL for the image
            caption=message,
            reply_markup=reply_markup
        )
        await update.message.reply_text("Message posted successfully!")
    except Exception as e:
        # Log the error for better debugging
        print(f"Error sending photo: {e}")
        await update.message.reply_text(f"Error: {e}")

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("post", post))
    print("Bot is running... Use /post in Telegram to send messages.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
