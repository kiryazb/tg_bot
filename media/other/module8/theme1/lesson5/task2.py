# views.py
#  импортируйте в код всё необходимое
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer


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


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_posts_detail(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = PostSerializer(post)
    return Response(serializer.data)

# urls.py
from django.urls import path
# Импортируйте необходимые view-функции
from . import views


urlpatterns = [
    path('api/v1/posts/', views.api_posts),
    path('api/v1/posts/<int:pk>/', views.api_posts_detail)
]