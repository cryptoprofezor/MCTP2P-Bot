import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

BOT_TOKEN = "7770364518:AAHA7DpYLlCamqKZ9CzKmgSDG-14Q1H3fDc"
CHAT_ID = "-1001639511027"
ALLOWED_USER_IDS = [5831487417]

# Image URLs
BUYING_IMAGE_URL = "https://raw.githubusercontent.com/cryptoprofezor/MCTP2P-Bot/main/image.jpg"
USDT_AVAILABLE_IMAGE_URL = "https://raw.githubusercontent.com/cryptoprofezor/MCTP2P-Bot/main/USDT_available.jpg"

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE, image_url: str, default_message: str) -> None:
    try:
        user_id = update.message.from_user.id
        if user_id not in ALLOWED_USER_IDS:
            await update.message.reply_text("🚫 Sorry, you’re not authorized to use this bot.")
            return
        
        # Get the full message after the command
        if context.args:
            message = " ".join(context.args)  # Join all arguments as a message
        else:
            message = default_message  # Use default message if no text is provided

        keyboard = [[InlineKeyboardButton("🔹 Contact Admin", url="https://t.me/Crypto_boysss")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_photo(
            chat_id=CHAT_ID,
            photo=image_url,  # Dynamic image selection
            caption=message,
            reply_markup=reply_markup
        )
        await update.message.reply_text("✅ Message posted successfully!")

    except Exception as e:
        logger.error(f"Error in post function: {e}")
        await update.message.reply_text(f"⚠️ Error: {e}")

async def post_buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await post(update, context, BUYING_IMAGE_URL, "**🔥 Buying USDT! Contact us now. 🔥**")

async def post_available(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await post(update, context, USDT_AVAILABLE_IMAGE_URL, "**✅ USDT Available! Get yours now. ✅**")

async def set_bot_commands(application: Application) -> None:
    commands = [
        BotCommand("postbuy", "Post 'Buying USDT' message"),
        BotCommand("postavailable", "Post 'USDT Available' message")
    ]
    await application.bot.set_my_commands(commands)

def main() -> None:
    try:
        application = Application.builder().token(BOT_TOKEN).build()

        # Set up command handlers
        application.add_handler(CommandHandler("postbuy", post_buy))
        application.add_handler(CommandHandler("postavailable", post_available))

        # Add bot menu commands
        application.post_init(set_bot_commands)

        print("🚀 Bot is running... Use the menu or commands to post.")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
