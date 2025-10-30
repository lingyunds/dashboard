#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.settings import api_settings
from user.models import User

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 第一步：取出前端传入的token串（从请求头的token中取出）
        token = request.META.get("HTTP_AUTHORIZATION")
        if token:
            # 验证token是否合法
            try:
                # 通过token，得到payload，在得到的过程中会校验，是否过期，是否被穿该
                payload = jwt_decode_handler(token)
                id = payload["user_id"]
            # except jwt.ExpiredSignature:
            #     raise AuthenticationFailed('签名过期')
            # except jwt.DecodeError:

            except Exception:
                raise AuthenticationFailed("签名验证失败")
            # except jwt.InvalidTokenError:
            #     raise AuthenticationFailed('未知错误')
            # 有没有问题？每次都要去数据库查用户，效率低
            # 优先用这种
            # # 本平台账户

            user = User.objects.get(id=id)

            # 不需要查数据库，效率高，存在缺陷，
            # user=User(id=payload['user_id'], username=payload['username'])
            return (user, token)  # 直接返回user,token添加到request中
        else:
            # 没带token串，没登录
            raise AuthenticationFailed("您没有携带token")
