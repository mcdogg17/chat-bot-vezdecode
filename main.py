import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import json


def top_9_memes(user_id):
    top_list = sorted(JSON_PHOTO, key=lambda x: JSON_PHOTO[x][0][0], reverse=True)
    for col in range(9):
        write_message(user_id, f'Топ {col + 1}')
        send_statics(user_id, top_list[col])


def create_keyboard(*req):
    keyboard = VkKeyboard(one_time=not req[2], inline=req[2])
    line = 0
    for r in req[0]:
        keyboard.add_button(str(r), color=req[0][r][0])
        if req[1] and line == 0:
            keyboard.add_line()
            line += 1
    return keyboard.get_keyboard()


def send_statics(user_id, photo):
    random_id = round(random.random() * 10 ** 9)
    post = {
        'user_id': user_id,
        'random_id': random_id,
        'attachment': photo,
        'owner_id': -212549250
    }
    vk_group.method('messages.send', post)


def send_memes(user_id, photo):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Лайк', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Дизлайк', color=VkKeyboardColor.NEGATIVE)
    random_id = round(random.random() * 10 ** 9)
    post = {
        'user_id': user_id,
        'random_id': random_id,
        'attachment': photo,
        'owner_id': -212549250,
        'keyboard': keyboard.get_keyboard()
    }
    vk_group.method('messages.send', post)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            response = event.text
            response = response.lower()
            if response == 'лайк':
                JSON_PHOTO[photo][0][0] += 1
                JSON_PHOTO[photo][1].append(user_id)
                break
            elif response == 'дизлайк':
                JSON_PHOTO[photo][0][1] += 1
                JSON_PHOTO[photo][1].append(user_id)
                break
    with open('photo_data.json', 'w') as file:
        json.dump(JSON_PHOTO, file)


def write_message(user_id, message, keyboard=None):
    random_id = round(random.random() * 10 ** 9)
    post = {
        'user_id': user_id,
        'random_id': random_id,
        'message': message,
        'keyboard': keyboard
    }
    vk_group.method('messages.send', post)
    if keyboard:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.text == 'Показать ТОП-9':
                    top_9_memes(user_id)
                    break
                else:
                    break


token = "01dec4449afed1f0a14aa494c931e53e3e5dfefd8c64de3aa003e4d7318026ab23ef8a530b91db8d0b7cf"
app_id = '8131939'
access_token = "ded4b44a6860c8fde80c9e287e3477b1e901ad27765117d08403c0f044a8b34b6d4207329aaf7bcfc65c8"
vk = vk_api.VkApi(token=access_token)

obj_photo = vk.method("photos.get",
                      {"app_id": 8131939, "access_token": access_token, "owner_id": -212549250, "album_id": 283703938,
                       "from_group": 1})
lst_photo = []

for photo in obj_photo["items"]:
    att = f"photo{photo['owner_id']}_{photo['id']}"
    lst_photo.append(att)

with open('photo_data.json', 'r') as read_file:
    JSON_PHOTO = json.load(read_file)

vk_group = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_group)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        response = event.text
        print(event.attachments)
        response = response.lower()
        if response == 'привет':
            write_message(event.user_id, 'Привет вездекодерам!')
        elif response == 'начать':
            state = 1
            write_message(event.user_id, 'Ты программист?', create_keyboard({'Да': [VkKeyboardColor.POSITIVE],
                                                                             'Нет': [VkKeyboardColor.NEGATIVE]}, False,
                                                                            False))
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if state == 1 and (event.text == 'Да' or event.text == 'Нет'):
                        state += 1
                        write_message(event.user_id, 'вопрос 2?', create_keyboard({'Ответ 1': [VkKeyboardColor.PRIMARY],
                                                                                   'Ответ 2': [
                                                                                       VkKeyboardColor.PRIMARY]},
                                                                                  False, True))
                    elif state == 2 and (event.text == 'Ответ 1' or event.text == 'Ответ 2'):
                        state += 1
                        write_message(event.user_id, 'вопрос 3?',
                                      create_keyboard({'Ответ 3': [VkKeyboardColor.POSITIVE],
                                                       'Ответ 4': [VkKeyboardColor.PRIMARY]},
                                                      True, False))
                    elif state == 3 and (event.text == 'Ответ 3' or event.text == 'Ответ 4'):
                        state += 1
                        write_message(event.user_id, 'вопрос 4?',
                                      create_keyboard({'Ответ 5': [VkKeyboardColor.SECONDARY],
                                                       'Ответ 6': [VkKeyboardColor.SECONDARY]},
                                                      True, True))
                    elif state == 4 and (event.text == 'Ответ 5' or event.text == 'Ответ 6'):
                        state += 1
                        write_message(event.user_id, 'вопрос 5?',
                                      create_keyboard({'Ответ 7': [VkKeyboardColor.NEGATIVE],
                                                       'Ответ 8': [VkKeyboardColor.SECONDARY]},
                                                      False, False))
                    elif state == 5 and (event.text == 'Ответ 7' or event.text == 'Ответ 8'):
                        state += 1
                        write_message(event.user_id, 'вопрос 6?', create_keyboard({'Ответ 9': [VkKeyboardColor.PRIMARY],
                                                                                   'Ответ 10': [
                                                                                       VkKeyboardColor.NEGATIVE]},
                                                                                  False, False))
                    elif state == 6 and (event.text == 'Ответ 9' or event.text == 'Ответ 10'):
                        state += 1
                        write_message(event.user_id, 'вопрос 7?',
                                      create_keyboard({'Ответ 11': [VkKeyboardColor.PRIMARY],
                                                       'Ответ 12': [VkKeyboardColor.PRIMARY]},
                                                      False, False))
                    elif state == 7 and (event.text == 'Ответ 11' or event.text == 'Ответ 12'):
                        state += 1
                        write_message(event.user_id, 'вопрос 8?',
                                      create_keyboard({'Ответ 13': [VkKeyboardColor.NEGATIVE],
                                                       'Ответ 14': [VkKeyboardColor.SECONDARY]},
                                                      False, False))
                        break
        elif response.lower() == 'мем':
            while True:
                photo = random.choice(lst_photo)
                if event.user_id in JSON_PHOTO[photo][1]:
                    photo = random.choice(lst_photo)
                else:
                    break
            send_memes(event.user_id, photo)
        elif response.lower() == 'статистика':
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('Показать ТОП-9', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('Закрыть', color=VkKeyboardColor.NEGATIVE)
            count = 0
            for elem in JSON_PHOTO:
                if event.user_id in JSON_PHOTO[elem][1]:
                    count += 1
            write_message(event.user_id, f'Вы оценили {count} мемов', keyboard.get_keyboard())
