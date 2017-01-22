import hashlib
import hmac
import urllib
import uuid

import settings


def generate_uuid(type):
        generated_uuid = str(uuid.uuid4())
        if type:
            return generated_uuid
        else:
            return generated_uuid.replace('-', '')


def generate_device_id():
    seed = hashlib.md5()
    seed.update(settings.username.encode('utf-8') + settings.password.encode('utf-8'))
    volatile_seed = "12345"
    seed.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
    return 'android-' + seed.hexdigest()[:16]


def generate_signature(self, data):
    try:
        parsed_data = urllib.parse.quote(data)
    except AttributeError:
        parsed_data = urllib.quote(data)

    return 'ig_sig_key_version=' + settings.SIG_KEY_VERSION + '&signed_body=' + hmac.new(self.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + parsed_data