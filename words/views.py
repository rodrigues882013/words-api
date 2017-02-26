import json
from json import loads

from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from words.models import Word
from words.serializers import WordSerializer
from words.services import WordService, AuthServices, auth_jwt


class WordDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):

    queryset = Word.objects.all()
    serializer_class = WordSerializer

    @auth_jwt
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class WordList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):

    queryset = Word.objects.all()
    serializer_class = WordSerializer

    @auth_jwt
    def get(self, request, *args, **kwargs):

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
        return self.create(request, *args, **kwargs)


class RequestAccess(APIView):

    def post(self, request, format=None):
        credentials = loads(request.body)

        token = AuthServices.verify_user(username=credentials.get('username'),
                                         password=credentials.get('password'),
                                         email=credentials.get('email'))

        return Response(dict(token=token), status=status.HTTP_201_CREATED)


class Distance(APIView):

    @auth_jwt
    def post(self, request, format=None):
        words = loads(request.body)
        data = dict()

        try:
            w1 = words.get('word1')
            w2 = words.get('word2')
            distance = WordService.compute_distance(w1, w2)
            data = dict(word1=w1, word2=w2, distance=distance)

        except ValueError:
            Response(dict(message="Bad Request"), status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_201_CREATED)

