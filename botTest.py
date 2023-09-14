import logging
import asyncio
import telegram

# Replace 'YOUR_TOKEN' with your actual bot token
TOKEN = '5782912448:AAELn1wznXUtPmXOgQTEON8_niAuLDJrgm8'

# Replace 'YOUR_CHAT_ID' with the desired chat ID
CHAT_ID = -913473170

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

async def main():
    # Create an instance of the Telegram bot
    bot = telegram.Bot(token=TOKEN)

    # Send a simple text message
    message = "Hello from your Telegram bot!"
    await bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
