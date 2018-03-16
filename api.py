# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals
from random import choices

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}
# Хранилище данных о пользователях
user = {}

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

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "камень",
                "ножницы",
                "бумага",
            ]
        }

        res['response']['text'] = 'Привет! Сыграем в камень-ножницы-бумага!'
        res['response']['buttons'] = getSuggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    if req['request']['command'].lower() in [
        'камень',
        'ножницы',
        'бумага',
    ]:
        # Если пользователь прислал один из вариантов, то играем с ним
        res['response']['text'] = gameStatus(req['request']['command'].lower())
        res['response']['buttons'] = getSuggests(user_id)
        return

    # Если нет, то снова предлагаем сыграть
    res['response']['text'] = 'Что-то не то... Ты уверен, что хотел сказать "{0}"? Может быть ты имел ввиду "{1}"?'.\
        format(req['request']['command'], answer())
    res['response']['buttons'] = getSuggests(user_id)


# верну случайный элемент
def answer(weights=[1, 1, 1]):
    answers = ['камень', 'ножницы', 'бумага']
    return choices(answers, weights=weights)[0]


# результат матча
def gameStatus(user_choice, is_first=False):
    # Известно, что первыми чаще всего выкидывают ножницы (до 70 % случаев)
    if is_first:
        bot_choice = answer(weights=[1.5, 7, 1.5])
    else:
        bot_choice = answer()
    if bot_choice == user_choice:
        return 'Ничья. Игра тоже выбрала {}.'.format(bot_choice)
    elif (bot_choice == 'камень' and user_choice == 'ножницы') or\
         (bot_choice == 'ножницы' and user_choice == 'бумага') or\
         (bot_choice == 'бумага' and user_choice == 'камень'):
        return 'Вы проиграли =(, игра выбрала {}.'.format(bot_choice)
    else:
        return 'Вы выиграли! Игра выбрала {}.'.format(bot_choice)


# Функция возвращает три подсказки для ответа.
def getSuggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:3]
    ]

    return suggests
