from django.db.models import Q

from .models_site import SiteSettings, SiteLink
from .site_links_defaults import ensure_default_site_links


def _active_links(category):
    return SiteLink.objects.filter(
        category=category,
        is_active=True,
    ).filter(Q(url__gt='') | ~Q(route_name=''))


def site_globals(request):
    ensure_default_site_links()
    site = SiteSettings.get_solo()
    return {
        'site_settings': site,
        'social_links': _active_links(SiteLink.CATEGORY_SOCIAL),
        'nav_links': _active_links(SiteLink.CATEGORY_NAV),
        'footer_links': _active_links(SiteLink.CATEGORY_FOOTER),
        'useful_links': _active_links(SiteLink.CATEGORY_USEFUL),
    }
