from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField


from posts.models import Comment, Post, User, Group, Follow
from django.core.files.base import ContentFile
import base64


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)
    followings = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'posts',
            'followings'
        )
        ref_name = 'ReadOnlyUsers'


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = '__all__'
        model = Post
        read_only_fields = ('id', 'author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('id', 'created', 'author', 'post')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'slug',
            'description'
        )


class FollowSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ('__all__')
        read_only_fields = ('id', 'user')
