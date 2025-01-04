from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet


router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'posts/(?P<post_id>[^/.]+)/comments', CommentViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'follow', FollowViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
