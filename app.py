import telebot
from config import keys, TOKEN
from extensions import CryptoConverter, APIException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = f'Привет, {message.chat.first_name}! Я Бот-конвертер валют и могу:\
        \n\
        \n- показать список доступных валют через команду /values \
        \n\
        \n- вычислить эквивалент валюты командой в следующем формате: <имя валюты>' \
        '<в какую валюту перевести> <количество переводимой валюты>\
        \n\
        \n- напомнить, что я могу через команду /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверно введены параметры или команда. Помощь /help')
        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Конвертируем {quote} в {base}, \n {amount} {quote} =' \
               f'{round(total_base, 2)} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
