from rest_framework import viewsets, mixins, filters, permissions
# from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
# from django_filters.rest_framework import DjangoFilterBackend
from .pagination import PostsPagination
# from .throttling import WorkingHoursRateThrottle
from .permissions import OwnerOrReadOnly, ReadOnly
from datetime import datetime as dt
from posts.models import Post, User, Comment, Group, Follow
from rest_framework.exceptions import ValidationError

from .serializers import (
    PostSerializer,
    UserSerializer,
    CommentSerializer,
    GroupSerializer,
    FollowSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = PostsPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, pub_date=dt.now())

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернём обновлённый перечень используемых пермишенов
            return (ReadOnly(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post, created=dt.now())

    def get_queryset(self):
        self.post = self.kwargs['post_id']
        return Comment.objects.filter(post=self.post)

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернём обновлённый перечень используемых пермишенов
            return (ReadOnly(),)
        return super().get_permissions()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        user = self.request.user
        following = serializer.validated_data.get('following')
        if following == user or Follow.objects.filter(
            user=user,
            following=following
        ):
            raise ValidationError()
        serializer.save(user=self.request.user)

    def get_queryset(self):
        query_set = Follow.objects.filter(user=self.request.user)
        return query_set
