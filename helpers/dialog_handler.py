from copy import deepcopy

from . import dialogs, constants, helpers

# Функция для непосредственной обработки диалога.
def handle_dialog(sessionStorage, req, res):
    # соберу данные о сессии
    session_id = req['session']['session_id'] + req['session']['user_id']

    # Обрабатываем ответ пользователя.
    user_answer = req['request']['command'].lower()

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        res['response']['text'], res['response']['tts'], sessionStorage[session_id] = \
            dialogs.new_session()
        res['response']['buttons'] = helpers.get_suggests(is_base_game=True)
        return

    is_lizard_spock = sessionStorage[session_id]['is_lizard_spock']

    if not is_lizard_spock:
        valid_game_answers = constants.VALID_GAME_ANSWERS

    else:
        valid_game_answers = constants.LIZARD_SPOCK_VALID_GAME_ANSWERS

    # сыграть раунд
    if user_answer in valid_game_answers:
        # Если пользователь прислал один из вариантов, то играем с ним
        text_answer, sound_answer, round_result = helpers.game_status(req['request']['command'].lower(),
                                                                      is_lizard_spock)
        # Добавлю сообщение о хорошем потоке 3 в ряд
        sessionStorage[session_id] = helpers.round_result_encoder(sessionStorage[session_id], round_result)

        # если игра лимитная
        if sessionStorage[session_id]['limit_of_game']:

            # если кто-то победил в лимитной игре
            if sessionStorage[session_id]['limit_game_score']['wins'] == sessionStorage[session_id]['limit_of_game'] or\
                sessionStorage[session_id]['limit_game_score']['looses'] == sessionStorage[session_id]['limit_of_game']:

                stats_of_limit, stats_of_limit_speech = dialogs.stats_of_limit_gameover(
                    sessionStorage[session_id]['limit_game_score'])
                sessionStorage[session_id]['limit_game_is_ended'] = True

                new_limit_game_inv, new_limit_game_inv_speech = dialogs.new_limit_game_invitation()

                res['response']['text'] = text_answer + stats_of_limit + new_limit_game_inv
                res['response']['tts'] = sound_answer + stats_of_limit_speech + new_limit_game_inv_speech
                res['response']['buttons'] = helpers.get_suggests_new_limit_game_invitation()

            # лимитная игра продолжается
            else:
                stats_of_limit, stats_of_limit_speech = dialogs.stats_of_limit(
                    sessionStorage[session_id]['limit_game_score'])

                res['response']['text'] = text_answer + stats_of_limit
                res['response']['tts'] = sound_answer + stats_of_limit_speech

                res['response']['buttons'] = helpers.get_suggests(is_base_game=not is_lizard_spock)

        # свободная игра
        else:
            remarkable_message = dialogs.remarkable_metrics(sessionStorage[session_id], 3)
            if remarkable_message:
                res['response']['text'] = text_answer + remarkable_message
                res['response']['tts'] = sound_answer + remarkable_message
            else:
                res['response']['text'] = text_answer
                res['response']['tts'] = sound_answer

            res['response']['buttons'] = helpers.get_suggests(is_base_game=not is_lizard_spock)
        return

    # если в запросе пользователя есть упоминание статистики, то верну статистику сессии
    elif 'статистик' in user_answer:
        res['response']['text'], res['response']['tts'] = dialogs.statistics(sessionStorage[session_id])
        res['response']['buttons'] = helpers.get_suggests(is_base_game=not is_lizard_spock)
        return

    # ответ на запрос о помощи
    elif 'помощь' in user_answer or \
            'помоги' in user_answer or \
            'возможност' in user_answer or \
            'что ты умеешь' in user_answer or \
            'ты умеешь' in user_answer or \
            'что умеешь' in user_answer or \
            'правил' in user_answer:

        res['response']['text'], res['response']['tts'] = dialogs.help_answer()
        res['response']['buttons'] = helpers.get_stars() + helpers.get_suggests(is_base_game=not is_lizard_spock)

        return

    # осознанное переключением пользователем на сложный вариант игры
    elif 'непростая игра' in user_answer or \
        'сложная игра' in user_answer:
        # поставлю метку расширенной игры
        if not is_lizard_spock:
            sessionStorage[session_id]['is_lizard_spock'] = True

            res['response']['text'], res['response']['tts'] = dialogs.add_lizard_spock()
            res['response']['buttons'] = helpers.get_suggests(is_base_game=False)
            return

        res['response']['text'], res['response']['tts'] = dialogs.already_lizard_spock()
        res['response']['buttons'] = helpers.get_suggests(is_base_game=False)
        return

    # если пользовать упомянет ящерицу или Спока в простом варианте игры, то команда не будет отработана как валидная
    # переключу в сложный режим
    elif 'ящериц' in user_answer or \
        'спок' in user_answer:
        sessionStorage[session_id]['is_lizard_spock'] = True

        res['response']['text'], res['response']['tts'] = dialogs.add_lizard_spock()
        res['response']['buttons'] = helpers.get_suggests(is_base_game=False)
        return

    # возврат к простому варианту игры
    elif 'обычная игра' in user_answer or \
            'простая игра' in user_answer:
        # поставлю метку расширенной игры
        if is_lizard_spock:
            sessionStorage[session_id]['is_lizard_spock'] = False

            res['response']['text'], res['response']['tts'] = dialogs.remove_lizard_spock()
            res['response']['buttons'] = helpers.get_suggests(is_base_game=True)
            return

        res['response']['text'], res['response']['tts'] = dialogs.already_simple_game()
        res['response']['buttons'] = helpers.get_suggests(is_base_game=True)
        return

    # игра до определённого предела
    # проверяю, что есть число, притом только 1
    # and len(req['nlu']['entities']) == 1 \
    elif ('играть до' in user_answer or 'до ' in user_answer) \
            and 'побед' in user_answer \
            and len(req['request']['nlu']['entities']) == 1 \
            and req['request']['nlu']['entities'][0]['type'] == 'YANDEX.NUMBER':

        sessionStorage[session_id]['limit_of_game'] = req['request']['nlu']['entities'][0]['value']
        res['response']['text'], res['response']['tts'] = \
            dialogs.start_limit_game(sessionStorage[session_id]['limit_of_game'])
        res['response']['buttons'] = helpers.get_suggests(is_base_game=not is_lizard_spock)
        return

    # спрошу, хочет ли пользователь сыграть ещё раз лимитную игру
    # если да, то сохраню лимит и сброшу счёт
    elif user_answer in ['да', 'да!', 'Да', 'Да!'] and sessionStorage[session_id]['limit_game_is_ended'] == True:
        # сброшу состояние матча
        sessionStorage[session_id]['limit_game_score'] = {'wins': 0, 'looses': 0}
        sessionStorage[session_id]['limit_game_is_ended'] = False

        res['response']['text'], res['response']['tts'] = \
            dialogs.start_limit_game(sessionStorage[session_id]['limit_of_game'])
        res['response']['buttons'] = helpers.get_suggests(is_base_game=not is_lizard_spock)
        return

    # если нет, то вернусь к стандартной игре
    elif user_answer in ['нет', 'нет!', 'Нет!', 'Нет'] and sessionStorage[session_id]['limit_game_is_ended'] == True:
        # сброшу состояние матча
        sessionStorage[session_id]['limit_game_score'] = {'wins': 0, 'looses': 0}
        sessionStorage[session_id]['limit_game_is_ended'] = False
        sessionStorage[session_id]['limit_of_game'] = None

        res['response']['text'], res['response']['tts'] = dialogs.back_from_limit_to_stand_game()
        res['response']['buttons'] = helpers.get_suggests(is_base_game=not is_lizard_spock)
        return

    # Если нет, то снова предлагаем сыграть
    res['response']['text'], res['response']['tts'] = dialogs.help_answer()
    res['response']['buttons'] = helpers.get_stars() + helpers.get_suggests(is_base_game=not is_lizard_spock)
