from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from blog_project.utils.i18n import t as translate_func

register = template.Library()


@register.simple_tag(takes_context=True)
def page_text(context, page_settings, field_name, default_key):
    """Texte éditable d'une page (About, Contact, etc.) avec repli sur i18n JSON."""
    request = context.get('request')
    lang = None
    if request:
        lang = request.LANGUAGE_CODE
    lang_short = (lang or 'fr').split('-')[0].lower()

    value = ''
    if page_settings:
        if lang_short == 'en':
            value = getattr(page_settings, f'{field_name}_en', '') or ''
            if not value:
                value = getattr(page_settings, field_name, '') or ''
        else:
            value = getattr(page_settings, field_name, '') or ''

    if value:
        text = value
    else:
        text = translate_func(default_key, lang=lang_short)

    if request and request.GET.get('dashboard_preview'):
        return mark_safe(f'<span data-preview="{field_name}">{escape(text)}</span>')

    return text
