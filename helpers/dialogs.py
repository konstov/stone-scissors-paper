from copy import deepcopy

from . import constants, helpers


# новая сессия
def new_session():
    text = """
        Привет! Сыграем в камень-ножницы-бумага! Выбирайте, камень, ножницы или бумага? 
        Скажите "Помощь" или "Что ты умеешь?", чтобы узнать все возможности игры (там есть кое-что интересное😉)."""
    tts = """
        Привет! - - - Сыграем в - камень - ножницы - бумага! Выбирайте, - - камень - -  ножницы - или - бумага? - - 
        Скаж+ите, - - помощь - - или - - что - ты - умеешь - , чтобы узнать все возможности игр+ы.
        - - там есть кое-что интересное.
    """
    blank_stats = deepcopy(constants.BLANK_STATS)

    return text, tts, blank_stats


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
            return ' Кстати, уже {} поражения подряд! Пора переломить ход игры!'.format(limit)
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

    return text, tts


# помощь
def help_answer():
    text = """
        Чтобы играть, скажите или введите с клавиатуры "камень", "ножницы" или "бумага". 
        Или отправьте один из этих эмотиконов: '✊', '✌', '✋'.
        В ответ игра пришлёт результат раунда.
        
        Чтобы сыграть в камень, ножницы, бумага, ящерица, Спок скажите "сложная игра".
        В этом режиме добавляются ящерица 🐉 и Спок 👽.
        Правила такие:
        Камень давит ящерицу и затупляет ножницы.
        Ножницы режут бумагу и обезглавливают ящерицу (бедное животное).
        Бумага опровергает Спока и оборачивает камень.
        Ящерица поедает бумагу и отравляет Спока.
        Спок разбивает ножницы и испаряет камень.
        Чтобы вернуться в вариант без ящерицы и Спока, скажите "простая игра".
        
        Чтобы узнать статистику текущей сессии, задайте вопрос, содержащий слово "статистика".
        
        Скажите "хватит", чтобы закончить игру.
    """
    tts = '\
        Чтобы играть, скажите или введите с клавиатуры - - камень - -, - - ножницы - - или - - бумага - -. \
        Или пришлите один из этих эмотиконов: - камень - , - ножницы -, - бумага -.\
        В ответ игра пришлёт результат раунда.\
        Чтобы сыграть в - камень , - ножницы , - бумага , - ящерица , - Спок - скаж+ите - - сложная - игра - - \
        В этом режиме добавляются ящерица и Спок. \
        Правила такие : \
        Камень давит ящерицу и затупляет ножницы - - . \
        Ножницы режут бумагу и обезглавливают ящерицу - - бедное животное - - . \
        Бумага опровергает Спока и оборачивает камень - - . \
        Ящерица поедает бумагу и отравляет Спока - - . \
        Спок разбивает ножницы и испаряет камень - - .\
        Чтобы вернуться в вариант без ящерицы и Спока, - - скаж+ите  - - простая - игра - - . \
        Чтобы узнать статистику текущей сессии, - задайте вопрос, содержащий слово - - - статистика - \
        Скажите - хв+атит - , чтобы закончить игр+у. \
    '

    return text, tts


def add_lizard_spock():
    text = """
    Ух ты! Вы решили сыграть в камень, ножницы, бумага, ящерица 🐉, Спок 👽!
    Напомню, что правила можно узнать по командам "Помощь" или "Что ты умеешь?"
    """

    tts = 'Ух ты! - Вы решили сыграть в камень, -  ножницы,  - бумага, - ящерица, - Спок! - \
          Напомню, что правила можно узнать по командам - - помощь - - или  - - Что ты умеешь? '

    return text, tts


def already_lizard_spock():
    text = """
    О, мы уже играем в камень, ножницы, бумага, ящерица 🐉, Спок 👽!
    Чтобы вернуться к стандартной игре камень, ножницы, бумага, скажите "простая игра".
    """

    tts = 'О! - Мы уже играем в камень, -  ножницы,  - бумага, - ящерица, - Спок! - \
          Чтобы вернуться к стандартной игре - камень, - ножницы, - бумага, скаж+ите  -- простая - игра. '

    return text, tts


