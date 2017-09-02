from pprint import pprint
import json
import time
import sys
import os.path

from diplom.data.requests_data import get_user_id, get_group_members, get_user_friends, get_user_group


DIR_PATH = os.path.abspath(os.path.dirname(__file__))


def sleep_inform(inform):
    print(inform, end='')
    for req_time in range(3):
        time.sleep(1)
        sys.stdout.write('.')
        sys.stdout.flush()
    print('\n')


def connect_group_inf(gpoups_extend_data,group_w_fr):
    groups = []
    for group in gpoups_extend_data:
        if group['id'] in group_w_fr:
            group_inform = {
                'name': group['name'],
                'gid': group['id'],
                'members_count': group['members_count']
            }
            groups.append(group_inform)
    return groups


def create_file(name, dict):
    with open(os.path.join(DIR_PATH, name), 'w', encoding='utf-8') as f:
        json.dump(dict, f, indent=2, ensure_ascii=False)


def load_file(name):
    with open(os.path.join(DIR_PATH, name), encoding='utf-8') as f:
        data_file = f.read()
    return data_file


def main():

    data_id = get_user_id()
    sleep_inform('запрос, ищу пользователя')

    data_friends_id = get_user_friends(data_id)
    sleep_inform('запрос, ищу друзей пользователя')

    data_groups = get_user_group(data_id)
    data_groups_id = [id['id'] for id in data_groups['response']['items']]
    sleep_inform('запрос, ищу группы пользователя')

    group_wout_fr = []
    n = 5 # количество пользователей для поиска групп, в которых есть общие друзья, но не более чем n
    group_with_nfr = []
    for iterations, group_id in enumerate(data_groups_id):
        ##############################################################################
        #  в контакте есть ограничение на количество пользователей , которых можно проверять на принадлежность группе
        max_check_ids = 300
        cout_of_iterations = 1 + len(data_friends_id) // max_check_ids
        summ = 0
        sleep_inform('{} {} {}'.format('Ищу друзей пользователя в группе , осталось',len(data_groups_id)-(iterations),'гр.'))
        for i in range(cout_of_iterations):
            i += 1
            user_ids = data_friends_id[max_check_ids * (i - 1):max_check_ids * i]
        ##############################################################################
            data_group_members = get_group_members(group_id,user_ids)
            for user_check in data_group_members['response']:
                summ = summ + user_check['member']
        if summ == 0:
            group_wout_fr.append(group_id)
        if summ != 0 and summ <= n:
            group_with_nfr.append(group_id)

    data_groups_inf = get_user_group(data_id)
    gpoups_extend_data = data_groups_inf['response']['items']

    groups = connect_group_inf(gpoups_extend_data,group_wout_fr)
    groups_n = connect_group_inf(gpoups_extend_data,group_with_nfr)

    sleep_inform('Записываю фаил №1')
    create_file('groups.json', groups)
    print('Посмотрим что получилось:')
    data_file = load_file('groups.json')
    pprint(data_file)

    sleep_inform('Записываю фаил№2')
    create_file('groups_n.json', groups_n)
    print('Посмотрим что получилось:')
    data_file_n = load_file('groups_n.json')
    pprint(data_file_n)


main()
