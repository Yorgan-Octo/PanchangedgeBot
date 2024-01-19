import telebot
from telebot import types
from decouple import config

telegram_bot_token = config("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(telegram_bot_token)

followed_users = []
start_string = "Вітаю я PanchangedgeBot і я можу надіслати тобі Panchang."


@bot.message_handler(commands=['start'])
def start(message):
    markup = init_start_button(message)
    bot.send_message(message.chat.id, start_string, reply_markup=markup)


@bot.message_handler()
def button_clic(message):
    if message.text == "Сьогоднішній panchang":
        markup = init_sity_button()
        bot.send_message(message.chat.id, "Выбери необходимый город", reply_markup=markup)
    elif message.text == "Підписатися":
        followed_users.append(message.chat.id)
        markup = init_start_button(message)
        bot.send_message(message.chat.id, text="Тепер ви підписсані на щоранкову росилку panchang", reply_markup=markup)
    elif message.text == "Відписатися":
        followed_users.remove(message.chat.id)
        markup = init_start_button(message)
        bot.send_message(message.chat.id, text="Шкода що ви відписалися", reply_markup=markup)



@bot.callback_query_handler(func=lambda call:True)
def callback_sity_button(call):
    if call.message:
        if call.data == "button_kiev":
            bot.send_message(call.message.chat.id, text="киев так киев")


def init_start_button(message):
    markup = types.ReplyKeyboardMarkup()
    send_panchang = types.KeyboardButton("Сьогоднішній panchang")

    if followed_users.__contains__(message.chat.id):
        followed_button = types.KeyboardButton("Відписатися")
    else:
        followed_button = types.KeyboardButton("Підписатися")

    markup.row(send_panchang, followed_button)
    return markup

def init_sity_button():
    markup = types.InlineKeyboardMarkup(row_width=2)
    button_kiev = types.InlineKeyboardButton("Киев", callback_data="button_kiev")
    button_riga = types.InlineKeyboardButton("Львів", callback_data="button_lviv")
    markup.add(button_kiev, button_riga)
    return markup




if __name__ == '__main__':
    bot.polling()

