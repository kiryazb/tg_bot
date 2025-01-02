# views.py
# Импортируйте в код всё необходимое
from .serializers import PostSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import Post
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def api_posts(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

# urls.py
# Импортируйте в код всё необходимое
from .views import api_posts
from django.urls import path

urlpatterns = [
    path('api/v1/posts/', api_posts),
]

# serializers.py
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'text', 'author', 'image', 'pub_date')
        model = Post