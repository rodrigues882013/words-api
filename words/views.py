

import json
import logging
from json import loads

from django.db import IntegrityError
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from words.models import Word
from words.serializers import WordSerializer
from words.services import WordService, AuthServices, auth_jwt

# Get an instance of a logger
logger = logging.getLogger(__name__)


class WordDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer

    @auth_jwt
    def get(self, request, *args, **kwargs):
        logger.info("Retrieve word")
        logger.debug("Retrieve word with id: %s", kwargs.get('pk'))
        return self.retrieve(request, *args, **kwargs)

    @auth_jwt
    def put(self, request, *args, **kwargs):
        logger.info("Update word")
        logger.debug("Update word with id: %s", kwargs.get('pk'))
        return self.update(request, *args, **kwargs)

    @auth_jwt
    def delete(self, request, *args, **kwargs):
        logger.info("Delete word")
        logger.debug("Delete word with id: %s", kwargs.get('pk'))
        return self.destroy(request, *args, **kwargs)


class WordList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer

    @auth_jwt
    def get(self, request, *args, **kwargs):
        logger.info("Listing resource")
        keyword = ''
        threshold = 3

        if request.GET:

            if 'key' in request.GET:
                keyword = request.GET['key']
            if 't' in request.GET:
                threshold = request.GET['t']

            self.queryset = WordService.filter_words(keyword=keyword,
                                                     threshold=threshold)

        return self.list(request, *args, **kwargs)

    @auth_jwt
    def post(self, request, *args, **kwargs):
        try:
            logger.debug("Creating the word: %s", json.loads(request.body).get("word"))

            if json.loads(request.body).get("word") == "" or "word" not in json.loads(request.body):
                raise ValueError

            return self.create(request, *args, **kwargs)

        except ValueError:
            logger.error("JSON is not a valid value")
            return Response(data=dict(message="JSON is not valid"), status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            logger.error("Resource already exist")
            return Response(data=dict(message="Resource already exist"), status=status.HTTP_409_CONFLICT)


class RequestAccess(APIView):

    def post(self, request, format=None):

        try:
            credentials = loads(request.body)
            token = AuthServices.verify_user(username=credentials.get('username'),
                                             password=credentials.get('password'),
                                             email=credentials.get('email'))

            if WordService.is_empty(credentials.get('username')) or\
               WordService.is_empty(credentials.get('password')) or \
               WordService.is_empty(credentials.get('email')):

                raise ValueError

            return Response(dict(token=token), status=status.HTTP_202_ACCEPTED)

        except ValueError:
            logger.error("JSON is not a valid value")
            return Response(data=dict(message="JSON is not valid"), status=status.HTTP_400_BAD_REQUEST)


class WordDistance(APIView):

    @auth_jwt
    def post(self, request, format=None):
        data = dict()

        try:
            words = loads(request.body)
            logger.debug("Calculate distance between %s and %s", words.get('word1'), words.get('word2'))

            w1 = words.get('word1')
            w2 = words.get('word2')

            if WordService.is_empty(w1) or WordService.is_empty(w2):
                raise ValueError

            distance = WordService.compute_distance(w1, w2)
            data = dict(word1=w1, word2=w2, distance=distance)

        except ValueError:
            return Response(dict(message="Bad Request"), status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_201_CREATED)
