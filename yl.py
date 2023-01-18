# -*- coding: utf-8 -*-
import telebot
from telebot import types
import pickle

bot = telebot.TeleBot('5589637928:AAG4Ell_L2GAFR7hHg6VQGrcoT6uV_q3BGk')

admins = 1138500722


@bot.message_handler(commands=['start'])
def start(message):
    sticker_hello = open('Photo and audio/yl_hello.webp', "rb")
    bot.send_sticker(message.chat.id, sticker_hello)

    print(message.from_user.first_name + '(' + str(message.from_user.id) + ") : " + message.text)
    with open('yl.txt', 'a+') as ch:
        print(message.chat.id, file=ch)
    mess = f'Привет, <b><u>{message.from_user.first_name}</u> Чтобы узнать о людях в Young Life /yl</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['help'])
def comands(message):
    sticker_help = open('Photo and audio/yl_help.webp', "rb")
    bot.send_sticker(message.chat.id, sticker_help)
    bot.send_message(message.chat.id, '''Все возможные команды:
/yl
/info
/insta
Спасибо за понимание!''')


@bot.message_handler(commands=['ras'])
def notify(message):
    command_sender = message.from_user.id
    if command_sender in admins:
        with open(r'yl.txt') as ids:
            for line in ids:
                user_id = int(line.strip("\n"))
                try:
                    bot.send_message(user_id, message.text[message.text.find(' '):])
                except Exception as e:
                    bot.send_message(command_sender, f'ошибка отправки сообщения юзеру - {user_id}')
    else:
        bot.send_message(command_sender, f'у вас нет прав для запуска команды')


@bot.message_handler(commands=['info'])
def info(message):
    sticker_info = open('Photo and audio/yl_info.webp', "rb")
    bot.send_sticker(message.chat.id, sticker_info)
    print(message.from_user.first_name + '(' + str(message.from_user.id) + ") : " + message.text)
    mess = f'<i><span class="tg-spoiler">Young Life - это место, где тебя ждут, место где тебя ценят и место где тебе не будет скучно!\n\nМы те, кто организовывает разнообразные увлекательные мероприятия для молодёжи и подростков! Квесты, лагеря, сумашедшие вечера и это ещё не всё!\n\nYoung Life - это там, где тебя поймут и выслушают, место встречи друзей, хорошее общение и просто там, где можно отлично провести время в хорошей компании за чашкой чая или миской поп-корна смотря фильм.\n\nРазные интересные и захватывающие настольные игры и другие разнообразные виды времяпрепровождения не дадут тебе скучать!</span></i>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['insta'])
def webside(message):
    sticker_insta = open('Photo and audio/yl_insta.webp', "rb")
    bot.send_sticker(message.chat.id, sticker_insta)

    print(message.from_user.first_name + '(' + str(message.from_user.id) + ") : " + message.text)
    marrup = types.InlineKeyboardMarkup()
    marrup.add(types.InlineKeyboardButton('Открыть Инсту', url='https://www.instagram.com/yl_karakol/'))
    bot.send_message(message.chat.id, 'Наш Инстаграм!!!', reply_markup=marrup)


try:
    with open("ylbase.pickle", "rb") as handle:
        database = pickle.load(handle)
except:
    database = {}



