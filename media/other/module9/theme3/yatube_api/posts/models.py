from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    description = models.TextField()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owner')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='group',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    def clean(self):
        # Проверяем, что user не равен following
        if self.user == self.following:
            raise ValidationError()
