from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CreationForm(UserCreationForm):
    """Создание класса, наследуется от UserCreationForm."""

    class Meta(UserCreationForm.Meta):
        """Форма для работы с моделью User."""

        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
