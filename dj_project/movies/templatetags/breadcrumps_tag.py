from django import template

from ..models import Movie, Category
from ..views import MoviesView

register = template.Library()


@register.inclusion_tag('breadcrumbs_template.html', takes_context=True)
def breadcrumbs(context, obj=None, status=None):

    crumbs = []
    if status:
        crumbs.append(status)
    if context.get('movie'):
        crumbs.append(context['movie'].category)
        crumbs.append(context['movie'])
    if '/category/' in context.get('request').path:
        crumbs.append(get_category(context['view'].kwargs.get('slug')))
    if '/filter/' in context.get('request').path:
        crumbs.append('Фильтр')
    elif 'search/' in context.get('request').path:
        crumbs.append('Поиск')
    if 'actor' in context.get('request').path:
        crumbs.append('Актеры и Режиссеры')
    if context.get('actor'):
        crumbs.append(context['actor'])

    # print(context)
    # print(context['view'].kwargs.get('slug'))
    # print(context['request'].path)
    # print(context['actor'])
    return {'crumbs': crumbs}


def get_category(slug):
    category_name = Category.objects.get(url=slug)
    return category_name
