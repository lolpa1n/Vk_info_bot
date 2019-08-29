from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api

token = 'Enter token here'  # https://vkhost.github.io/ , выберите Kate Mobile и скопируйте токен из URL

vk_session = vk_api.VkApi(token=token)
vk_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
flag = 0
error_flag = 0
while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                userId = str(event.text)

                if userId == '/help':
                    vk_session.method('messages.send', {'user_id': event.user_id,
                                                        'message': "Для получения информации о пользователе введите ID пользователя с фотографией" +
                                                                   " и с открытым профилем. Для завершения работы с ботом введите /stop",
                                                        'random_id': 0})
                    flag = 2
                    error_flag = 1

                while flag == 0:
                    vk_session.method('messages.send', {'user_id': event.user_id,
                                                        'message': "Пожалуйста, введите команду /help для помощи",
                                                        'random_id': 0})
                    flag = 1
                    error_flag = 1
                if userId.isalpha() and error_flag == 1 and flag == 2:
                    vk_session.method('messages.send', {'user_id': event.user_id,
                                                        'message': "Пожалуйста, введите корректный ID",
                                                        'random_id': 0})

                if userId == '/stop':
                    vk_session.method('messages.send', {'user_id': event.user_id,
                                                        'message': "Работа бота приостановлена. Для возобновления работы с ботом введите /help",
                                                        'random_id': 0})
                    flag = 3
                if userId.isdigit() and flag == 2:
                    response_photo_id = vk_api.users.get(user_ids=userId, fields='photo_id')
                    global bot_answer
                    id = str(response_photo_id[0]['id'])
                    photo_id = response_photo_id[0]['photo_id']
                    clear_id = photo_id.replace(id + '_', '')
                    response_likes = vk_api.likes.getList(type='photo', owner_id=id, item_id=clear_id)
                    likes_counter = response_likes['count']
                    response_photo = vk_api.users.get(user_ids=userId, fields='photo_max_orig')
                    photo_URL = response_photo[0]['photo_max_orig']
                    response_friends = vk_api.friends.get(user_id=userId)
                    friends_counter = response_friends['count']
                    response_wall = vk_api.wall.get(owner_id=userId, filter='owner')
                    views_counter = None

                    if friends_counter != 0:
                        percent_of_likes = str(round((likes_counter / friends_counter) * 100, 2)) + '%'
                    else:
                        percent_of_likes = 'невозможно посчитать, друзей не обнаружено.'

                    for i in range((len(response_wall['items']))):
                        if 'attachments' in response_wall['items'][i].keys():
                            for item in response_wall['items'][i]['attachments']:
                                if 'photo' in item.values():
                                    if str(item['photo']['id']) == clear_id and 'views' in response_wall['items'][
                                        i].keys():
                                        views_counter = response_wall['items'][i]['views']['count']
                    if views_counter == None:
                        views_counter = 'невозможно посчитать просмотры, т.к. пост отсутствует.'
                    bot_answer = 'ID пользователя - ' + id + '\n' + 'ID аватара пользователя - ' + clear_id + '\n' + \
                                 'URL аватара - ' + photo_URL + '\n' + \
                                 "Лайки на аватаре - " + str(likes_counter) + '\n' + \
                                 "Количество просмотров на аватаре - " + str(views_counter) + '\n' + \
                                 "Количество друзей пользователя - " + str(friends_counter) + '\n' + \
                                 'Процент лайков - ' + percent_of_likes
 
                if event.from_user and not (event.from_me) and flag == 2:
                    if userId.isdigit():
                        vk_session.method('messages.send', {'user_id': event.user_id,
                                                            'message': bot_answer,
                                                            'random_id': 0})
            except:
                if error_flag == 1 and flag == 2:
                    vk_session.method('messages.send', {'user_id': event.user_id,
                                                        'message': "Пожалуйста, введите ID пользователя с фотографией и с открытым профилем.",
                                                        'random_id': 0})

