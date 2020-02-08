import telebot
import markups
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '.....................................................'

bot = telebot.TeleBot(API_TOKEN)

#dict: { person_id: { type, current_menu, avapic, resume, bio, age, wanna_match = [] } }
#current_menu: start_up, change_information,
db = dict()

#dict { work_id: { avapic, description, type } }
db_works = {
    'andersen': {
        'avapic': 'AgACAgIAAxkBAAOiXj6gcAvlGqzoiDqa6T3AzLK2obIAAuCtMRv69_hJqqhScq8V4qyzB8EOAAQBAAMCAANtAAMroQIAARgE',
        'description':
"""
ANDERSEN – международная аутсорсинговая компания, ориентированная на разработку программного обеспечения.\n
За последний год количество сотрудников нашей компании увеличилось на 40%;\n
За последние два года более 20% наших сотрудников были в командировках в США, Европе и Израиле;\n
        """,
        'wanna_match': [],
        'contact_info': "+375336526926"
    },

    'imaguru': {
        'avapic': 'AgACAgIAAxkBAAOjXj6ghoTKvTEqdnnXcRzm5kh71xcAAhqsMRv6P_FJDvkWC7Z7n19EIcEOAAQBAAMCAANtAAPvoAIAARgE',
        'description':
"""
Imaguru - первый и самый крупный и влиятельный Startup HUB Беларуси. Это частный бизнес, который имеет 6+ лет опыта в создании и развитии стартапов в Беларуси, работает с инвесторами, инноваторами и предпринимателями.\n
Это пространство для развития инновационных, технологических стартап компаний и предпринимателей, направленных на глобальный рынок.
""",
        'wanna_match': [],
        'contact_info': "+375336526926"
    }
}

@bot.message_handler(commands=['start'])
def startup_handler(message):

    cid = message.chat.id
    if cid in db:
        bot.send_message(cid, 'Ещё раз здравствуйте!')
        bot.send_message(cid, 'Хотите продолжить поиск?', reply_markup=markups.markup_newstart)

    else:

        bot.send_message(cid, 'Здравствуйте. ')
        bot.send_message(cid, 'Что вы ищете?', reply_markup=markups.markup_firststart)

# @bot.message_handler(content_types=['photo'])
# def kek(message):
#     print(message.photo[0].file_id)

print(db)
print(db_works)

#Работник или работодатель
@bot.message_handler(func=lambda message: (message.chat.id not in db) and (message.chat.id not in db_works))
def handler(message):
    print("No 1")
    cid = message.chat.id
    text = message.text.lower()

    print(cid, text)

    if text == 'ищу работу':

        print('Here1')
        db[cid] = dict()
        db[cid]['wanna_match'] = []
        db[cid]['current_menu'] = 'age'
        bot.send_message(cid, 'Хорошо, скажите свой возраст')

    elif text == 'ищу работников':

        print('Here2')
        db_works[cid] = dict()
        db_works[cid]['wanna_match'] = []
        db_works[cid]['current_menu'] = 'description'
        bot.send_message(cid, 'Хорошо, расскажите о своей компании')

#Работодатель
@bot.message_handler(func=lambda message: message.chat.id in db_works, content_types=['text', 'photo'])
def hadler(message):
    try:
        cid = message.chat.id
        try: text = message.text.lower()
        except Exception: text = ''
        menu = db_works[cid]['current_menu']

        if menu == 'description':

            db_works[cid]['description'] = text
            bot.send_message(cid, 'Напишите ваши контактные данные', reply_markup=markups.markup_avapic)

            db_works[cid]['current_menu'] = 'contact_info'

        elif menu == 'contact_info':

            db_works[cid]['contact_info'] = text
            bot.send_message(cid, 'Загрузите фотографию', reply_markup=markups.markup_avapic)

            db_works[cid]['current_menu'] = 'avapic'


        elif menu == 'avapic':

            print('Youre here')
            print(text)
            if text != 'не хочу загружать фотографию.':
                if len(message.photo) != 0:
                    if 'avapic' not in db_works[cid]:
                        db_works[cid]['avapic'] = ''
                    db_works[cid]['avapic'] = message.photo[0].file_id
                    print(db_works[cid]['avapic'])

            bot.send_message(cid, 'Спасибо!')

            import random

            db_works[cid]['current_menu'] = 'matching'
            workerid = random.choice(list(db.keys()))
            db_works[cid]['last_worker'] = workerid

            if 'avapic' in db[workerid]:
                bot.send_photo(cid, db[workerid]['avapic'])
            bio = 'Мы нашли кое-кого для вас!\n\n{}, {}\n{}'.format(db[workerid]['name'], db[workerid]['age'], db[workerid]['bio'])
            bot.send_message(cid, bio, reply_markup=markups.markup_matching)

        elif menu == 'matching':

            if text == 'да.':

                worker = db_works[cid]['last_worker']
                db[worker]['wanna_match'].append(cid)

            if text == 'нет.':

                pass

            if text == 'изменить вакансию.':

                bot.send_message(cid, 'Напишите о своей компании')
                db[cid]['current_menu'] = 'description'
                return

            import random

            workerid = random.choice(list(db.keys()))
            db_works[cid]['last_worker'] = workerid

            if len(db[workerid]['wanna_match']) != 0:

                if 'avapic' in db[workerid]:
                    bot.send_photo(cid, db[workerid]['avapic'])
                bio = 'Этот человек хочет работать у вас.\n\n{}, {}\n{}'.format(db[workerid]['name'], db[workerid]['age'], db[workerid]['bio'])
                bot.send_message(cid, bio, reply_markup=markups.markup_matching)

            else:

                if 'avapic' in db[workerid]:
                    bot.send_photo(cid, db[workerid]['avapic'])
                bio = 'Мы нашли кое-кого для вас!\n\n{}, {}\n{}'.format(db[workerid]['name'], db[workerid]['age'], db[workerid]['bio'])
                bot.send_message(cid, bio, reply_markup=markups.markup_matching)
    except Exception:
        pass
