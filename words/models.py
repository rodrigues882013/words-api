
from __future__ import unicode_literals
from django.db import models


class Word(models.Model):

    word = models.CharField(max_length=100)

    def __unicode__(self):
        return str(self.word)

    def get_word(self):
        return self.__unicode__()
