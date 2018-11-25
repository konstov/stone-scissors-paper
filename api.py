# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals
from random import choices

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

# вспомотельные модули
from helpers import constants, helpers

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Хранилище данных о пользователях
# пока не прикрутил хранилище, буду работать только с текущими сессиями
# user = {}

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    # user_id = req['session']['user_id'] пока насквозь пользователья хранить не буду

    # соберу данные о сессии
    session_id = req['session']['session_id']


    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        res['response']['text'], res['response']['tts'], res['response']['buttons'], sessionStorage[session_id] =\
            helpers.new_session()
        return

    # Обрабатываем ответ пользователя.
    if req['request']['command'].lower() in constants.VALID_ANSWERS:
        # Если пользователь прислал один из вариантов, то играем с ним
        text_answer, sound_answer, round_result = helpers.gameStatus(req['request']['command'].lower())

        # Добавлю сообщение о хорошем потоке в ряд
        sessionStorage[session_id] = helpers.round_result_encoder(sessionStorage[session_id], round_result)
        remarkable_message = helpers.remarkable_metrics(sessionStorage[session_id], 3)

        if remarkable_message:
            res['response']['text'] = text_answer + remarkable_message
            res['response']['tts'] = sound_answer + remarkable_message
        else:
            res['response']['text'] = text_answer
            res['response']['tts'] = sound_answer

        res['response']['buttons'] = helpers.getSuggests(isBaseGame=True)
        return

    # Если нет, то снова предлагаем сыграть
    random_answer = helpers.answer()
    res['response']['text'] = 'Что-то не то... Вы уверены, что хотели сказать "{0}"? Может быть вы имели ввиду "{1}"?'.\
        format(req['request']['command'], random_answer)
    res['response'][
        'tts'] = 'Что-то не то. - - - Вы уверены, что хотели сказать "{0}"? Может быть вы имели ввиду "{1}"?'. \
        format(req['request']['command'], random_answer)
    res['response']['buttons'] = helpers.getSuggests(isBaseGame=True)


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


if __name__ == '__main__':
    print(helpers.remarkable_metrics({
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
