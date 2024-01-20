import telebot
import json
from telebot import types
from decouple import config
from parsers.panchang_parser import panchang_parser as pr


telegram_bot_token = config("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(telegram_bot_token)

with open('data/cities.json', 'r', encoding='utf-8') as file:
    cities = json.load(file)

@bot.message_handler(commands=['start'])
def start(message):
    markup = init_start_button(message)
    bot.send_message(message.chat.id, "Вітаю я PanchangedgeBot і я можу надіслати тобі Panchang.", reply_markup=markup)


@bot.message_handler()
def button_clic(message):
    if message.text == "Сьогоднішній panchang":
        markup = init_sity_button()
        bot.send_message(message.chat.id, "Выбери необходимый город", reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def callback_sity_button(call):
    if call.message:
        for item in cities:
            if item["system_name"] == call.data:
                name_city = item["name"]
                bot.send_message(call.message.chat.id, text=f"Одну минуту формирую ответ для города {name_city}:")
                res = pr.parser_from_city_id(item["geoname_id"])
                bot.send_message(call.message.chat.id, text=res)


def init_start_button(message):
    markup = types.ReplyKeyboardMarkup()
    send_panchang = types.KeyboardButton("Сьогоднішній panchang")
    markup.row(send_panchang)
    return markup

def init_sity_button():
    markup = types.InlineKeyboardMarkup(row_width=2)

    for button in cities:
        markup.add(types.InlineKeyboardButton(text=button["name"], callback_data=button["system_name"]))
    return markup


if __name__ == '__main__':
    bot.polling()

