# coding=utf-8
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.db import models


@python_2_unicode_compatible
class Word(models.Model):

    word = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.word

    def get_word(self):
        return self.__str__()


@python_2_unicode_compatible
class Token(models.Model):

    token = models.CharField(max_length=512)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.token

    def get_token(self):
        return self.__str__()
