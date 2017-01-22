import requests
import time

import settings
import utils


class InstagramAPI:
    def __init__(self):
        # Generated values
        self.device_id = utils.generate_device_id()
        self.uuid = utils.generate_uuid(True)

        # Data for requests
        self.headers = {
            'Connection': 'close',
            'Accept': '*/*',
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie2': '$Version=1',
            'Accept-Language': 'en-US',
            'User-Agent': settings.USER_AGENT,
        }

        self.data = {
            'phone_id': utils.generate_uuid(True),
            'username': settings.username,
            'password': settings.password,
            'guid': self.uuid,
            'device_id': self.device_id,
            'login_attempt_count': '0'
        }
        self.session = requests.Session()
        self.session.headers = self.headers

        # Values from response
        self.response = None
        self.response_decoded = None
        self.token = '9buQEiunf7vdc7ywvnrOMFvn6OAP52ZC'
        self.username_id = None
        self.rank_token = None

    def login(self):
        csrf_response = self.send_request(
            'get',
            'si/fetch_headers/?challenge_type=signup&guid='+utils.generate_uuid(False)
        )

        if csrf_response:
            self.data.update({'_csrftoken': self.response.cookies['csrftoken']})
        else:
            print('Something gone wrong')
            return False

        sig = utils.generate_signature(self.data)
        login_response = self.send_request(request_method='post',
                                           api_method='accounts/login/',
                                           data=sig
       )

        if login_response:
            self.token = self.response.cookies["csrftoken"]
            self.username_id = self.response_decoded["logged_in_user"]["pk"]
            self.rank_token = "%s_%s" % (self.username_id, self.uuid)

            self.sync_features()
            # self.autocomplete_userlist()
            self.timeline_feed()
            self.get_v2_inbox()
            self.get_recent_activity()
            print('Login success!')
            return True
        else:
            print('Something gone wrong 2')
            return False

    def sync_features(self):
        data = {
            '_uuid': self.uuid,
            '_uid': self.username_id,
            'id': self.username_id,
            '_csrftoken': self.token,
            'experiments': settings.EXPERIMENTS
        }
        sig = utils.generate_signature(data)
        return self.send_request(
            request_method='post',
            api_method='qe/sync/',
            data=sig,
        )

    def autocomplete_userlist(self):
        return self.send_request(
            request_method='get',
            api_method='friendships/autocomplete_user_list/',
        )

    def timeline_feed(self):
        return self.send_request(
            request_method='get',
            api_method='feed/timeline/',
        )

    def megaphone_log(self):
        return self.send_request(
            request_method='get',
            api_method='megaphone/log/'
         )

    def get_v2_inbox(self):
        return self.send_request(
            request_method='get',
            api_method='direct_v2/inbox/?'
        )

    def get_recent_activity(self):
        return self.send_request(
            request_method='get',
            api_method='news/inbox/?'
        )

    def get_friends_stories(self):
        return self.send_request(
            request_method='get',
            api_method='feed/reels_tray/',
        )

    def mark_story_as_seen(self, stories):
        data = {
            '_uuid': self.uuid,
            '_uid': self.username_id,
            'id': self.username_id,
            '_csrftoken': self.token,
            'reels': stories,
        }

        return self.send_request(
            request_method='post',
            api_method='media/seen/',
            data=data,
        )

    def send_request(self, request_method, api_method='', data=None):
        if request_method == 'get':
            response = self.session.get(settings.API_URL.format(settings.API_VERSION, api_method))
        elif request_method == 'post':
            response = self.session.post(settings.API_URL.format(settings.API_VERSION, api_method), data=data)
        else:
            print("Wrong method. Try 'get' or 'post'")
            return False

        if response.status_code == 200:
            self.response = response
            self.response_decoded = response.json()
            return True
        else:
            print(response.url)
            print(response.text)
            print(response.status_code)
            return False


def main():
    client = InstagramAPI()
    client.login()
    print(client.token)
    client.get_friends_stories()
    stories_response = client.response_decoded
    if stories_response['status'] == 'ok':
        reels = stories_response['tray']
        for reel in reels:
            if reel['items']:
                for moment in reel['items']:
                    taken_at = str(moment['taken_at'])
                    moment['taken_at'] = taken_at + '_' + "%.0f" % time.time()
                    client.mark_story_as_seen(moment)


if __name__ == '__main__':
    main()




