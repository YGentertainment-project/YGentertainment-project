import os
from base64 import b64encode
from io import BytesIO


def img2base64(img):
    with BytesIO() as buf:
        img.save(buf, "gif")
        buf_str = buf.getvalue()
    img_prefix = "data:image/png;base64,"
    b64_str = img_prefix + b64encode(buf_str).decode("utf-8")
    return b64_str


def get_env(name, default=""):
    return os.environ.get(name, default)