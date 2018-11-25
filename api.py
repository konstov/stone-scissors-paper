# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

# мои вспомотельные модули
from helpers import constants, helpers, dialogs

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}


# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    # user_id = req['session']['user_id'] пока насквозь пользователья хранить не буду

    # соберу данные о сессии
    session_id = req['session']['session_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        res['response']['text'], res['response']['tts'], res['response']['buttons'], sessionStorage[session_id] = \
            dialogs.new_session()
        return

    # Обрабатываем ответ пользователя.
    user_answer = req['request']['command'].lower()

    # сыграть раунд
    if user_answer in constants.VALID_GAME_ANSWERS:
        # Если пользователь прислал один из вариантов, то играем с ним
        text_answer, sound_answer, round_result = helpers.game_status(req['request']['command'].lower())

        # Добавлю сообщение о хорошем потоке 3 в ряд
        sessionStorage[session_id] = helpers.round_result_encoder(sessionStorage[session_id], round_result)
        remarkable_message = dialogs.remarkable_metrics(sessionStorage[session_id], 3)

        if remarkable_message:
            res['response']['text'] = text_answer + remarkable_message
            res['response']['tts'] = sound_answer + remarkable_message
        else:
            res['response']['text'] = text_answer
            res['response']['tts'] = sound_answer

        res['response']['buttons'] = helpers.get_suggests(is_base_game=True)
        return

    # если в запросе пользователя есть упоминание статистики, то верну статистику сессии
    elif 'статистик' in user_answer:

        res['response']['text'], res['response']['tts'], res['response']['buttons'] \
            = dialogs.statistics(sessionStorage[session_id])
        return

    # ответ на запрос о помощи
    elif 'помощь' in user_answer or \
            'помоги' in user_answer or \
            'возможност' in user_answer or \
            'правил' in user_answer:

        res['response']['text'], res['response']['tts'], res['response']['buttons'] \
            = dialogs.help_answer()
        return

    # Если нет, то снова предлагаем сыграть
    res['response']['text'], res['response']['tts'], res['response']['buttons'] = \
        dialogs.error_message(req['request']['command'])


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