@bot.message_handler(commands=['yl'])
def button(message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_name = message.from_user.first_name
    add_user_to_database(user_id, username, user_name)
    bot.send_message(message.chat.id, '<u>Сейчас я расскажу о команде Young life Karakol</u>', parse_mode='html')
    sticker_karakol = open('Photo and audio/yl_karakol.webp', "rb")
    bot.send_sticker(message.chat.id, sticker_karakol)

    print(message.from_user.first_name + '(' + str(message.from_user.id) + ") : " + message.text)

    markup = types.InlineKeyboardMarkup()
    leaders_button = types.InlineKeyboardButton("Лидеры", callback_data="Лидеры")
    helpers_button = types.InlineKeyboardButton("Помощники", callback_data="Помощники")
    markup.add(leaders_button, helpers_button)
    bot.send_message(message.chat.id, "О ком хочешь узнать:", reply_markup=markup)

@bot.message_handler(commands=['see'])
def see_user(message):
    print(message.from_user.first_name + '(' + str(message.from_user.id) + ") : " + message.text)
    if message.from_user.id == admins:
        if database:
            text = ""
            for user_id, user_data in database.items():
                text += f"ID: {user_id}\nUsername: {user_data['user']}\nUser name: {user_data['name']}\n\n"
            bot.send_message(chat_id=message.chat.id, text=text)
        else:
            bot.send_message(chat_id=message.chat.id, text="Нечего нет")
    else:
        bot.send_message(chat_id=message.chat.id, text="У вас нет прав на использование этой команды")

def add_user_to_database(user_id, username, user_name=None):
    if user_id not in database:
        database[user_id] = {
            'name': user_name,
            'user': username,
        }
        with open("ylbase.pickle", "wb") as handle:
            pickle.dump(database, handle)

@bot.message_handler(commands=['pip'])
def broadcast(message):
    if message.from_user.id == admins:
        message_text = message.text.replace("/pip ", "")
        for user_id in database:
            try:
                bot.send_message(user_id, message_text)
            except:
                bot.send_message(chat_id=message.chat.id, text=f"Не удалось отправить сообщение пользователю с идентификатором: {user_id}")
    else:
        bot.send_message(chat_id=message.chat.id, text="У вас нет прав на использование этой команды")

@bot.message_handler(commands=['pi'])
def message_user(message):
    if message.from_user.id == admins:
        message_text = message.text.replace("/pi ", "")
        user_id = message_text.split(" ")[0]
        message_text = message_text.replace(user_id + " ", "")
        try:
            bot.send_message(user_id, message_text)
            bot.send_message(chat_id=message.chat.id, text=f"Сообщение отправлено пользователю с id: {user_id}")
        except:
            bot.send_message(chat_id=message.chat.id, text=f"Не удалось отправить сообщение пользователю с идентификатором: {user_id}")
    else:
        bot.send_message(chat_id=message.chat.id, text="У вас нет прав на использование этой команды")

@bot.callback_query_handler(func=lambda call: call.data == "◀Назад")
def handle_back(call):
    markup = types.InlineKeyboardMarkup()
    leaders_button = types.InlineKeyboardButton("Лидеры", callback_data="Лидеры")
    helpers_button = types.InlineKeyboardButton("Помощники", callback_data="Помощники")
    markup.row(leaders_button, helpers_button)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="О ком хочешь узнать:",
                          reply_markup=markup)


sent_messages_ids = []


