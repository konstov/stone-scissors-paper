# приглашения сыграть дальше
NEW_ROUND_INVITATION = ['Ещё разок?', 'Давайте ещё?', 'Играем дальше?', 'Ваш ход!', 'Продолжим?', 'Разовьём успех?']
NEW_ROUND_INVITATION_WIN_BACK = ['Отыграемся?', 'Сыграем ещё?', 'Попробуем ещё раз?', 'Возьмём реванш?']

# список ответов, которые распознает игра
VALID_ANSWERS = ['✊', '✌', '✋', 'ножницы', 'камень', 'бумага']

# Эмотиконы для добавления в сообщение
HAPPY_EMOTICONS = ['😜 ', '😸 ', '🙌 ', '✨ ', '🎂 ', '🎉 ', '🎊 ', '🏆 ', '👏 ', '👍 ', '🎆 ']
SAD_EMOTICONS = ['😔 ', '😢 ', '😩 ', '😿 ', '😕 ']
NEUTRAL_EMOTICONS = ['🤝 ']

# Начальная фраза сообщения о результате раунда
HAPPY_PREFIXES = ['Ура! ', 'Да! ', 'Поздравляю! ']
SAD_PREFIXES = ['Жаль. ', 'Ну вот. ', 'Грустно. ', 'Как так? ', 'Мда... ', 'Так себе. ']
NEUTRAL_PREFIXES = ['Неплохо. ', 'Жить можно. ', 'Сойдёт. ']

# Основное сообщение
HAPPY_MAIN_PHRASES = ['Вы выиграли! ', 'Победа! ', 'Чистая победа! ', 'Этот раунд ваш! ', 'Уверенная победа! ']
SAD_MAIN_PHRASES = ['Вы проиграли. ', 'На этот раз проигрыш. ', 'Раунд остался за соперником. ', 'Поражение. ']
NEUTRAL_MAIN_PHRASES = ['Ничья. ', 'Не проиграли. ', 'Ни нашим, ни вашим. ', 'Боевая ничья. ']

# Выбор игры
HAPPY_GAME_SELECT = ['Игра выбрала ', 'Игра выбросила ']
SAD_GAME_SELECT = ['Игра выбрала ', 'Игра выбросила ']
NEUTRAL_GAME_SELECT = ['Игра тоже выбрала ', 'Игра тоже выбросила ', 'Игра также выбрала ', 'Игра также выбросила ']

# Звуки в зависимости от результата раунда
HAPPY_SOUNDS = ['<speaker audio="alice-sounds-game-win-1.opus">',
                '<speaker audio="alice-sounds-game-win-2.opus">',
                '<speaker audio="alice-sounds-game-win-3.opus">'
                ]
SAD_SOUNDS = ['<speaker audio="alice-sounds-game-loss-1.opus">',
              '<speaker audio="alice-sounds-game-loss-2.opus">'
              ]
NEUTRAL_SOUNDS = ['<speaker audio="alice-sounds-game-ping-1.opus">',
                  '<speaker audio="alice-sounds-game-boot-1.opus">'
                  ]

BASE_SUGGESTS = ['камень', 'ножницы', 'бумага']
LIZARD_SPOCK_SUGGESTS = ['камень', 'ножницы', 'бумага', 'ящерица', 'Спок']