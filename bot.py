import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

# Replace with your bot token from BotFather
BOT_TOKEN = "7770364518:AAHA7DpYLlCamqKZ9CzKmgSDG-14Q1H3fDc"
ADMIN_USERNAME = "@CryptoNithis"
CHAT_ID = "-1001639511027"  # Assuming this is correct now; adjust if needed

# Initialize bot
bot = Bot(token=BOT_TOKEN)

async def send_message_with_image():
    image_path = "/home/mrcryptotamilan/MCTP2P-Bot/image.jpg"

    # Caption with your exact message
    caption = (
        "Buying USDT 💵 @ Best Rate\n\n"
        "DM:- @Crypto_boysss ✔️\n\n"
        "Safe and Secure By MCT P2P\n\n"
        "Note:- Plz Only DM If Your Serious Seller"
    )

    # Inline button linking to admin
    keyboard = [[InlineKeyboardButton("🔹 Contact Admin", url="https://t.me/Crypto_boysss")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send photo with caption and inline button
    try:
        with open(image_path, "rb") as photo:
            await bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=caption, reply_markup=reply_markup)
    except FileNotFoundError:
        print("Error: Image file not found. Please check the file path.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(send_message_with_image())