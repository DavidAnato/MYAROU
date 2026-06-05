from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

_PREVIEW_KEYS = {
    'title': 'article_title',
    'excerpt': 'article_excerpt',
    'content': 'article_content',
    'name': 'article_category',
}


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
    else:
        value = getattr(article, field_name, '')
    request = context.get('request')
    if request and request.GET.get('dashboard_preview'):
        preview_key = _PREVIEW_KEYS.get(field_name)
        if preview_key:
            if field_name == 'content':
                return mark_safe(f'<div data-preview-html="{preview_key}">{value}</div>')
            return mark_safe(f'<span data-preview="{preview_key}">{escape(value)}</span>')
    if field_name in ('content', 'excerpt', 'description'):
        return mark_safe(value)
    return value


@register.simple_tag(takes_context=True)
def category_field(context, category, field_name):
    if not category:
        return ''
    getter = f'get_{field_name}'
    if hasattr(category, getter):
        value = getattr(category, getter)(_lang_from_context(context))
    else:
        value = getattr(category, field_name, '')
    request = context.get('request')
    if request and request.GET.get('dashboard_preview') and field_name == 'name':
        return mark_safe(f'<span data-preview="article_category">{escape(value)}</span>')
    if field_name == 'description':
        return mark_safe(value)
    return value
