# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
from time import time

# мои вспомотельные модули
from helpers import constants, helpers, dialogs, dialog_handler

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    # Чищу словарь от неиспользуемых сессий
    # Убиваю сессию, неактивную более 5 минут среди первых пяти
    # иначе, чтобы не тянуть время ответа, двигаюсь дальше
    for index, kv in enumerate(sessionStorage.items()):
        try:
            if time() - kv[1]['last_query_moment'] > 900:
                del sessionStorage[kv[0]]
                break
            if index > 5:
                break
        except:
            pass

    dialog_handler.handle_dialog(sessionStorage, request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


# немного потестим
if __name__ == '__main__':
    print(dialogs.remarkable_metrics({
        'wins': 0,
        'ties': 0,
        'looses': 0,
        'wins_in_row': 3,
        'ties_in_row': 0,
        'looses_in_row': 0
    },
        3))

    print(helpers.round_result_encoder({
        'wins': 0,
        'ties': 0,
        'looses': 0,
        'wins_in_row': 3,
        'ties_in_row': 0,
        'looses_in_row': 0
    }, 'loose'))

    print(dialogs.statistics({
        'wins': 0,
        'ties': 2,
        'looses': 0,
        'wins_in_row': 3,
        'ties_in_row': 0,
        'looses_in_row': 0
    }))

    print(dialogs.help_answer())