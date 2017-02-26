
from django.conf.urls import url, include
from django.contrib import admin

from words import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('words.urls')),
    url(r'^api/v1/auth/request_access/$', views.RequestAccess.as_view()),

]
