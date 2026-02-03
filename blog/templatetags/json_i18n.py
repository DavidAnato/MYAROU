from django import template
from blog_project.utils.i18n import t as translate_func

register = template.Library()

@register.simple_tag(takes_context=True)
def t(context, key, **kwargs):
    """
    Template tag pour traduire une chaîne en utilisant le système JSON.
    Usage: {% t "ma.cle" name="David" %}
    """
    request = context.get('request')
    lang = None
    if request:
        lang = request.LANGUAGE_CODE
    
    return translate_func(key, lang=lang, **kwargs)
