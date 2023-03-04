# Module_18-Currency_Converter_Bot
https://t.me/ExchangeConverter_Bot - бот, который отправляет GET-запрос на сайт https://min_api.cryptocompare.com, взаимодействует с API и получает актуальную информацию о текущем курсе валют. Результат отправляет пользователю.

Используемые библиотеки:

- aiogram
- requests
- logging
- sqlite3
- json

Реализовано логирование в файл py_log.log и создание базы данных db.db с двумя таблицами:

users - таблица пользователей, работающих с ботом
requests - курсы валют, которыми интересовался пользователь
