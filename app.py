from aiogram import Bot, Dispatcher, executor, types
from config import AllConfiguration
from extensions import ConvertionException, CryptoConverter
from connect_db import db_connection, new_user, table_requests, record_result

import logging

# инициализация бота
bot = Bot(token=AllConfiguration.TOKEN)
db = Dispatcher(bot)

# логирование в файл py_log.log в режиме перезаписи при каждом запуске бота с указанием времени
logging.basicConfig(level=logging.INFO, filename='py_log.log', filemode='w', format='%(asctime)s %(levelname)s %(message)s')


# обработка команд /start и /help
@db.message_handler(commands=['start', 'help'])
async def welcome_message(message: types.Message):
    logging.info(f'Пользователь {message.from_user.full_name} активировал бота')
    await bot.send_message(message.from_user.id, AllConfiguration.welcome_text)
    logging.info(f'Бот отправил пользователю {message.from_user.full_name} приветственное сообщение')
    await db_connection()
    await new_user(user_id=message.from_user.id, user_name=message.from_user.full_name)
    await table_requests()


# обработка команды /currencies. Отображение доступных валют
@db.message_handler(commands=['currencies'])
async def list_currencies(message: types.Message):
    logging.info(f'Пользователь {message.from_user.full_name} активировал команду /currencies')
    text = 'Доступные валюты: '
    for key in AllConfiguration.keys.keys():
        text = '\n'.join((text, key))
    await bot.send_message(message.from_user.id, text)
    logging.info(f'Бот отправил ответ пользователю {message.from_user.full_name}')

# функиця конвертации валют
@db.message_handler(content_types=['text'])
async def convert(message: types.Message):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл сообщение {message.text}')

    try:
        values = message.text.split(' ')

        # если кол-во параметров != 3
        if len(values) != 3:
            logging.warning(f'Введено неверное количество параметров: {values} != 3')
            raise ConvertionException('Вы ввели неверное количество параметров. Чтобы напомнить, как выполнять конвертацию, нажмите /help')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
        price = float(amount) * total_base
    except ConvertionException as e:
        await bot.send_message(message.from_user.id, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        await bot.send_message(message.from_user.id, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {price}'
        await bot.send_message(message.from_user.id, text)
        logging.info(f'Пользователь {message.from_user.full_name} получил ответ: {price}')
        await record_result(first_param=quote, second_param=base, third_param=amount, result=price)

executor.start_polling(db, skip_updates=True)