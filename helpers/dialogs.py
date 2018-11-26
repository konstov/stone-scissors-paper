from . import constants, helpers


# новая сессия
def new_session():
    text = """
        Привет! Сыграем в камень-ножницы-бумага! Выбирайте, камень, ножницы или бумага? 
        Скажитe "помоги", чтобы узнать все возможности игры."""
    tts = """
        Привет! - - - Сыграем в камень ножницы бумага! Выбирайте, камень, ножницы или бумага? - - 
        Скажитe - - помоги - - , чтобы узнать все возможности игры.
    """
    buttons = helpers.get_suggests(is_base_game=True)
    blank_stats = constants.BLANK_STATS

    return text, tts, buttons, blank_stats


# подготовка ответов
def prepare_answers(bot_choice, bot_choice_text_for_speech, is_looser, round_result):
    # text_answer, sound_answer
    invitation, prefix, main_phrase, game_select, emoticon, sound \
        = helpers.create_answer_parameters(is_loose=is_looser, round_result=round_result)

    return ['{}{}{}{}{}. {}'.format(prefix,
                                    main_phrase,
                                    emoticon,
                                    game_select,
                                    bot_choice,
                                    invitation
                                    ),

            '{} - - - {}{} - - - {}{}. {}'.format(sound,
                                                  prefix,
                                                  main_phrase,
                                                  game_select,
                                                  bot_choice_text_for_speech,
                                                  invitation
                                                  )
            ]


# Функция для проверки рядов событий, можно указать длину ряда повторяющихся событий и получить сообщение,
# если выполняется.
def remarkable_metrics(session_state, limit):
    if limit < 5:
        if session_state['wins_in_row'] == limit:
            return ' Кстати, уже {} победы к ряду! Это тянет на рекорд!'.format(limit)
        elif session_state['ties_in_row'] == limit:
            return ' Кстати, уже {} ничьи подряд. Надо начинать побеждать!'.format(limit)
        elif session_state['looses_in_row'] == limit:
            return ' Уже {} поражения подряд! Пора переломить ход игры!'.format(limit)
        return ''

    else:
        if session_state['wins_in_row'] == limit:
            return ' Кстати, уже {} побед к ряду! Это тянет на рекорд!'.format(limit)
        elif session_state['ties_in_row'] == limit:
            return ' Кстати, уже {} ничьих подряд. Надо побеждать!'.format(limit)
        elif session_state['looses_in_row'] == limit:
            return ' Кстати, уже {} поражений подряд! Пора переломить ход игры!'.format(limit)
        return ''


# статистика
def statistics(session_state):
    text = 'Побед: {}, ничьих: {}, поражений: {}.'.format(session_state['wins'],
                                                          session_state['ties'],
                                                          session_state['looses'])

    tts = 'Побед - - {} - - - -, ничьих - - {} - - - -, поражений - - {}'.format(session_state['wins'],
                                                                                 session_state['ties'],
                                                                                 session_state['looses'])

    return text, tts, helpers.get_suggests(is_base_game=True)


# помощь
def help_answer():
    text = """
        Чтобы играть, скажите или введите с клавиатуры "камень", "ножницы" или "бумага". 
        Или отправьте один из этих эмотиконов: '✊', '✌', '✋'.
        В ответ игра пришлёт результат раунда.
        Чтобы узнать статистику текущей сессии, задайте вопрос, содержащий слово "статистика".
    """
    tts = '\
        Чтобы играть, скажите или введите с клавиатуры - - камень - -, - - ножницы - - или - - бумага - -. \
        Или пришлите один из этих эмотиконов: - камень - , - ножницы -, - бумага -.\
        В ответ игра пришлёт результат раунда.\
        Чтобы узнать статистику текущей сессии, - задайте вопрос, содержащий слово - - - статистика - - -.\
    '

    return text, tts, helpers.get_suggests(is_base_game=True)


def error_message(request_command):
    random_answer, random_answer_tts = helpers.bot_choice_text_mapper(helpers.answer())

    text = 'Что-то не то... Вы уверены, что хотели сказать "{0}"? Может быть вы имели ввиду "{1}"?'.\
        format(request_command, random_answer)

    tts = 'Что-то не то. - - - Вы уверены, что хотели сказать "{0}"? Может быть вы имели ввиду "{1}"?'. \
        format(request_command, random_answer_tts)

    return text, tts, helpers.get_suggests(is_base_game=True)
