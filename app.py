import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN) # инициализация бота

welcome_text = 'Чтобы начать работу, введите команду в следующем формате: \
    \n<название валюты>\
    <в какую валюту перевести>\
    <количество переводимой валюты>\
    \n\nПример: евро рубль 1\
    \n\nОтобразить список всех доступных валют: /values'

@bot.message_handler(commands=['start', 'help'])
# функция начала работы
def welcome_message(message: telebot.types.Message):
    bot.reply_to(message, welcome_text)

# функция отображения доступных валют
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

# функиця конвертации валют
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3: # если параметров больше 3
            raise ConvertionException('Вы ввели слишком много параметров. Чтобы напомнить, как выполнять конвертацию, нажмите /help')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
        price = float(amount) * total_base
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {price}'
        bot.send_message(message.chat.id, text)

bot.polling()