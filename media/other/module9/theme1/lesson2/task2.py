# api.throttling
# импортируйте в код все необходимое
import datetime
from rest_framework import throttling


class LunchBreakThrottle(throttling.BaseThrottle):

    def allow_request(self, request, view):
        now = datetime.datetime.now().hour
        if now >= 13 and now < 14:
            return False
        return True
    
# api.views
from rest_framework import generics, permissions
from .throttling import LunchBreakThrottle

from posts.models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnlyPermission
# импортируйте в код все необходимое


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    throttle_classes = (LunchBreakThrottle,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    throttle_classes = (LunchBreakThrottle,)