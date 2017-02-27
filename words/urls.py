
from words_api.settings import BASE_API_URL

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from words import views

urlpatterns = [
    url(r'^' + BASE_API_URL + 'words/$', views.WordList.as_view()),
    url(r'^' + BASE_API_URL + 'words/(?P<pk>[0-9]+)/$', views.WordDetail.as_view()),
    url(r'^' + BASE_API_URL + 'words/distance/$', views.WordDistance.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
