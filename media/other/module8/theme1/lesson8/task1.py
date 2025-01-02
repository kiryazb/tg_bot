# serializers.py
from rest_framework import serializers

from .models import Post, Group


class PostSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField( 
        queryset=Group.objects.all(), 
        slug_field='slug', 
        required=False,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'image', 'pub_date', 'group')
        model = Post

# urls.py
#  импортируйте в код всё необходимое
from django.urls import include, path
from rest_framework import routers

from .views import PostViewSet

router = routers.DefaultRouter()
router.register('api/v1/posts', PostViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

# views.py
#  импортируйте в код всё необходимое
from rest_framework import viewsets

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer