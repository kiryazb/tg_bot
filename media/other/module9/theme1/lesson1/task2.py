# api.permissions
from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
        
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.author == request.user

# api.views
from rest_framework import generics, permissions
from .permissions import IsAuthorOrReadOnlyPermission

from posts.models import Post
from .serializers import PostSerializer
# Импортируйте в код все необходимое


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)