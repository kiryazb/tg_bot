# serializers.py
#  импортируйте в код всё необходимое
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('text', 'pub_date', 'author')
        model = Post