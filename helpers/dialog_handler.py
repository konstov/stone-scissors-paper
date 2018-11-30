from . import dialogs, constants, helpers

# Функция для непосредственной обработки диалога.
def handle_dialog(sessionStorage, req, res):
    # user_id = req['session']['user_id'] пока насквозь пользователья хранить не буду

    # соберу данные о сессии
    session_id = req['session']['session_id'] + req['session']['user_id']

    # Обрабатываем ответ пользователя.
    user_answer = req['request']['command'].lower()

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        res['response']['text'], res['response']['tts'], res['response']['buttons'], sessionStorage[session_id] = \
            dialogs.new_session()
        return

    session_stat = sessionStorage[session_id].copy()

    # сыграть раунд
    if user_answer in constants.VALID_GAME_ANSWERS:
        # Если пользователь прислал один из вариантов, то играем с ним
        text_answer, sound_answer, round_result = helpers.game_status(req['request']['command'].lower())

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

        res['response']['buttons'] = helpers.get_suggests(is_base_game=True)
        return

    # если в запросе пользователя есть упоминание статистики, то верну статистику сессии
    elif 'статистик' in user_answer:

        res['response']['text'], res['response']['tts'], res['response']['buttons'] \
            = dialogs.statistics(session_stat)
        return

    # ответ на запрос о помощи
    elif 'помощь' in user_answer or \
            'помоги' in user_answer or \
            'возможност' in user_answer or \
            'что ты умеешь' in user_answer or \
            'ты умеешь' in user_answer or \
            'что умеешь' in user_answer or \
            'правил' in user_answer:

        res['response']['text'], res['response']['tts'], res['response']['buttons'] \
            = dialogs.help_answer()
        return

    # Если нет, то снова предлагаем сыграть
    res['response']['text'], res['response']['tts'], res['response']['buttons'] = \
        dialogs.help_answer()
        # dialogs.error_message(req['request']['command'])