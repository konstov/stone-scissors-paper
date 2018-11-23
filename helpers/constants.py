# приглашения сыграть дальше
NEW_ROUND_INVITATION = ['Ещё разок?', 'Давайте ещё?', 'Играем дальше?', 'Ваш ход!', 'Продолжим?', 'Разовьём успех?']
NEW_ROUND_INVITATION_WIN_BACK = ['Отыграемся?', 'Сыграем ещё?', 'Попробуем ещё раз?']

# список ответов, которые распознает игра
TRUE_ANSWERS = ['✊', '✌', '✋', 'ножницы', 'камень', 'бумага']

# Эмотиконы для добавления в сообщение
SAD_EMOTICONS = ['😔', '😢', '😩', '😿', '😕']
HAPPY_EMOTICONS = ['😜', '😸', '🙌', '✨', '🎂', '🎉', '🎊', '🏆', '👏', '👍', '🎆']

# Начальная фраза сообщения о результате раунда
HAPPY_PREFIXES = ['Ура! ', 'Да! ', 'Поздравляю! ']
SAD_PREFIXES = ['Жаль. ', 'Ну вот. ', 'Грустно. ']

# Основное сообщение
HAPPY_MAIN_PHRASES = ['Вы выиграли! ', 'Победа! ', 'Чистая победа! ', 'Этот раунд наш!']
SAD_MAIN_PHRASES = ['Вы проиграли. ', 'На этот раз проигрыш. ', 'Раунд осталься за Алисой. ']

# Звуки в зависимости от результата раунда
HAPPY_SOUNDS = ['<speaker audio="alice-sounds-game-win-1.opus">',
                '<speaker audio="alice-sounds-game-win-2.opus">',
                '<speaker audio="alice-sounds-game-win-3.opus">']
SAD_SOUNDS = ['<speaker audio="alice-sounds-game-loss-1.opus">',
              '<speaker audio="alice-sounds-game-loss-2.opus">']
NEUTRAL_SOUNDS = ['<speaker audio="alice-sounds-game-ping-1.opus">',
                  '<speaker audio="alice-sounds-game-boot-1.opus">']
