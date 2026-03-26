from django import template
from blog_project.utils.i18n import t as translate_func

register = template.Library()


@register.simple_tag(takes_context=True)
def home_text(context, home, field_name, default_key):
    request = context.get('request')
    lang = None
    if request:
        lang = request.LANGUAGE_CODE
    lang_short = (lang or 'fr').split('-')[0].lower()

    value = ''
    if home:
        if lang_short == 'en':
            value = getattr(home, f'{field_name}_en', '') or ''
            if not value:
                value = getattr(home, field_name, '') or ''
        else:
            value = getattr(home, field_name, '') or ''

    if value:
        return value

    return translate_func(default_key, lang=lang_short)

