from random import choices

from . import constants, dialogs

# верну случайный элемент
def answer(weights=[1, 1, 1]):
    answers = ['✊', '✌', '✋']
    return choices(answers, weights=weights)[0]


# возвращает начальную форму и правильное произношение
def bot_choice_text_mapper(bot_choice):
    if bot_choice == '✊':
        return 'камень', 'камень'
    elif bot_choice == '✋':
        return 'бумага', 'бумагу'
    elif bot_choice == '✌':
        return 'ножницы', 'ножницы'


def new_round_invitation(is_loose):
    if not is_loose:
        return choices(constants.NEW_ROUND_INVITATION)[0]
    else:
        return choices(constants.NEW_ROUND_INVITATION_WIN_BACK)[0]


# результат матча
def game_status(user_choice, is_first=False):
    # Известно, что первыми чаще всего выкидывают ножницы (до 70 % случаев)
    if is_first:
        bot_choice = answer(weights=[1.5, 7, 1.5])
    else:
        bot_choice = answer()

    bot_choice_text, bot_choice_text_for_speech = bot_choice_text_mapper(bot_choice)

    # ничья
    if user_choice in [bot_choice, bot_choice_text]:
        round_result = 'tie'
        text_answer, sound_answer = dialogs.prepare_answers(bot_choice=bot_choice,
                                                            bot_choice_text_for_speech=bot_choice_text_for_speech,
                                                            is_looser=False,
                                                            round_result=round_result)

    # проигрыш
    elif user_choice in constants.WIN_AND_LOOSE[bot_choice_text]:
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
        return session_state

    elif round_result == 'tie':
        session_state['ties'] += 1
        session_state['ties_in_row'] += 1
        session_state['wins_in_row'] = 0
        session_state['looses_in_row'] = 0
        return session_state

    elif round_result == 'loose':
        session_state['looses'] += 1
        session_state['looses_in_row'] += 1
        session_state['ties_in_row'] = 0
        session_state['wins_in_row'] = 0
        return session_state
