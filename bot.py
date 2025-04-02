import asyncio
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

# Bot token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Allowed users' Telegram IDs from environment variable (comma-separated string to list)
ALLOWED_USER_IDS = [int(user_id) for user_id in os.environ.get("ALLOWED_USER_IDS", "").split(",") if user_id]

# Image paths (local files in Railway)
BUYING_USDT_IMAGE_PATH = "./image.jpg"
USDT_AVAILABLE_IMAGE_PATH = "./USDT_available.jpg"

# Channel chat ID from environment variable
CHANNEL_CHAT_ID = int(os.environ.get("CHANNEL_CHAT_ID"))

# Variables for message forwarding and inline buttons
saved_message_id = None
forwarding_interval = None  # In hours
forwarding_task = None
inline_buttons = []  # Store custom inline buttons (optional)

# States for ConversationHandler
BUTTON_TEXT, BUTTON_URL = range(2)

# Define the start command that shows the menu (Custom Keyboard)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text("Sorry, you’re not authorized to use this bot.")
        return

    keyboard = [
        ["Post USDT Available", "Post Buying USDT"],
        ["Forward Message", "Stop Forwarding"],
        ["Manage Inline Buttons"],
        ["Help"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    if not context.user_data.get('has_started', False):
        await update.message.reply_text("Welcome! Choose an option from the menu below:", reply_markup=reply_markup)
        context.user_data['has_started'] = True
    else:
        try:
            await context.bot.edit_message_reply_markup(
                chat_id=update.message.chat_id,
                message_id=update.message.message_id,
                reply_markup=reply_markup
            )
        except:
            await update.message.reply_text("Main menu:", reply_markup=reply_markup)
    print("Main menu displayed")

# Function to send "Buying USDT" post (silent unless error)
async def post_buying_usdt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global saved_message_id, inline_buttons
    message = """<b>Buying USDT 💵 at the Best Rate – Limited Offer!</b>

🔒100% Secure Transactions via MCT P2P

✅️ Instant Availability | Fast & Reliable

<blockquote><b>Status:</b> Available</blockquote>

<b>Note:</b> 💎 For Serious Sellers Only – No Time Wasters!"""

    image_path = BUYING_USDT_IMAGE_PATH
    reply_markup = InlineKeyboardMarkup(inline_buttons) if inline_buttons else None

    try:
        with open(image_path, 'rb') as photo:
            message_obj = await context.bot.send_photo(
                chat_id=CHANNEL_CHAT_ID,
                photo=photo,
                caption=message,
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
        saved_message_id = message_obj.message_id
        print(f"Posted 'Buying USDT' - Message ID: {saved_message_id}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error posting 'Buying USDT': {str(e)}")

# Function to send "USDT Available" post (silent unless error)
async def post_usdt_available(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global saved_message_id, inline_buttons
    message = """<b> USDT Available 💵 at the Best Rate – Limited Offer!</b>

🔒100% Secure Transactions via MCT P2P

✅️ Instant Availability | Fast & Reliable

<blockquote><b>Status:</b> Available</blockquote>

<b>Note:</b> 💎 For Serious Buyers Only – No Time Wasters!"""

    image_path = USDT_AVAILABLE_IMAGE_PATH
    reply_markup = InlineKeyboardMarkup(inline_buttons) if inline_buttons else None

    try:
        with open(image_path, 'rb') as photo:
            message_obj = await context.bot.send_photo(
                chat_id=CHANNEL_CHAT_ID,
                photo=photo,
                caption=message,
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
        saved_message_id = message_obj.message_id
        print(f"Posted 'USDT Available' - Message ID: {saved_message_id}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error posting 'USDT Available': {str(e)}")

# Function to manage inline buttons (visible menu switch)
async def manage_inline_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["Add Inline Button", "Remove Inline Buttons"],
        ["List Inline Buttons", "Back to Main Menu"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    try:
        await context.bot.edit_message_reply_markup(
            chat_id=update.message.chat_id,
            message_id=update.message.message_id,
            reply_markup=reply_markup
        )
    except:
        await update.message.reply_text("Inline buttons menu:", reply_markup=reply_markup)
    print("Switched to inline buttons menu")

# Start adding an inline button (ConversationHandler entry point)
async def add_inline_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please enter the button text (e.g., 'Contact Admin'):")
    print("Prompted for inline button text")
    return BUTTON_TEXT

# Handle button text input
async def receive_button_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['button_text'] = update.message.text
    await update.message.reply_text(f"Button text set to '{update.message.text}'. Now enter the URL (e.g., 'https://t.me/Crypto_boysss'):")
    print("Received button text, prompted for URL")
    return BUTTON_URL

# Handle button URL input
async def receive_button_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global inline_buttons
    button_text = context.user_data.pop('button_text')
    button_url = update.message.text
    inline_buttons.append([InlineKeyboardButton(button_text, url=button_url)])
    await update.message.reply_text(f"✅ Inline button '{button_text}' added with URL '{button_url}'!")
    print(f"Added inline button: {button_text} -> {button_url}")
    return ConversationHandler.END

# Cancel the conversation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Cancelled adding inline button.")
    print("Cancelled inline button addition")
    return ConversationHandler.END

# Function to remove all inline buttons (silent)
async def remove_inline_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global inline_buttons
    inline_buttons = []
    print("Removed all inline buttons")

# Function to list current inline buttons (outputs to chat)
async def list_inline_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global inline_buttons
    if not inline_buttons:
        await update.message.reply_text("No inline buttons are currently set.")
        print("Listed inline buttons: None")
    else:
        button_list = "\n".join([f"- '{btn[0].text}' -> {btn[0].url}" for btn in inline_buttons])
        await update.message.reply_text(f"Current inline buttons:\n{button_list}")
        print(f"Listed inline buttons:\n{button_list}")

# Function to start the forwarding process (prompts for input)
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global saved_message_id, forwarding_task, forwarding_interval
    
    if saved_message_id is None:
        await update.message.reply_text("No message has been saved for forwarding. Please post a message first.")
        print("No message to forward")
        return
    
    if forwarding_task is not None:
        await update.message.reply_text("Forwarding is already running. Use 'Stop Forwarding' to stop it first.")
        print("Forwarding already active")
        return
    
    await update.message.reply_text("Please enter the interval in hours for forwarding (e.g., 24 for once a day):")
    context.user_data['waiting_for_interval'] = True
    context.user_data['chat_id'] = update.message.chat_id
    print("Prompted for forwarding interval")

# Handle the interval input (in hours)
async def handle_interval_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global forwarding_task, forwarding_interval
    
    if not context.user_data.get('waiting_for_interval', False) or update.message.chat_id != context.user_data.get('chat_id'):
        return
    
    try:
        interval_hours = int(update.message.text)
        if interval_hours <= 0:
            await update.message.reply_text("Please enter a positive number of hours!")
            print("Invalid interval: not positive")
            return
        
        forwarding_interval = interval_hours
        forwarding_task = asyncio.create_task(forward_message_loop(context, interval_hours))
        await update.message.reply_text(f"✅ Forwarding started! Message will be forwarded every {interval_hours} hour(s).")
        print(f"Forwarding started every {interval_hours} hours")
        
        context.user_data['waiting_for_interval'] = False
        context.user_data.pop('chat_id', None)
        
    except ValueError:
        await update.message.reply_text("Invalid input! Please enter a number (e.g., 24).")
        print("Invalid interval: not a number")

# Loop to forward the message at intervals (in hours)
async def forward_message_loop(context: ContextTypes.DEFAULT_TYPE, interval_hours: int) -> None:
    global saved_message_id
    try:
        while True:
            await asyncio.sleep(interval_hours * 3600)  # Convert hours to seconds
            if saved_message_id:
                try:
                    await context.bot.forward_message(
                        chat_id=CHANNEL_CHAT_ID,
                        from_chat_id=CHANNEL_CHAT_ID,
                        message_id=saved_message_id
                    )
                    print(f"Message forwarded at {interval_hours} hour interval")
                except Exception as e:
                    print(f"Error forwarding message: {e}")
    except asyncio.CancelledError:
        print("Forwarding task cancelled")
        return

# Stop the forwarding process (silent unless no task)
async def stop_forwarding(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global forwarding_task, forwarding_interval
    if forwarding_task is not None:
        forwarding_task.cancel()
        try:
            await forwarding_task
        except asyncio.CancelledError:
            pass
        forwarding_task = None
        forwarding_interval = None
        print("Forwarding stopped")
    else:
        await update.message.reply_text("No active forwarding process found.")
        print("No forwarding to stop")

# Handle custom keyboard button clicks
async def handle_custom_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    print(f"Received command: {text}")
    if text == "Post USDT Available":
        await post_usdt_available(update, context)
    elif text == "Post Buying USDT":
        await post_buying_usdt(update, context)
    elif text == "Forward Message":
        await forward_message(update, context)
    elif text == "Stop Forwarding":
        await stop_forwarding(update, context)
    elif text == "Manage Inline Buttons":
        await manage_inline_buttons(update, context)
    elif text == "Remove Inline Buttons":
        await remove_inline_buttons(update, context)
    elif text == "List Inline Buttons":
        await list_inline_buttons(update, context)
    elif text == "Back to Main Menu":
        await start(update, context)
    elif text == "Help":
        await update.message.reply_text("To use the bot, click on the options provided in the menu!")
        print("Help displayed")
    else:
        await handle_interval_input(update, context)

# Start the bot
def main() -> None:
    if not BOT_TOKEN or not ALLOWED_USER_IDS or not CHANNEL_CHAT_ID:
        raise ValueError("Missing required environment variables: BOT_TOKEN, ALLOWED_USER_IDS, or CHANNEL_CHAT_ID")
    
    application = Application.builder().token(BOT_TOKEN).build()

    # Conversation handler for adding inline buttons
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Add Inline Button"), add_inline_button)],
        states={
            BUTTON_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_button_text)],
            BUTTON_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_button_url)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_keyboard))
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
