# serializers.py
from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    character_quantity = serializers.SerializerMethodField()
    publication_date = serializers.DateTimeField(source='pub_date', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'image',
                  'character_quantity', 'publication_date')
        model = Post

    def get_character_quantity(self, obj):
        return len(obj.text)