from django import template

register = template.Library()


@register.filter
def localized_link_label(link, language_code='fr'):
    if not link:
        return ''
    if hasattr(link, 'get_label'):
        return link.get_label(language_code)
    return getattr(link, 'label', '') or ''
