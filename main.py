import requests

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

        # Values from response
        self.session = requests.Session()
        self.session.headers = self.headers
        self.response = None
        self.response_decoded = None

    def login(self):
        csrf_response = self.send_request(
            'si/fetch_headers/?challenge_type=signup&guid='+utils.generate_uuid(False), 'get')

        if csrf_response:
            self.data.update({'_csrftoken': self.response.cookies['csrftoken']})
        else:
            print('Something gone wrong')

        login_response = self.send_request('accounts/login/', 'post')

    def send_request(self, request_method, api_method, data=None):
        if request_method == 'get':
            response = self.session.get(settings.API_URL.format(api_method))
        elif request_method == 'post':
            response = self.session.post(settings.API_URL.format(api_method), data=data)
        else:
            print("Wrong method. Try 'get' or 'post'")
            return False

        if response.status_code == 200:
            self.response = response
            self.response_decoded = response.json()
            return True
        else:
            print(response.status_code)
            return False





