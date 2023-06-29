import telebot
from time import sleep

from tinkoff.invest import Client
from errors.setup_logger import logger
from config_data.config import load_config


config = load_config()

TCS_TOKEN = config.tcs_client.token
FIGI_BOT_TOKEN = config.tg_bot.token

bot = telebot.TeleBot(FIGI_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        bot.send_message(message.chat.id,
                         "Hello, write me a ticker, i'll try to find instrument info by query")
    except Exception as e:
        logger.exception(f"Exception in start handler: \n{e}\n")
        
@bot.message_handler(func=lambda message: True)
def all_message(message):
    try:
        with Client(TCS_TOKEN) as client:
            info_all = client.instruments.find_instrument(query=message.text)
            for info in info_all.instruments:
                bot.send_message(message.chat.id, info)
                sleep(4)
    except Exception as e:
        logger.exception(f"Exception in message handler: \n{e}\n")


if __name__ == "__main__":
    while True:
        try:
            bot.polling()
        except Exception as e:
            logger.exception(f"Exception in bot polling: \n{e}\n")