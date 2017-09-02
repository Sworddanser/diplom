import requests
from diplom.data.config_information.information import VERSION, ACCESS_TOKEN,SCREEN_NAME, USER_ID

# APP_ID = 6119344
# AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
# auth_data = {
#     'client_id': APP_ID,
#     'redirect_url': 'https://oauth.vk.com/blank.html',
#     'display': 'mobile',
#     'scope': 'friends, groups',
#     'response_type': 'token',
#     'v': VERSION
# }
#
# print(urlencode(auth_data))
#
# print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))


def get_user_id():
    print('Валидные значения:\nscreen_name:', SCREEN_NAME, '\nuser_id:', USER_ID)
    screen_name_or_id = input('Введите имя или id пользователя:')
    if screen_name_or_id.isdigit() is True and int(screen_name_or_id) > 0:
        data_id = screen_name_or_id
    else:
        screen_name = screen_name_or_id
        print('.')
        params = {
            'access_token': ACCESS_TOKEN,
            'screen_name': screen_name,
            'v': VERSION,
        }
        try:
            response = requests.get('https://api.vk.com/method/utils.resolveScreenName', params)
        except requests.exceptions.ReadTimeout:
            print('Cловили Read timeout occured')
            response = requests.get('https://api.vk.com/method/utils.resolveScreenName', params, timeout=10)
        data_id_user = response.json()
        data_id = data_id_user['response']['object_id']
    return data_id


def get_user_friends(data_id):
    params = {
        'user_id': data_id,
        'v': VERSION,
        'fields': ''
    }
    try:
        response = requests.get('https://api.vk.com/method/friends.get', params)
    except requests.exceptions.ReadTimeout:
        print('Cловили Read timeout occured')
        response = requests.get('https://api.vk.com/method/friends.get', params, timeout=10)
    data_friends = response.json()
    data_friends_id = data_friends['response']['items']
    return data_friends_id


def get_user_group(data_id):
    params = {
        'access_token': ACCESS_TOKEN,
        'user_id': data_id,
        'v': VERSION,
        'extended': 1,
        'fields': 'members_count'
    }
    try:
        response = requests.get('https://api.vk.com/method/groups.get', params)
    except requests.exceptions.ReadTimeout:
        print('Cловили Read timeout occured')
        response = requests.get('https://api.vk.com/method/groups.get', params, timeout=10)
    data_groups = response.json()
    return data_groups


def get_group_members(group_id,user_ids):
    params = {
        'access_token': ACCESS_TOKEN,
        'v': VERSION,
        'group_id': group_id,
        'user_ids': '{user_ids}'.format(user_ids=user_ids),
        'extended': 0,
    }
    try:
        response = requests.get('https://api.vk.com/method/groups.isMember', params)
    except requests.exceptions.ReadTimeout:
        print('Cловили Read timeout occured')
        response = requests.get('https://api.vk.com/method/groups.get', params, timeout=10)
    data_group_members = response.json()
    return data_group_members

