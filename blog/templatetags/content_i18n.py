from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def _lang_from_context(context):
    request = context.get('request')
    if request:
        return (getattr(request, 'LANGUAGE_CODE', None) or 'fr').split('-')[0].lower()
    return 'fr'


@register.simple_tag(takes_context=True)
def article_field(context, article, field_name):
    if not article:
        return ''
    getter = f'get_{field_name}'
    if hasattr(article, getter):
        value = getattr(article, getter)(_lang_from_context(context))
        if field_name in ('content', 'excerpt', 'description'):
            return mark_safe(value)
        return value
    return getattr(article, field_name, '')


@register.simple_tag(takes_context=True)
def category_field(context, category, field_name):
    if not category:
        return ''
    getter = f'get_{field_name}'
    if hasattr(category, getter):
        value = getattr(category, getter)(_lang_from_context(context))
        if field_name == 'description':
            return mark_safe(value)
        return value
    return getattr(category, field_name, '')