@bot.callback_query_handler(func=lambda call: call.data == 'back')
def delete_photo(call):
    if sent_messages_ids:
        last_message_id = sent_messages_ids.pop()
        bot.delete_message(chat_id=call.message.chat.id, message_id=last_message_id)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    message = None
    if call.data == "Лидеры":
        leaders = []
        markup = types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton('Дарья', callback_data='Дарья'))
        markup.row(telebot.types.InlineKeyboardButton('Канат', callback_data='Канат'))
        markup.row(telebot.types.InlineKeyboardButton('София', callback_data='София'))
        markup.row(telebot.types.InlineKeyboardButton('Саида', callback_data='Саида'))
        markup.row(telebot.types.InlineKeyboardButton('Луиза', callback_data='Луиза'))
        for leader in leaders:
            button = types.InlineKeyboardButton(leader, callback_data="Лидеры")
            markup.add(button)
        back_button = types.InlineKeyboardButton("◀Назад", callback_data="◀Назад")
        markup.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Лидеры:",
                              reply_markup=markup)
    elif call.data == "Помощники":
        helpers = []
        markup = types.InlineKeyboardMarkup()

        markup.row(telebot.types.InlineKeyboardButton('Элиза', callback_data='Элиза'))
        markup.row(telebot.types.InlineKeyboardButton('Макс', callback_data='Макс'))

        for helper in helpers:
            button = types.InlineKeyboardButton(helper, callback_data="Помощник")
            markup.add(button)
        back_button = types.InlineKeyboardButton("◀Назад", callback_data="◀Назад")
        markup.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Помощники:",
                              reply_markup=markup)
    elif call.data == "◀Назад":
        markup = types.InlineKeyboardMarkup()
        leaders_button = types.InlineKeyboardButton("Лидеры", callback_data="Лидеры")
        helpers_button = types.InlineKeyboardButton("Помощники", callback_data="Помощники")
        markup.add(leaders_button, helpers_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="О ком хочешь узнать:",
                              reply_markup=markup)

    if call.data == "Дарья":
        photo1 = open("Photo and audio/dasha4.jpg", "rb")
        sent_photo = bot.send_photo(call.from_user.id, photo1, caption='''Привет!
Моё имя Дарья, в основном меня зовут Даша, но те, кто давно в Young Life знают меня как Тут-турут 💁🏻‍♀(Да это отсылка к Даше путешественнице).
Я из Бишкека, но уже год живу в Караколе 💞, полюбила этот город. 
В Young Life я с 2016г.
Люблю танцевать 💃🏻, думаю у меня хорошо получается (кхе-кхе 7 лет в танцах не прошли даром).Очень люблю петь 🎶 (3 года в музыкалке тоже не хухры-мухры 😌).
🎲 Настольные игры - отдельный вид удовольствия.
Люблю ночные прогулки по городу 🌃,а еще смотреть фильмы и сериалы🍿.
Мечтаю стать фитнес-тренером 💪🏻.
У меня нет самой любимой песни 🤷🏻‍♀. Думаю могу рассказать ещё много всего, но уже при встрече 😉
Приходи к нам на клуб💫''', reply_markup=types.InlineKeyboardMarkup().add(
            telebot.types.InlineKeyboardButton('◀Назад', callback_data='back')))
        sent_messages_ids.append(sent_photo.message_id)


    elif call.data == "Канат":
        photo = open("Photo and audio/pupkin.webp", "rb")
        sent_photo = \
            bot.send_photo(call.from_user.id, photo,
                           caption='<b>Привет, меня зовут Канат! Я целеустремлённый! Умный! Самый хороший! Прекрасный! Просто красавчик. БОзар нэт мужЫк - в этом убеждена моя мама!!!</b>',
                           parse_mode='html',
                           reply_markup=telebot.types.InlineKeyboardMarkup().add(
                               telebot.types.InlineKeyboardButton('◀Назад', callback_data='back')))
        sent_messages_ids.append(sent_photo.message_id)




    elif call.data == "Макс":
        photo = open("Photo and audio/stirlitz.jpg", "rb")
        audio = open('Photo and audio/qwe.mp3', "rb")
        sent_photo = bot.send_photo(call.from_user.id, photo,
                                    caption=f'<i><span class="tg-spoiler">Это Макс и он создатель этого бота\n@MrStirlitz</span></i>',
                                    parse_mode='html', reply_markup=telebot.types.InlineKeyboardMarkup().add(
                telebot.types.InlineKeyboardButton('◀Назад', callback_data='back')))
        sent_messages_ids.append(sent_photo.message_id)

    elif call.data == "София":
        photo = open("Photo and audio/sonia.jpg", "rb")
        sent_photo = bot.send_photo(call.from_user.id, photo,
                                    caption='''Привет. Меня зовут София,
(да, та что София прекрасная👸🏻😂 ), но все называют меня Соня , я люблю спать 🙃
Мне 16 лет.  Я учусь во 2 школе, работаю в кофейне, а ещё люблю лежать как овощ и ничего не делать🫠
Как то в 2020 году , меня позвала подруга покушать бесплатно пиццу в young life, именно тогда меня и занесло сюда  😁 пицца уж очень вкусная была 
Я люблю:
Поэзию 🤓
Слушать музыку 🎶
Играть в настольные игры🎲
Кататься на скейте , коньках , сноуборде🛹⛸🏂
Гулять 
Ходить в походы 🏕
Лагеря young life 😍
Вкусную еду 😋
И ещё много всякого разного😌 
Приходи к нам на клуб✨(у нас есть вкусняшки😂)''', reply_markup=telebot.types.InlineKeyboardMarkup().add(
                telebot.types.InlineKeyboardButton('◀Назад', callback_data='back')))
        sent_messages_ids.append(sent_photo.message_id)

    elif call.data == "Саида":
        photo = open("Photo and audio/saida.jpg", "rb")
        sent_photo = bot.send_photo(call.from_user.id, photo,
                                    caption='''Привет!
Меня зовут Саида.
Я в young Life не давно, но очень полюбила его. Young Life для меня стал семьёй.
Я с рождения живу в Караколе и очень люблю этот город.
Люблю заниматься спортом, читать и печь вкусную выпечку. Люблю проводить время с друзьями. Люблю гулять ночью, но родители не любят когда я гуляю поздно.
Я очень добрая и люблю людей.
Приходи к нам на клуб и при встрече на клубе лучше познакомимся.''',
                                    reply_markup=telebot.types.InlineKeyboardMarkup().add(
                                        telebot.types.InlineKeyboardButton('◀Назад', callback_data='back')))
        sent_messages_ids.append(sent_photo.message_id)
    elif call.data == "Элиза":
        photo = open("Photo and audio/iliza.jpg", "rb")
        sent_photo = bot.send_photo(call.from_user.id, photo,
                                    caption='''привет.
меня зовут элиза.
и я подросток с Каракола, для которого young life стал очень важной и любимой частичкой души.
так же, я самый младший участник в young life, но не смотря на это я преобладаю достаточно взрослым умом и в целом я очень интересная личность.
я люблю читать книги.умею правильно расставлять приоритеты и размышлять.со мной легко найти общий язык.сама по себе являюсь очень сильной, но одновременно очень ранимой личностью.я очень позитивная, эмоциональная, амбициозная и очень талантливая.я очень боюсь животных, даже кошек (простите).
ENTP - мой тип личности, да я полемист.любимый жанр музыки : фонк и классическая музыка.
 для меня young life - это не место, а люди и неимоверный комфорт. благодоря yl я вышла из зоны комфорта и не боюсь быть собой. уже как год как я частичка yl.для меня это что-то очень важное, и то что я очень люблю и ценю.
 —ƍʎvʞ ɐн wɐн ʞ иɓохиdu.''', reply_markup=types.InlineKeyboardMarkup().add(
                telebot.types.InlineKeyboardButton('◀Назад', callback_data='back')))
        sent_messages_ids.append(sent_photo.message_id)

    elif call.data == "Луиза":
        photo = open("Photo and audio/luiza.jpg", "rb")
        sent_photo = bot.send_photo(call.from_user.id, photo,
                                    caption='''Привет меня зовут Луиза, я лучшая в мире колонка. Я немного прихотлива, люблю работать только у истинных владельцев. А так обычно всегда с командой, я могу в любой момент помочь своим высококлассным звучанием!''',
                                    reply_markup=types.InlineKeyboardMarkup().add(
                                        telebot.types.InlineKeyboardButton('◀Назад', callback_data='back')))
        sent_messages_ids.append(sent_photo.message_id)

    print(call.message.from_user.first_name + '(' + str(call.message.from_user.id) + ") : " + call.message.text)


@bot.message_handler(content_types=['text'])
def jok(message):
    if message.text.lower() == 'кто топ':
        bot.reply_to(message,
                     f'<b><u>{message.from_user.first_name}</u> Самый лучший, самый красивый, самый 😎</b>',
                     parse_mode='html')
    else:
        bot.reply_to(message,
                     'Извените я тебя не понял! \nЧтобы узнать команды: \n/help')
    print(message.from_user.first_name + '(' + str(message.from_user.id) + ") : " + message.text)


bot.message_handler()

bot.polling(none_stop=True, interval=0)