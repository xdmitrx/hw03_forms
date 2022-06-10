from datetime import datetime


def year(request):
    """Добавляет в контекст шаблона страницы переменную year."""
    date_time = datetime.now().year

    return {'year': date_time}
