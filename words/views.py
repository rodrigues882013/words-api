from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import mixins

from words.models import Word
from words.serializers import WordSerializer
from words.constants import Constants

from json import dumps


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


@csrf_exempt
def distance(request, **kwargs):
    kwargs['content_type'] = 'application/json'

    if request.method == Constants.HTTP_POST:
        print kwargs

    return dumps(dict(teste=1))

# class JSONResponse(HttpResponse):
#
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)
#
#
# @csrf_exempt
# def get_all(request):
#
#     if request.method == Constants.HTTP_GET:
#         words = Word.objects.all()
#         serializer = WordSerializer(words, many=True)
#         return JSONResponse(serializer.data)
#
#     else:
#         return JSONResponse(dict("Bad Request"), tatus=404)
#
#
# @csrf_exempt
# def create(request):
#
#     if request.method == Constants.HTTP_POST:
#
#         data = JSONParser().parse(request)
#         serializer = WordSerializer(data=data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data)
#         return JSONResponse(serializer.errors, status=400)
#
#
# @csrf_exempt
# def get(request, pk):
#
#     if request.method == Constants.HTTP_GET:
#
#         try:
#             word = Word.objects.get(pk=pk)
#         except Word.DoesNotExist:
#             return HttpResponse(status=404)
#
#         serializer = WordSerializer(word)
#         return JSONResponse(serializer.data)
#
#
# @csrf_exempt
# def distance(request, **kwargs):
#
#     if request.method == Constants.HTTP_POST:
#         pass
#
#     return JSONResponse("")
