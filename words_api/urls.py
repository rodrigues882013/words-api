from django.conf.urls import url, include
from django.contrib import admin

from settings import BASE_API_URL
from words import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^' + BASE_API_URL + 'auth/request_access/$', views.RequestAccess.as_view()),
    url(r'^', include('words.urls'))


]
