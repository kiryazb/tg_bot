from rest_framework import serializers
import datetime as dt
from posts.models import Post, Group, Comment
from django.contrib.auth import get_user_model


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    pub_date = serializers.DateTimeField(
        read_only=True,
        default=dt.datetime.now()
    )
    image = serializers.ImageField(
        read_only=True,
        default=None
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'pub_date',
            'author',
            'image',
            'group'
        )
        read_only_fields = ('id', 'pub_date', 'author', 'image')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'slug',
            'description'
        )


class CommentSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(
        read_only=True,
        default=dt.datetime.now()
    )
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'post',
            'text',
            'created'
        )

        read_only_fields = ('id', 'created', 'author', 'post')

    def create(self, validated_data):
        post_id = self.context['view'].kwargs['post_id']
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.create(post=post, **validated_data)
        return comment


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name',
            'last_name', 'posts', 'comments'
        )
        ref_name = 'ReadOnlyUsers'
