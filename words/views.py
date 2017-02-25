from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from words.models import Word
from words.serializers import WordSerializer
from words.services import WordService
from words.constants import Constants

from json import loads


class WordDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):

    queryset = Word.objects.all()
    serializer_class = WordSerializer

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

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class Distance(APIView):

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

