import os
import random
from base64 import b64encode
from io import BytesIO
from django.utils.crypto import get_random_string


def img2base64(img):
    with BytesIO() as buf:
        img.save(buf, "gif")
        buf_str = buf.getvalue()
    img_prefix = "data:image/png;base64,"
    b64_str = img_prefix + b64encode(buf_str).decode("utf-8")
    return b64_str


def get_env(name, default=""):
    return os.environ.get(name, default)


def rand_str(length=32, type="lower_hex"):
    """
    Generate random strings or numbers of specified length, which can be used in security scenarios such as keys
    :param length: length of string or number
    :param type: str represents a random string, num represents a random number
    :return: string
    """
    if type == "str":
        return get_random_string(length, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    elif type == "lower_str":
        return get_random_string(length, allowed_chars="abcdefghijklmnopqrstuvwxyz0123456789")
    elif type == "lower_hex":
        return random.choice("123456789abcdef") + get_random_string(length - 1, allowed_chars="0123456789abcdef")
    else:
        return random.choice("123456789") + get_random_string(length - 1, allowed_chars="0123456789")
