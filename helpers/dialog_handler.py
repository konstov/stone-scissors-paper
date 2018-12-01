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

    session_stat = sessionStorage[session_id].copy()
    is_lizard_spock = session_stat['is_lizard_spock']

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
        sessionStorage[session_id] = helpers.round_result_encoder(session_stat, round_result)
        session_stat = sessionStorage[session_id].copy()
        remarkable_message = dialogs.remarkable_metrics(session_stat, 3)

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
        res['response']['text'], res['response']['tts'] = dialogs.statistics(session_stat)
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
        res['response']['buttons'] = helpers.get_suggests(is_base_game=not is_lizard_spock)
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

    # Если нет, то снова предлагаем сыграть
    res['response']['text'], res['response']['tts'] = dialogs.help_answer()
    res['response']['buttons'] = helpers.get_suggests(is_base_game=not is_lizard_spock)
