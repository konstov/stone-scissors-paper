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

# Импортирую свои модули
from helpers import constants

# некоторый набор констант, чтобы было удобно править их


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
                "бумага"
            ]
        }

        res['response']['text'] = 'Привет! Сыграем в камень-ножницы-бумага!'
        res['response']['tts'] = 'Привет! - - - Сыграем в камень ножницы бумага!'
        res['response']['buttons'] = getSuggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    if req['request']['command'].lower() in constants.TRUE_ANSWERS:
        # Если пользователь прислал один из вариантов, то играем с ним
        text_answer, sound_answer = gameStatus(req['request']['command'].lower())

        res['response']['text'] = text_answer
        res['response']['tts'] = sound_answer
        res['response']['buttons'] = getSuggests(user_id)
        return

    # Если нет, то снова предлагаем сыграть
    random_answer = answer()
    res['response']['text'] = 'Что-то не то... Вы уверены, что хотели сказать "{0}"? Может быть вы имели ввиду "{1}"?'. \
        format(req['request']['command'], random_answer)
    res['response'][
        'tts'] = 'Что-то не то. - - - Вы уверены, что хотели сказать "{0}"? Может быть вы имели ввиду "{1}"?'. \
        format(req['request']['command'], random_answer)
    res['response']['buttons'] = getSuggests(user_id)


# верну случайный элемент
def answer(weights=[1, 1, 1]):
    answers = ['✊', '✌', '✋']
    return choices(answers, weights=weights)[0]


# возвращает начальную форму и правильное произношение
def botChoiceTextMapper(bot_choice):
    if bot_choice == '✊':
        return 'камень', 'камень'
    elif bot_choice == '✋':
        return 'бумага', 'бумагу'
    elif bot_choice == '✌':
        return 'ножницы', 'ножницы'


def newRoundInvitation(isLoose):
    if not isLoose:
        return choices(constants.NEW_ROUND_INVITATION)[0]
    else:
        return choices(constants.NEW_ROUND_INVITATION_WIN_BACK)[0]


# результат матча
def gameStatus(user_choice, is_first=False):
    # Известно, что первыми чаще всего выкидывают ножницы (до 70 % случаев)
    if is_first:
        bot_choice = answer(weights=[1.5, 7, 1.5])
    else:
        bot_choice = answer()

    bot_choice_text, bot_choice_text_for_speech = botChoiceTextMapper(bot_choice)

    # ничья
    if user_choice in [bot_choice, bot_choice_text]:
        invitation = newRoundInvitation(isLoose=False)
        prefix = choices(constants.NEUTRAL_PREFIXES)[0]
        main_phrase = choices(constants.NEUTRAL_MAIN_PHRASES)[0]
        emoticon = choices(constants.NEUTRAL_EMOTICONS)[0]
        sound = choices(constants.NEUTRAL_SOUNDS)[0]

        text_answer = '{}{}{} Игра тоже выбрала {}. '.format(prefix,
                                                             main_phrase,
                                                             emoticon,
                                                             bot_choice
                                                            )
        sound_answer = '{} - - - {}{} - - - Игра тоже выбрала {}. {}'.format(sound,
                                                                             prefix,
                                                                             main_phrase,
                                                                             bot_choice_text_for_speech,
                                                                             invitation
                                                                            )


    # прогирыш
    elif (bot_choice == '✊' and user_choice in ['ножницы', '✌']) or \
            (bot_choice == '✌' and user_choice in ['бумага', '✋']) or \
            (bot_choice == '✋' and user_choice in ['камень', '✊']):
        invitation = newRoundInvitation(isLoose=True)
        prefix = choices(constants.SAD_PREFIXES)[0]
        main_phrase = choices(constants.SAD_MAIN_PHRASES)[0]
        emoticon = choices(constants.SAD_EMOTICONS)[0]
        sound = choices(constants.SAD_SOUNDS)[0]

        text_answer = '{}{}{}, игра выбрала {}. '.format(prefix,
                                                         main_phrase,
                                                         emoticon,
                                                         bot_choice
                                                         )
        sound_answer = '{} - - - {}{} - - - Игра выбрала {}. {}'.format(sound,
                                                                        prefix,
                                                                        main_phrase,
                                                                        bot_choice_text_for_speech,
                                                                        invitation
                                                                        )


    # победа
    else:
        invitation = newRoundInvitation(isLoose=False)
        prefix = choices(constants.HAPPY_PREFIXES)[0]
        main_phrase = choices(constants.HAPPY_MAIN_PHRASES)[0]
        emoticon = choices(constants.HAPPY_EMOTICONS)[0]
        sound = choices(constants.HAPPY_SOUNDS)[0]
        text_answer = '{}{}{} Игра выбрала {}. '.format(prefix,
                                                        main_phrase,
                                                        emoticon,
                                                        bot_choice
                                                        )
        sound_answer = '{} - - - {}{} - - - Игра выбрала {}. {}'.format(sound,
                                                                        prefix,
                                                                        main_phrase,
                                                                        bot_choice_text_for_speech,
                                                                        invitation
                                                                        )

    return text_answer + invitation, sound_answer


# Функция возвращает три подсказки для ответа.
def getSuggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем три подсказки
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:3]
    ]

    return suggests
