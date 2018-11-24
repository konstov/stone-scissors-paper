from random import choices

from . import constants

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
        text_answer, sound_answer = prepare_answers(bot_choice=bot_choice,
                                                    bot_choice_text_for_speech=bot_choice_text_for_speech,
                                                    isLooser=False,
                                                    roundResult='tie')

    # проигрыш
    elif (bot_choice == '✊' and user_choice in ['ножницы', '✌']) or \
            (bot_choice == '✌' and user_choice in ['бумага', '✋']) or \
            (bot_choice == '✋' and user_choice in ['камень', '✊']):

        text_answer, sound_answer = prepare_answers(bot_choice=bot_choice,
                                                    bot_choice_text_for_speech=bot_choice_text_for_speech,
                                                    isLooser=True,
                                                    roundResult='loose')

    # победа
    else:
        text_answer, sound_answer = prepare_answers(bot_choice=bot_choice,
                                                    bot_choice_text_for_speech=bot_choice_text_for_speech,
                                                    isLooser=False,
                                                    roundResult='win')

    return text_answer, sound_answer


# Функция возвращает подсказки для ответа.
def getSuggests(isBaseGame=True):
    if isBaseGame:
        return [
            {'title': suggest, 'hide': True}
            for suggest in constants.BASE_SUGGESTS
        ]

    return [
        {'title': suggest, 'hide': True}
        for suggest in constants.LIZARD_SPOCK_SUGGESTS
    ]


# сформирую составляющие итогового ответа пользователю
def create_answer_parameters(isLoose, roundResult):
    if roundResult == 'win':
        # invitation, prefix, main_phrase, game_select, emoticon, sound
        return [newRoundInvitation(isLoose=isLoose),
                choices(constants.HAPPY_PREFIXES)[0],
                choices(constants.HAPPY_MAIN_PHRASES)[0],
                choices(constants.HAPPY_GAME_SELECT)[0],
                choices(constants.HAPPY_EMOTICONS)[0],
                choices(constants.HAPPY_SOUNDS)[0]
                ]

    elif roundResult == 'tie':
        # invitation, prefix, main_phrase, game_select, emoticon, sound
        return [newRoundInvitation(isLoose=isLoose),
                choices(constants.NEUTRAL_PREFIXES)[0],
                choices(constants.NEUTRAL_MAIN_PHRASES)[0],
                choices(constants.NEUTRAL_GAME_SELECT)[0],
                choices(constants.NEUTRAL_EMOTICONS)[0],
                choices(constants.NEUTRAL_SOUNDS)[0]
                ]

    elif roundResult == 'loose':
        # invitation, prefix, main_phrase, game_select, emoticon, sound
        return [newRoundInvitation(isLoose=isLoose),
                choices(constants.SAD_PREFIXES)[0],
                choices(constants.SAD_MAIN_PHRASES)[0],
                choices(constants.SAD_GAME_SELECT)[0],
                choices(constants.SAD_EMOTICONS)[0],
                choices(constants.SAD_SOUNDS)[0]
                ]


def prepare_answers(bot_choice, bot_choice_text_for_speech, isLooser, roundResult):
    # text_answer, sound_answer
    invitation, prefix, main_phrase, game_select, emoticon, sound \
        = create_answer_parameters(isLoose=isLooser, roundResult=roundResult)

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
