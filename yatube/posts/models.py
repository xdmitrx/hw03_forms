from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    """Создание модели Post."""

    text = models.TextField('текст поста')
    pub_date = models.DateTimeField('дата', auto_now_add=True)
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
        """Строковое представление объекта."""
        return self.text


class Group(models.Model):
    """Создание модели Group."""

    title = models.CharField('Заголовок', max_length=200,
                             help_text='Максимум 200 символов.')
    slug = models.SlugField('URL', max_length=200, unique=True,
                            help_text='Максимум 200 символов.')
    description = models.TextField('Содержание')

    def __str__(self):
        """Возвращает название группы."""
        return self.title
