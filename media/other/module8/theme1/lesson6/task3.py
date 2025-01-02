# views.py
from rest_framework.views import APIView
from rest_framework import generics

from .models import Post
from .serializers import PostSerializer


class APIPostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class APIPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# urls.py
from django.urls import path

from .views import APIPostList, APIPostDetail

urlpatterns = [
   path('api/v1/posts/', APIPostList.as_view()),
   path('api/v1/posts/<pk>/', APIPostDetail.as_view()),
]

# serializers.py
from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'text', 'author', 'image', 'pub_date')
        model = Post