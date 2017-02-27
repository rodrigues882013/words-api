from rest_framework import serializers

from .models import Word


class WordSerializer(serializers.ModelSerializer):
    word = serializers.CharField(required=False, allow_blank=True, max_length=100)

    class Meta:
        model = Word
        fields = ['word']

