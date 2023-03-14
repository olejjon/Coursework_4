import calendar
import datetime
import jwt
from flask_restx import abort
from project.config import BaseConfig
from project.services.users_service import UserService
from project.tools.security import generate_password_hash, compose_passwords


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def create(self, data: dict):
        data['password'] = generate_password_hash(data['password'])
        return self.user_service.create(data)

    def create_token(self, email, password, is_refresh=False):

        user = self.user_service.get_by_email(email)
        if user is None:
            raise abort(404)

        if not is_refresh:
            if not compose_passwords(user.password, password):
                abort(400)

        data = {
            'email': user.email,
            'password': user.password
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=BaseConfig.TOKEN_EXPIRE_MINUTES)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=BaseConfig.ALGO)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=BaseConfig.TOKEN_EXPIRE_DAYS)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=BaseConfig.ALGO)

        return {'access_token': access_token, 'refresh_token': refresh_token}

    def approve_token(self, refresh_token):

        data = jwt.decode(jwt=refresh_token, key=BaseConfig.SECRET_KEY, algorithms=BaseConfig.ALGO )
        email = data.get('email')
        return self.create_token(email, None, is_refresh=True)

