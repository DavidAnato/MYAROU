from django import template
from django.urls import resolve, Resolver404

register = template.Library()


@register.simple_tag(takes_context=True)
def is_active(context, *view_names):
    request = context.get('request')
    if not request:
        return False

    try:
        match = request.resolver_match
        if not match:
            match = resolve(request.path)

        if match.view_name in view_names:
            return True

        for name in view_names:
            if name.endswith(':') and match.view_name.startswith(name):
                return True

    except Resolver404:
        return False

    return False


@register.simple_tag(takes_context=True)
def nav_item_active(context, item):
    """Indique si un item de menu principal est actif."""
    request = context.get('request')
    if not request:
        return False
    try:
        match = request.resolver_match
        if not match:
            match = resolve(request.path)
        if item.get('kind') == 'custom':
            return (
                match.view_name == 'blog:custom_page'
                and match.kwargs.get('slug') == item.get('slug')
            )
        return match.view_name in item.get('active_views', [])
    except Resolver404:
        return False
