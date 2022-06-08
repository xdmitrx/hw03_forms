from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):

    text = models.TextField('posts text')
    pub_date = models.DateTimeField('date', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts')
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True, null=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Group(models.Model):

    title = models.CharField('name', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    description = models.TextField('about')

    def __str__(self):
        return self.title
