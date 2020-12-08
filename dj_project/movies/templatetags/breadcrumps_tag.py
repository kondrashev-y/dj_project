from django import template
from django.urls import reverse

from ..models import Category

register = template.Library()


class ActorList:
    """Класс для yrl Актеров и Режиссеров"""
    get_absolute_url = reverse('actor_list')

    def __str__(self):
        return 'Актеры и Режиссеры'


class RatingList:
    """Класс для yrl Актеров и Режиссеров"""
    get_absolute_url = '#'   # заглушка вместо  reverse('rating_list') пока нет шаблона для рейтинга

    def __str__(self):
        return 'Рэйтинг'


@register.inclusion_tag('breadcrumbs_template.html', takes_context=True)
def breadcrumbs(context):

    crumbs = []
    path = context.get('request').path
    if context.get('movie'):
        model = context['movie']
        crumbs.append(model.category)
        crumbs.append(model)
    elif '/category/' in path:
        crumbs.append(get_category(context['view'].kwargs.get('slug')))
    elif '/filter/' in path:
        crumbs.append('Фильтр')
    elif 'search/' in path:
        crumbs.append('Поиск')
    elif 'actor' in path:
        crumbs.append(ActorList)
        if context.get('actor'):
            crumbs.append(context['actor'])
    elif '/rating/' in path:
        crumbs.append(RatingList)
        crumbs.append(context['view'].kwargs.get('rt'))
    return {'crumbs': crumbs}


def get_category(slug):
    category_name = Category.objects.get(url=slug)
    return category_name