def remove_lizard_spock():
    text = """
    Возвращаемся к стандартному варианту игры. 
    Теперь только ✊, ✌ и ✋, без 🐉 и 👽.
    """

    tts = 'Возвращаемся к стандартному варианту игры. - \
          Теперь только камень, - ножницы - и - бумага - , - без ящерицы - и - Спока. '

    return text, tts


def already_simple_game():
    text = """
    Да, как скажете, продолжим играть в простой вариант игры без ящерицы и Спока.
    Чтобы сыграть с ними, скажите "сложная игра".
    """

    tts = 'Да, - - как скажете,  - - продолжим играть в простой вариант игры без ящерицы и Спока - \
          Чтобы сыграть с ними, скажите  - - сложная игра. '

    return text, tts


def start_limit_game(limit):
    text = """
    Играем до {} побед!
    """.format(limit)

    tts = 'Играем до - {} - побед! '.format(limit)

    return text, tts


def to_match_numbers_in_limit_game():
    text = """
    Ой. Кажется, вы назвали более одного числа. Не знаю, что и выбрать. Повторите, пожалуйста, команду.
    """

    tts = 'Ой . - Кажется , вы назвали более одного числа . - Не знаю , - что и выбрать . - ' \
          'Повторите , - пожалуйста , - команду. '

    return text, tts


def no_numbers_in_limit_game():
    text = """
    Ну вот, всё прослушала. До скольки побед играем пропустила. Повторите, пожалуйста, команду.
    """

    tts = 'Ну вот, - всё просл+ушала. До скольк+и побед играем пропустила. Повторите , - пожалуйста , - команду. '

    return text, tts


def stats_of_limit(stats):
    if stats['wins'] > stats['looses']:
        text = """
            Счёт {}:{}, вы ведёте в матче!
            """.format(stats['wins'], stats['looses'])

        tts = 'Счёт - {} - - {} , вы ведёте в матче! '.format(stats['wins'], stats['looses'])

    elif stats['wins'] == stats['looses']:
        text = """
                    Пока ничья в матче. Счёт {}:{}.
                    """.format(stats['wins'], stats['looses'])

        tts = 'Пока ничья в матче. - Счёт - {} - - {}. '.format(stats['wins'], stats['looses'])

    else:
        text = """
                    Вы прогрываете матч со счётом {}:{}.
                    """.format(stats['wins'], stats['looses'])

        tts = 'Вы прогрываете матч со счётом - {} - - {}. '.format(stats['wins'], stats['looses'])

    return text, tts


def stats_of_limit_gameover(stats):
    if stats['wins'] > stats['looses']:
        text = """
            Матч закончился со счётом {}:{} в вашу пользу!
            """.format(stats['wins'], stats['looses'])

        tts = 'Матч закончился со счётом - {} - - {} - в вашу пользу! '.format(stats['wins'], stats['looses'])

    else:
        text = """
                    Поражение в матче со счётом {}:{}.
                    """.format(stats['wins'], stats['looses'])

        tts = 'Поражение в матче со счётом - {} - - {}. '.format(stats['wins'], stats['looses'])

    return text, tts


def new_limit_game_invitation():
    text = """
    Скажите "да", чтобы повторить матч сначала, или "нет", чтобы вернятся к обычной игре.
    """

    tts = 'Скажите - да - , чтобы повторить матч сначала, или  - нет - , чтобы вернятся к обычной игре. '

    return text, tts


def back_from_limit_to_stand_game():
    text = """
    Хорошо, играем в несоревновательный вариант, для души, так сказать. 😉
    """

    tts = 'Хорошо, - играем в несоревнов+ательный вариант, - для душ+и, так сказать. '

    return text, tts