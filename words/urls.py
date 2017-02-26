
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from words import views

urlpatterns = [
    url(r'^api/v1/words/$', views.WordList.as_view()),
    url(r'^api/v1/words/(?P<pk>[0-9]+)/$', views.WordDetail.as_view()),
    url(r'^api/v1/words/distance/$', views.Distance.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
