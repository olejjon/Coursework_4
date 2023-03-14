import base64
import hashlib
import hmac
from typing import Union

import jwt
from flask import current_app, request, abort

from project.config import BaseConfig


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compose_passwords(password_hash: Union[str, bytes], password: str):
    decode_password = base64.b64decode(password_hash)

    hash_password = __generate_password_digest(password)
    return hmac.compare_digest(decode_password, hash_password)


def auth_required(func):
    def wrapper(*args, **kwargs):

        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer ')[:-1]

        try:
            jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGO])
        except Exception as e:
            print('JWT Decode Exception', e)
            abort(401)
        return func(*args, **kwargs)
    return wrapper

