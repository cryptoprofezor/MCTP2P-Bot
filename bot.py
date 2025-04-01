import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, JobQueue
import os
import logging

BOT_TOKEN = "7770364518:AAHA7DpYLlCamqKZ9CzKmgSDG-14Q1H3fDc"
CHAT_ID = "-1001639511027"
ALLOWED_USER_IDS = [5831487417]  # Replace with your Telegram ID (e.g., 123456789)

# Buying post message and image URL
BUYING_IMAGE_URL = "https://raw.githubusercontent.com/cryptoprofezor/MCTP2P-Bot/main/image.jpg"
BUYING_MESSAGE = "Buy USDT Now! Available at best rates!"

# USDT Available post message and image URL
USDT_AVAILABLE_IMAGE_URL = "https://raw.githubusercontent.com/cryptoprofezor/MCTP2P-Bot/main/USDT_available.jpg"  # Replace with correct image URL
USDT_AVAILABLE_MESSAGE = "USDT Available Now! Check out the latest stock."

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

async def post(update: Update = None, context: ContextTypes.DEFAULT_TYPE = None, message: str = None, image_url: str = None) -> None:
    """Helper function to send posts with messages and images"""
    try:
        if update:
            user_id = update.message.from_user.id
            if user_id not in ALLOWED_USER_IDS:
                await update.message.reply_text("Sorry, you’re not authorized to use this bot.")
                return
            if not context.args:
                await update.message.reply_text("Usage: /post <your message here>\nType each line separately.")
                return
        
            # Get the full message text after /post, preserving line breaks
            message = update.message.text[len("/post "):]

        # If message or image_url is not provided, fall back to defaults
        message = message or BUYING_MESSAGE  # Default to buying message if none provided
        image_url = image_url or BUYING_IMAGE_URL  # Default to buying image if none provided

        # Create the keyboard for admin contact
        keyboard = [[InlineKeyboardButton("🔹 Contact Admin", url="https://t.me/Crypto_boysss")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_photo(
            chat_id=CHAT_ID,
            photo=image_url,  # Using the provided image URL
            caption=message,
            reply_markup=reply_markup
        )
        
        if update:
            await update.message.reply_text("Message posted successfully!")

    except Exception as e:
        logger.error(f"Error in post function: {e}")
        if update:
            await update.message.reply_text(f"Error: {e}")

async def scheduled_buying_post(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Function to post the Buying message every 6 hours"""
    try:
        await post(context=context, message=BUYING_MESSAGE, image_url=BUYING_IMAGE_URL)
    except Exception as e:
        logger.error(f"Error in scheduled post: {e}")

def main() -> None:
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Set up the JobQueue
        job_queue = application.job_queue

        # Schedule the Buying post to run every 6 hours
        job_queue.run_repeating(scheduled_buying_post, interval=6 * 60 * 60, first=0)

        # Adding the /post command handler (manual post)
        application.add_handler(CommandHandler("post", post))

        print("Bot is running... Use /post in Telegram to send messages.")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
