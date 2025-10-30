#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib

from django.contrib.auth.backends import ModelBackend
from user.models import User


class DjangoAuthenticate(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # django.contrib.auth中调用backends，
        # user = backend.authenticate(request, **credentials)
        # 此时request还为空，**credentials带内容
        password = password.encode("utf-8")
        password = hashlib.sha3_256(password).hexdigest()
        try:
            user = User.objects.get(username=username, password=password)
            return user
        except Exception:
            return None
