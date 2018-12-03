from random import choices
from time import time

from . import constants, dialogs

# верну случайный элемент
def answer(answers):
    return choices(answers)[0]


# возвращает начальную форму и правильное произношение
def bot_choice_text_mapper(bot_choice):
    return constants.TEXT_MAPPER[bot_choice]


def new_round_invitation(is_loose):
    if not is_loose:
        return choices(constants.NEW_ROUND_INVITATION)[0]
    else:
        return choices(constants.NEW_ROUND_INVITATION_WIN_BACK)[0]


# результат матча
def game_status(user_choice, is_lizard_spock):
    if is_lizard_spock:
        bot_choice = answer(constants.LIZARD_SPOCK_BOT_ANSWERS)
        win_and_loose = constants.LIZARD_SPOCK_WIN_AND_LOOSE
    else:
        bot_choice = answer(constants.BOT_ANSWERS)
        win_and_loose = constants.WIN_AND_LOOSE

    bot_choice_text, bot_choice_text_for_speech = bot_choice_text_mapper(bot_choice)

    # ничья
    if user_choice.lower() in [bot_choice.lower(), bot_choice_text.lower()]: # lower(), чтобы не было проблем со Споком
        round_result = 'tie'
        text_answer, sound_answer = dialogs.prepare_answers(bot_choice=bot_choice,
                                                            bot_choice_text_for_speech=bot_choice_text_for_speech,
                                                            is_looser=False,
                                                            round_result=round_result)

    # проигрыш
    elif user_choice.lower() in win_and_loose[bot_choice_text]:
        round_result = 'loose'
        text_answer, sound_answer = dialogs.prepare_answers(bot_choice=bot_choice,
                                                            bot_choice_text_for_speech=bot_choice_text_for_speech,
                                                            is_looser=True,
                                                            round_result=round_result)

    # победа
    else:
        round_result = 'win'
        text_answer, sound_answer = dialogs.prepare_answers(bot_choice=bot_choice,
                                                            bot_choice_text_for_speech=bot_choice_text_for_speech,
                                                            is_looser=False,
                                                            round_result=round_result)

    return text_answer, sound_answer, round_result


# Функция возвращает подсказки для ответа.
def get_suggests(is_base_game=True):
    if is_base_game:
        return [
            {'title': suggest, 'hide': True}
            for suggest in constants.BASE_SUGGESTS
        ]

    return [
        {'title': suggest, 'hide': True}
        for suggest in constants.LIZARD_SPOCK_SUGGESTS
    ]


def get_suggests_new_limit_game_invitation():
    return [
        {'title': 'Да!', 'hide': True},
        {'title': 'Нет!', 'hide': True}
    ]


# сформирую составляющие итогового ответа пользователю
def create_answer_parameters(is_loose, round_result):
    if round_result == 'win':
        # invitation, prefix, main_phrase, game_select, emoticon, sound
        return [new_round_invitation(is_loose=is_loose),
                choices(constants.HAPPY_PREFIXES)[0],
                choices(constants.HAPPY_MAIN_PHRASES)[0],
                choices(constants.HAPPY_GAME_SELECT)[0],
                choices(constants.HAPPY_EMOTICONS)[0],
                choices(constants.HAPPY_SOUNDS)[0]
                ]

    elif round_result == 'tie':
        # invitation, prefix, main_phrase, game_select, emoticon, sound
        return [new_round_invitation(is_loose=is_loose),
                choices(constants.NEUTRAL_PREFIXES)[0],
                choices(constants.NEUTRAL_MAIN_PHRASES)[0],
                choices(constants.NEUTRAL_GAME_SELECT)[0],
                choices(constants.NEUTRAL_EMOTICONS)[0],
                choices(constants.NEUTRAL_SOUNDS)[0]
                ]

    elif round_result == 'loose':
        # invitation, prefix, main_phrase, game_select, emoticon, sound
        return [new_round_invitation(is_loose=is_loose),
                choices(constants.SAD_PREFIXES)[0],
                choices(constants.SAD_MAIN_PHRASES)[0],
                choices(constants.SAD_GAME_SELECT)[0],
                choices(constants.SAD_EMOTICONS)[0],
                choices(constants.SAD_SOUNDS)[0]
                ]


def round_result_encoder(session_state, round_result):
    if round_result == 'win':
        session_state['wins'] += 1
        session_state['wins_in_row'] += 1
        session_state['looses_in_row'] = 0
        session_state['ties_in_row'] = 0
        session_state['last_query_moment'] = time()
        if session_state['limit_of_game']:
            session_state['limit_game_score']['wins'] += 1
        return session_state

    elif round_result == 'tie':
        session_state['ties'] += 1
        session_state['ties_in_row'] += 1
        session_state['wins_in_row'] = 0
        session_state['looses_in_row'] = 0
        session_state['last_query_moment'] = time()
        return session_state

    elif round_result == 'loose':
        session_state['looses'] += 1
        session_state['looses_in_row'] += 1
        session_state['ties_in_row'] = 0
        session_state['wins_in_row'] = 0
        session_state['last_query_moment'] = time()
        if session_state['limit_of_game']:
            session_state['limit_game_score']['looses'] += 1
        return session_state


def get_stars():
    return [{'title': 'Оцените, если понравилось 😉',
            'hide': False,
            'url': 'https://dialogs.yandex.ru/store/skills/09946070-kamen-nozhnicy-bumag'
            }]


def limit_game(session_state):

    return session_state