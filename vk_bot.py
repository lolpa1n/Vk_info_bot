from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api

token = 'Enter token here' # https://vkhost.github.io/ , choose Kate Mobile and take token/

vk_session = vk_api.VkApi(token=token)
vk_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                userId = str(event.text)
                if userId.isalpha():
                    vk_session.method('messages.send', {'user_id': event.user_id,
                                                        'message': "Please input ID",
                                                        'random_id': 0})
                if userId.isdigit():
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
                    views_counter = ''

                    if friends_counter != 0:
                        percent_of_likes = str(round((likes_counter / friends_counter) * 100, 2)) + '%'
                    else:
                        percent_of_likes = 'It is impossible to count without having friends'

                    for i in range((len(response_wall['items']))):
                        if 'attachments' in response_wall['items'][i].keys():
                            for item in response_wall['items'][i]['attachments']:
                                if 'photo' in item.values():
                                    if str(item['photo']['id']) == clear_id and 'views' in response_wall['items'][i].keys():
                                        views_counter = response_wall['items'][i]['views']['count']
                    bot_answer = 'User id - ' + id + '\n' + 'User photo id - ' + clear_id + '\n' + \
                                 'Photo URL - ' + photo_URL + '\n' + \
                                 "User's likes - " + str(likes_counter) + '\n' + \
                                 "Avatar views - " + str(views_counter) + '\n' + \
                                 "User's friends - " + str(friends_counter) + '\n' + \
                                 'Likes percentage - ' + percent_of_likes

                if event.from_user and not (event.from_me):
                    if userId.isdigit():
                        vk_session.method('messages.send', {'user_id': event.user_id,
                                                            'message': bot_answer,
                                                            'random_id': 0})
            except:
                vk_session.method('messages.send', {'user_id': event.user_id,
                                                    'message': "Please input user's ID with photo",
                                                    'random_id': 0})



