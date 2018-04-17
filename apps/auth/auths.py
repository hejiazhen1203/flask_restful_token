#!/usr/bin/env python
# -*- coding: utf-8
import jwt, datetime
from flask import current_app
class Auth():
    @staticmethod
    def encode_auth_token(user):
        try:

            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=6000),
                'iat': datetime.datetime.utcnow(),
                'aud': 'JWT',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'isAdmin':user.isAdmin,
                    # 'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY', 'aSDDsdasdlmklnkbnbjh'),
                algorithm='HS256'
            )
        except Exception as e:
            print(e)
            return e
    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # 取消过期时间验证
            #payload = jwt.decode(auth_token, config.SECRET_KEY, options={'verify_exp': False})
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY', 'aSDDsdasdlmklnkbnbjh'), audience='JWT', algorithms=['HS256'])
            return {"status": True,
                    "data": payload["data"]
                    }
        except jwt.ExpiredSignatureError:
            return {"status": False,
                    "data": "Token过期"
                    }
        except jwt.InvalidTokenError:
            return {"status": False,
                    "data": "无效Token"
                    }
        except Exception as e:
            return {"status": False,
                    "data": e
                    }
    @staticmethod
    def authenticate(self, user):
        token = self.encode_auth_token(user)
        return token.decode()

    @staticmethod
    def identify(self, request):
        auth_token = request.headers.get('Authorization')
        if auth_token:
            payload = self.decode_auth_token(auth_token)
            result = payload
        else:
            result = {"status": False,
                      "data": "没有提供认证token"
                    }
        return result