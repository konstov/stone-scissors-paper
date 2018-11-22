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
    if req['request']['command'].lower() in ['✊', '✌', '✋', 'ножницы', 'камень', 'бумага']:
        # Если пользователь прислал один из вариантов, то играем с ним
        res['response']['text'] = gameStatus(req['request']['command'].lower())
        res['response']['buttons'] = getSuggests(user_id)
        return

    # Если нет, то снова предлагаем сыграть
    res['response']['text'] = 'Что-то не то... Вы уверены, что хотели сказать "{0}"? Может быть вы имели ввиду "{1}"?'.\
        format(req['request']['command'], answer())
    res['response']['buttons'] = getSuggests(user_id)


# верну случайный элемент
def answer(weights=[1, 1, 1]):
    answers = ['✊', '✌', '✋']
    return choices(answers, weights=weights)[0]


def botChoiceTextMapper(bot_choice):
    if bot_choice == '✊':
        return 'камень'
    elif bot_choice == '✋':
        return 'бумагу'
    elif bot_choice == '✌':
        return 'ножницы'


def newRoundInvitation():
    phraces = ['Ещё разок?', 'Давайте ещё?', 'Играем дальше?', 'Ваш ход!']
    return choices(phraces)[0]

# результат матча
def gameStatus(user_choice, is_first=False):
    # Известно, что первыми чаще всего выкидывают ножницы (до 70 % случаев)
    if is_first:
        bot_choice = answer(weights=[1.5, 7, 1.5])
    else:
        bot_choice = answer()

    bot_choice_text = botChoiceTextMapper(bot_choice)

    if user_choice in [bot_choice, bot_choice_text]:
        phrace = 'Ничья 🤝. Игра тоже выбрала {}. '.format(bot_choice_text)

    elif (bot_choice == '✊' and user_choice in ['ножницы', '✌']) or\
         (bot_choice == '✌' and user_choice in ['бумага', '✋']) or\
         (bot_choice == '✋' and user_choice in ['камень', '✊']):
        phrace = 'Вы проиграли 😕, игра выбрала {}. '.format(bot_choice_text)

    else:
        phrace = 'Вы выиграли 🙌! Игра выбрала {}. '.format(bot_choice_text)

    return phrace + newRoundInvitation()

# Функция возвращает три подсказки для ответа.
def getSuggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем три подсказки
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:3]
    ]

    return suggests
