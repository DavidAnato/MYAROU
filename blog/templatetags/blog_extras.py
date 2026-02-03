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
            # Fallback for some test environments or edge cases
            match = resolve(request.path)
        
        if match.view_name in view_names:
            return True
            
        # Also check if the current view name starts with the provided name (for sub-sections)
        # But be careful: 'blog:home' shouldn't match 'blog:article_detail'
        # So exact match is safer for explicitly listed views.
        # If the user passes 'blog:', we could match all blog views.
        for name in view_names:
            if name.endswith(':') and match.view_name.startswith(name):
                return True
                
    except Resolver404:
        return False
        
    return False