#Работник
@bot.message_handler(func=lambda message: message.chat.id in db, content_types=['text', 'photo'])
def handler(message):
    try:
        cid = message.chat.id
        try: text = message.text.lower()
        except Exception: text = ""
        menu = db[cid]['current_menu']
        print('#', menu)

        if menu == 'age':

            age_str = text
            try:
                xxx = int(age_str)
            except Exception:
                bot.send_message(cid, 'Введите, пожалуйста, свой возраст числом')
                return

            age = int(age_str)
            if age < 16:
                bot.send_message(cid, 'Извините, вам должно быть хотя бы 16 лет.')
                return

            db[cid]['age'] = age
            db[cid]['current_menu'] = 'name'
            bot.send_message(cid, 'Как вас зовут?')

        elif menu == 'name':

            db[cid]['name'] = text
            bot.send_message(cid, 'Расскажите немного о себе.')
            db[cid]['current_menu'] = 'bio'

        elif menu == 'bio':

            db[cid]['bio'] = text

            print('You did this')
            bot.send_message(cid, 'Загрузите свою фотографию', reply_markup=markups.markup_avapic)
            db[cid]['current_menu'] = 'avapic'

        elif menu == 'avapic':

            print('Youre here')
            print(text)
            if text != 'не хочу загружать фотографию.':
                if len(message.photo) != 0:
                    if 'avapic' not in db[cid]:
                        db[cid]['avapic'] = ''
                    db[cid]['avapic'] = message.photo[0].file_id
                    print(db[cid]['avapic'])

            bot.send_message(cid, 'Спасибо!')

            db[cid]['current_menu'] = 'matching'

            import random

            workid = random.choice(list(db_works.keys()))
            db[cid]['last_work'] = workid
            if 'avapic' in db_works[workid]:
                bot.send_photo(cid, db_works[workid]['avapic'])
            bot.send_message(cid, 'Мы нашли для вас вакансию:\n\n{}'.format(db_works[workid]['description']),
                                 reply_markup=markups.markup_matching)

        elif menu == 'matching':

            if text == 'да.':

                if ('wanted' in db[cid]) and db[cid]['wanted']:
                    bot.send_message(cid, 'Вас заметила компания:')

                    workid = db[cid]['last_work']
                    if 'avapic' in db_works[workid]:
                        bot.send_photo(cid, db_works[workid]['avapic'])
                        bot.send_message(cid, '{}'.format(db_works[workid]['description']))
                        bot.send_message(cid, 'Контактные данные:\n\n{}'.format(db_works[workid]['contact_info']))

                else:
                    work = db[cid]['last_work']
                    if 'wanna_match' not in db_works[work]:
                        db_works[work]['wannd_match'] = list()
                    db_works[work]['wanna_match'].append(cid)

            if text == 'нет.':
                pass

            if text == 'изменить анкету.':

                bot.send_message(cid, 'Хорошо, скажите свой возраст')
                db[cid]['current_menu'] = 'age'
                return

            import random

            if len(db[cid]['wanna_match']) != 0:
                workid = db[cid]['wanna_match'][0]
                db[cid]['wanna_match'] = db[cid]['wanna_match'][1:]
                db[cid]['wanted'] = True

            else:
                workid = random.choice(list(db_works.keys()))
                db[cid]['wanted'] = False

            db[cid]['last_work'] = workid
            if 'avapic' in db_works[workid]:
                bot.send_photo(cid, db_works[workid]['avapic'])
            bot.send_message(cid, 'Мы нашли для вас вакансию:\n\n{}'.format(db_works[workid]['description']), reply_markup=markups.markup_matching)
    except Exception:
        pass

bot.polling(none_stop=True)
