from django import template
from app.models import Favorite  # アプリのモデルをインポート

register = template.Library()

@register.filter
def is_favorite(user, company):
    if user.is_authenticated:
        return Favorite.objects.filter(user=user, company=company).exists()
    return False

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

