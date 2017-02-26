
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Word(models.Model):

    word = models.CharField(max_length=100)

    def __unicode__(self):
        return str(self.word)

    def get_word(self):
        return self.__unicode__()


class Token(models.Model):

    token = models.CharField(max_length=512)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __unicode__(self):
        return str(self.token)

    def get_token(self):
        return self.__unicode__()