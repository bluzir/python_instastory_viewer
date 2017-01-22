import requests

import utils


class InstagramAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.device_id = utils.generate_device_id()
        self.uuid = utils.generate_uuid(True)
        self.session = None
        self.response = None
        self.response_decoded = None

    def login(self):
        self.session = requests.Session()
        csrf_response = self.send_request(
            'si/fetch_headers/?challenge_type=signup&guid='+utils.generate_uuid(False), 'get')

        if csrf_response:
            data = {
                'phone_id': utils.generate_uuid(True),
                '_csrftoken': self.response.cookies['csrftoken'],
                'username': self.username,
                'guid': self.uuid,
                'device_id': self.device_id,
                'password': self.password,
                'login_attempt_count': '0'
            }

        login_response = self.send_request('accounts/login/', 'post')



    def send_request(self, request_method, api_method, data=None):
        self.session.headers.update({
            'Connection': 'close',
            'Accept': '*/*',
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie2': '$Version=1',
            'Accept-Language': 'en-US',
            'User-Agent': self.USER_AGENT}
        )
        if request_method == 'get':
            response = requests.get(self.API_URL.format(api_method))
        elif request_method == 'post':
            response = requests.post(self.API_URL.format(api_method), data=data)
        else:
            print("Wrong method. Try 'get' or 'false'")
            return False

        if response.status_code == 200:
            self.response = response
            self.response_decoded = response.json()
            return True
        else:
            print(response.status_code)
            return False





