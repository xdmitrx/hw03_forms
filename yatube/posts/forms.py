from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    """Создание класса, наследуется от ModelForm."""

    class Meta:
        """Форма для работы с моделью Post."""

        model = Post
        fields = ('text', 'group')
