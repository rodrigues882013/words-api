import json
import re
import jwt
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth import authenticate



class WordService(object):
    @staticmethod
    def min(v1, v2, v3):
        return min(min(v1, v2), v3)

    @staticmethod
    def compute_distance(w1, w2):

        def _range(start, end):
            return range(start, end + 1)

        if w1 is None or w2 is None:
            raise ValueError("Word 1  or Word 2 is not a valid value")

        w1, w2 = w1.lower(), w2.lower()
        m, n = len(w1), len(w2)

        if w1 == w2:
            return 0

        if w1 == "" and w2 != "" or w2 == "" and w1 != "":
            return 0

        result = [[0 for _ in _range(0, n)] for _ in _range(0, m)]

        for i in _range(0, m):
            result[i][0] = i

        for j in _range(0, n):
            result[0][j] = j

        for i in _range(1, m):
            for j in _range(1, n):
                cost = 0 if w1[i - 1] == w2[j - 1] else 1
                result[i][j] = WordService.min(result[i - 1][j] + 1,
                                               result[i][j - 1] + 1,
                                               result[i - 1][j - 1] + cost)

        return result[m][n]

    @staticmethod
    def recursive_version(w1, w2):

        if w1 is None or w2 is None:
            raise ValueError("Word 1  or Word 2 is not a valid value")

        if not w1:
            return len(w1)
        if not w2:
            return len(w2)

        w1, w2 = w1.lower(), w2.lower()

        return min(WordService.recursive_version(w1[1:], w2[1:]) + (w1[0] != w2[0]),
                   WordService.recursive_version(w1[1:], w2) + 1,
                   WordService.recursive_version(w1, w2[1:]) + 1)


class AuthServices(object):

    @staticmethod
    def _create_token(user_id):
        return jwt.encode(dict(user=user_id), 'secret', algorithm='HS256')

    @staticmethod
    def decode_token(token):
        user_id = None

        try:
            claims = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = claims.get('user')

        except jwt.DecodeError:
            pass

        return user_id

    @staticmethod
    def auth(user):
        authenticate(username=user.username, password=user.password)

        if user.is_authenticated():
            token = AuthServices._create_token(user.id)
        else:
            token = False

        return token

    @staticmethod
    def verify_user(**kwargs):

        try:
            user = User.objects.get(username=kwargs['username'], email=kwargs['email'])
        except User.DoesNotExist:
            user = None

        if user is not None:
            token = AuthServices.auth(user)

        else:
            user = User.objects.create_user(kwargs['username'], kwargs['email'], kwargs['password'])
            user.save()
            token = AuthServices.auth(user)

        return token


def auth_jwt(function):
    def wrapped(*args, **kwargs):
        request = args[1]

        token = None
        bearer = None
        jwt_token = None

        if request.META.get('HTTP_AUTHORIZATION') is not None:
            token = request.META.get('HTTP_AUTHORIZATION')
        elif request.META.get('AUTHORIZATION') is not None:
            token = request.META.get('AUTHORIZATION')

        if token is not None:
            bearer = re.search(r'Bearer', token)
            jwt_token = re.search(r'(?!Bearer )\w+\d.+', token)

            if bearer is not None:
                bearer = bearer.group()

            if jwt_token is not None:
                jwt_token = jwt_token.group()

        if token is None or bearer != 'Bearer' or AuthServices.decode_token(jwt_token) is None:
                return Response(dict(message="Not Authorized",
                                     status_code=status.HTTP_401_UNAUTHORIZED),
                                status=status.HTTP_401_UNAUTHORIZED)

        return function(*args, **kwargs)

    return wrapped
