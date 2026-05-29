"""Contrôle d’accès public aux pages intégrées."""

from django.http import Http404

ALWAYS_ACCESSIBLE_ROUTES = {'blog:home'}


def is_staff_preview(request):
    return (
        request.GET.get('dashboard_preview') == '1'
        and getattr(request.user, 'is_authenticated', False)
        and getattr(request.user, 'is_staff', False)
    )


def get_site_page(route_name):
    from .page_defaults import ensure_default_site_pages
    from .models_site import SitePage

    ensure_default_site_pages()
    return SitePage.objects.filter(route_name=route_name).first()


def is_route_publicly_visible(route_name):
    if route_name in ALWAYS_ACCESSIBLE_ROUTES:
        return True
    page = get_site_page(route_name)
    if page is None:
        return True
    return page.is_visible


def require_visible_page(route_name):
    def decorator(view_func):
        def wrapped(request, *args, **kwargs):
            if not is_staff_preview(request) and not is_route_publicly_visible(route_name):
                raise Http404
            return view_func(request, *args, **kwargs)
        wrapped.__name__ = view_func.__name__
        wrapped.__doc__ = view_func.__doc__
        return wrapped
    return decorator


class VisiblePageMixin:
    """Mixin pour vues basées sur classe : bloque l’accès si page masquée."""

    visible_route_name = None

    def dispatch(self, request, *args, **kwargs):
        route = self.visible_route_name
        if route and not is_staff_preview(request) and not is_route_publicly_visible(route):
            raise Http404
        return super().dispatch(request, *args, **kwargs)
