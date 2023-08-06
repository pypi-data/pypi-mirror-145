import time
import json
from urllib.parse import urlencode

from src.InstagramFakeAPI.v159.mixin import LoginAction


class InstagramCustom(LoginAction):

    def __init__(self):
        LoginAction.__init__(self)
        self.__log.debug('Start Instagram')

        self.__follow_rank_token = {}
        self.__follow_user_id = {}

    def timeline(self):
        self.proxy_str = self.account.get('proxy', None)
        self.post('/feed/timeline/', self.authorized(), json.dumps({'test': '1'}))

    def info(self, user_id):
        self.proxy_str = self.account.get('proxy', None)
        self.get('/users/{}/info/'.format(user_id), self.authorized(), None)

    def info_by_username(self, username: str):
        self.proxy_str = self.account.get('proxy', None)
        self.get('/users/{}/usernameinfo/'.format(username), self.authorized(), None)

    def followers(self, user_id, max_id):
        self.__follow(user_id, 'followers', max_id)

    def following(self, user_id, max_id):
        self.__follow(user_id, 'following', max_id)

    def related(self, user_id):
        self.get('/discover/chaining/?target_id={}'.format(user_id), self.authorized())

    def related_by_username(self, username):
        self.info_by_username(username)
        account = self.last_json
        self.related(account['user']['pk'])

    def story_by_username(self, username):
        self.info_by_username(username)
        account = self.last_json
        self.stories(account['user']['pk'])

    def stories(self, user_id: int):
        self.get('/feed/user/{}/story/'.format(user_id), self.authorized(), None, False,
                 {'supported_capabilities_new': json.dumps(self.SUPPORTED_CAPABILITIES_NEW)})

    def story_by_id(self, story_id: int):
        self.__log.debug('!!!!! Story info')
        self.get('/media/{}/info/'.format(story_id), self.authorized())

    def __follow(self, user_id, search_type: str, max_id: int):

        if self.__follow_user_id.get(search_type) != user_id:
            self.__follow_rank_token[search_type] = self.uuid('{}-{}-{}'.format('following', user_id, time.time()))
            self.__follow_user_id[search_type] = user_id

        query = {
            'search_surface': 'follow_list_page',
            'order': 'default',
            'query': '',
            'max_id': max_id,
            'enable_groups': 'true',
            'rank_token': self.__follow_user_id[search_type]
        }

        if not query['max_id']:
            del query['max_id']

        url = '/friendships/{}/{}/?{}'.format(user_id, search_type, urlencode(query))
        self.get(url, self.authorized(), None)
