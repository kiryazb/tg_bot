# urls.py
from django.urls import path
from rest_framework.authtoken import views
from .views import api_posts, api_posts_detail
# импортируйте нужную функцию


urlpatterns = [
    path('api/v1/posts/', api_posts),
    path('api/v1/posts/<int:pk>/', api_posts_detail),
    path('api/v1/api-token-auth/', views.obtain_auth_token)
]

# view.py
from django.shortcuts import get_object_or_404
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
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_posts_detail(request, pk):
    post = get_object_or_404(Post, id=pk)

    # напишем обработчик для метода GET
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    # получаем пользователя из запроса
    user = request.user
    # если пользователь, обратившийся к API, не является автором поста,
    # то к методам, идущим после GET, мы его не пропускаем
    # и возвращаем ответ со статусом 403
    if user != post.author:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# serializers.py
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        fields = ('id', 'text', 'author', 'image', 'pub_date')
        # укажите поля, доступные только для чтения
        model = Post