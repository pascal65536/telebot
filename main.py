from datetime import datetime
import telebot
import os
import subprocess
import random

from settings_local import bot_api


bot = telebot.TeleBot(bot_api)


def init_user(name):
    folder = str(name)
    try:
        os.mkdir(folder)
    except OSError:
        pass


@bot.message_handler(commands=['start'])
def send_start(message):
    user_id = message.chat.id
    init_user(user_id)
    msg = 'Привет, я просто телеграм-бот!\nСвязь с автором: https://telegram.me/pascal65536'
    bot.send_message(user_id, msg)


@bot.message_handler(commands=['time'])
def send_time(message):
    user_id = message.chat.id
    init_user(user_id)
    msg = 'Время на сервере: {}'.format(datetime.now().isoformat())
    bot.send_message(user_id, msg)


@bot.message_handler(commands=['screenshot'])
def send_screenshot(message):
    user_id = message.chat.id
    init_user(user_id)
    name = 'screenshot.jpg'
    # Запустить команду в терминале
    proc = subprocess.Popen('DISPLAY=":0.0" import -window root ' + str(user_id) + '/' + name, shell=True, stdout=subprocess.PIPE)
    out = proc.communicate()
    # msg = bot.send_message(message.chat.id, 'Скриншот в папке юзера.')
    if os.path.exists(str(user_id) + '/' + name):
        bot.send_chat_action(user_id, 'upload_photo')
        img = open(str(user_id) + '/' + name, 'rb')
        bot.send_photo(user_id, img, reply_to_message_id=message.message_id)
        img.close()
    else:
        bot.send_message(user_id, 'Фотографии нет, надо создать её')


@bot.message_handler(commands=['camera'])
def send_camera(message):
    user_id = message.chat.id
    init_user(user_id)
    name = 'out.jpg'
    # Запустить команду в терминале
    proc = subprocess.Popen("fswebcam " + str(user_id) + "/" + name + " --jpeg 99 --resolution 640x480", shell=True, stdout=subprocess.PIPE)
    out = proc.communicate()
    # msg = bot.send_message(message.chat.id, 'То, что увидела камера сохранилось в файл out.jpg в папке юзера.')
    if os.path.exists(str(user_id) + '/' + name):
        bot.send_chat_action(message.chat.id, 'upload_photo')
        img = open(str(user_id) + '/' + name, 'rb')
        bot.send_photo(user_id, img, reply_to_message_id=message.message_id)
        img.close()
    else:
        bot.send_message(user_id, 'Фотографии нет, надо создать её')


@bot.message_handler(commands=['list'])
def send_setting(message):
    user_id = message.chat.id
    init_user(user_id)
    msg = 'Файлы в папке пользователя:\n'
    msg += '\n'.join(os.listdir(str(user_id)))
    msg +=  '...'
    bot.send_message(user_id, msg)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_msg(message):
    user_id = message.chat.id
    init_user(user_id)

    message_lst = list(message.text)
    random.shuffle(message_lst)
    message_send = ''.join(message_lst)
    bot.send_message(user_id, message_send)


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    user_id = message.chat.id
    init_user(user_id)

    try:
        file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = str(user_id) + '/' + file_info.file_path
        with open(src, 'wb') as new_file:
           new_file.write(downloaded_file)
        bot.reply_to(message, 'Фото добавлено')
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    user_id = message.chat.id
    init_user(user_id)

    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = str(user_id) + '/' + file_info.file_path
        with open(src, 'wb') as new_file:
           new_file.write(downloaded_file)
        bot.reply_to(user_id, 'Файл добавлен')
    except Exception as e:
        bot.reply_to(user_id, e)


bot.polling()


'''
@bot.message_handler(commands=['setting, help'])
def send_setting(message):
    path = str(message.chat.id)
    # На всякий случай, если юзер не сделал start
    CreateDir(str(message.chat.id))
    msg = bot.send_message(message.chat.id, 'Файлы в папке пользователя:')
    files = os.listdir(path)
    i = 0
    while i < len(files):
        msg = bot.send_message(message.chat.id, files[i])
        i = i + 1
    msg = bot.send_message(message.chat.id, '...')

# Обработчик для документов и аудиофайлов
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass

#Обработчик сообщений, подходящих под указанное регулярное выражение
@bot.message_handler(regexp="SOME_REGEXP")
def handle_message(message):
    pass

# Обработчик сообщений, содержащих документ с mime_type 'text/plain' (обычный текст)
@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
def handle_text_doc(message):
    pass

@bot.message_handler(commands=['auth'])
def send_auth(message):
    pass
'''
