import telebot
from telebot import types
from decouple import config

telegram_bot_token = config("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(telegram_bot_token)

default_messages = {
    "start": "Приветсвую я PanchangedgeBot и я могу присылать тебе Panchang. Просто выбери то нужно и я все зделаю!"
}




@bot.message_handler(commands=['start'])
def start(message):
    #markup = types.InlineKeyboardMarkup(row_width=2)
    #button_kiev = types.InlineKeyboardButton("Киев", callback_data="button_kiev")
    #button_riga = types.InlineKeyboardButton("Рига", callback_data="button_riga")

    #markup.add(button_kiev,button_riga)

    markup = types.ReplyKeyboardMarkup()
    send_panchang = types.KeyboardButton("Сеголнешний panchang")
    everyday_panchang = types.KeyboardButton("Ежедневный panchang")

    markup.row(send_panchang)
    markup.row(everyday_panchang)

    bot.send_message(message.chat.id, default_messages["start"])
    on_button(message, "Сеголнешний panchang", "Ежедневный panchang")


def on_button(message, button1, button2):
    markup = types.ReplyKeyboardMarkup()
    send_panchang = types.KeyboardButton(button1)
    everyday_panchang = types.KeyboardButton(button2)

    markup.row(send_panchang)
    markup.row(everyday_panchang)
    bot.send_message(message.chat.id, "Чем помочь", reply_markup=markup)


@bot.message_handler()
def button_clic(message):
    if message.text == "Сеголнешний panchang":
        bot.send_message(message.chat.id, "конечно сейчас все будет")
    elif message.text == "Ежедневный panchang":
        bot.send_message(message.chat.id, "конечно Ежедневный")
        on_button(message, "1234", "6788")



if __name__ == '__main__':
    bot.polling()

