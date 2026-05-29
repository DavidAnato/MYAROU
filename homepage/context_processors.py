from django.db.models import Q

from .models_site import SiteLink, SiteSettings
from .page_nav import build_main_nav_items
from .page_visibility import is_route_publicly_visible
from .site_links_defaults import ensure_default_site_links


def _link_is_available(link):
    if link.route_name:
        return is_route_publicly_visible(link.route_name)
    return bool(link.url)


def _active_links(category):
    qs = SiteLink.objects.filter(
        category=category,
        is_active=True,
    ).filter(Q(url__gt='') | ~Q(route_name=''))
    return [link for link in qs if _link_is_available(link)]


def site_globals(request):
    ensure_default_site_links()
    site = SiteSettings.get_solo()
    language_code = getattr(request, 'LANGUAGE_CODE', 'fr')
    return {
        'site_settings': site,
        'social_links': _active_links(SiteLink.CATEGORY_SOCIAL),
        'nav_links': _active_links(SiteLink.CATEGORY_NAV),
        'footer_links': _active_links(SiteLink.CATEGORY_FOOTER),
        'main_nav_items': build_main_nav_items(language_code),
    }
