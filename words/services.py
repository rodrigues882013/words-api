import datetime
import logging
import re
import jwt

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response

from words.models import Token, Word

# Get an instance of a logger
logger = logging.getLogger(__name__)


class WordService(object):

    @staticmethod
    def is_empty(word):
        return word == "" or word == " " or word is None

    @staticmethod
    def min(v1, v2, v3):
        return min(min(v1, v2), v3)

    @staticmethod
    def compute_distance(w1, w2):

        def _range(start, end):
            return range(start, end + 1)

        if w1 is None or w2 is None:
            logger.error("Word 1  or Word 2 is not a valid value")
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
            logger.error("Word 1  or Word 2 is not a valid value")
            raise ValueError("Word 1  or Word 2 is not a valid value")

        if not w1:
            return len(w1)
        if not w2:
            return len(w2)

        w1, w2 = w1.lower(), w2.lower()

        return min(WordService.recursive_version(w1[1:], w2[1:]) + (w1[0] != w2[0]),
                   WordService.recursive_version(w1[1:], w2) + 1,
                   WordService.recursive_version(w1, w2[1:]) + 1)

    @staticmethod
    def is_similar(w1, w2, threshold=3):
        logger.info("Testing if worlds are similar")
        return WordService.compute_distance(w1, w2) <= threshold

    @staticmethod
    def filter_words(**kwargs):
        logger.info("Filtering the word set")
        keyword = kwargs.get('keyword')
        threshold = kwargs.get('threshold') if kwargs.get('threshold') is not None else 3
        words = list()

        _filter = lambda x: WordService.is_similar(keyword, x, threshold)
        words_set = [w if _filter(w.get_word()) else None for w in Word.objects.all()]
        filter(lambda x: words.append(x) if x is not None else False, words_set)

        return words


class AuthServices(object):

    @staticmethod
    def create_token(user):
        logger.info("Creating access token")
        token = jwt.encode(dict(user_id=user.id,
                                exp=datetime.datetime.utcnow() + datetime.timedelta(minutes=15)),
                           'secret', algorithm='HS256')
        token_obj = Token(token=token, user=user)
        token_obj.save()

        return token_obj.get_token()

    @staticmethod
    def decode_token(token):
        result = None

        try:
            claims = jwt.decode(token, 'secret', algorithms=['HS256'])
            # The result is own user id
            result = claims.get('user_id')

        except jwt.DecodeError:
            pass

        except jwt.ExpiredSignatureError:
            result = False

        return result

    @staticmethod
    def is_valid(token):
        return AuthServices.decode_token(token)

    @staticmethod
    def token_manager(user):
        token = None

        try:
            token = Token.objects.get(user=user.id)
        except Token.DoesNotExist:
            pass

        if token is not None and AuthServices.is_valid(token):
            token = token.get_token()

        else:
            token = AuthServices.create_token(user)

        return token

    @staticmethod
    def verify_user(**kwargs):
        logger.info("Verifying if users and grant access to api")
        try:
            user = User.objects.get(username=kwargs['username'],
                                    email=kwargs['email'])
        except User.DoesNotExist:
            logger.info("User yet haven't access to api, the user will be created")
            user = None

        if user is None:
            logger.info("Creating user")
            user = User.objects.create_user(kwargs['username'],
                                            kwargs['email'],
                                            kwargs['password'])
            user.save()

        token = AuthServices.token_manager(user)

        return token


# Decorators
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

        is_valid = AuthServices.is_valid(jwt_token)
        if token is None or bearer != 'Bearer' or is_valid is False or is_valid is None:
            message = dict(message="Not Authorized",
                           status_code=status.HTTP_401_UNAUTHORIZED),

            if not AuthServices.is_valid(jwt_token):
                message = dict(message="Token Expired, request a new token",
                               status_code=status.HTTP_401_UNAUTHORIZED)

            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

        return function(*args, **kwargs)

    return wrapped



