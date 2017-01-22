import hashlib
import hmac
import json
from urllib import parse
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
    seed = seed.hexdigest()
    volatile_seed = "12345"
    final_seed = hashlib.md5()
    final_seed.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
    return 'android-' + final_seed.hexdigest()[:16]


def generate_signature(data):
    data = json.dumps(data)
    parsed_data = parse.quote(data)
    return 'ig_sig_key_version=' + settings.SIG_KEY_VERSION + \
           '&signed_body=' + hmac.new(settings.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() +\
           '.' + parsed_data