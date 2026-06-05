from django.db.models import Q

from blog.category_i18n_defaults import sync_categories_en_names

from .custom_page_nav import sync_all_custom_pages_footer_nav
from .site_links_defaults import sync_site_links_en_labels
from .models_site import SiteLink, SiteSettings
from .page_nav import build_main_nav_items
from .page_visibility import is_route_publicly_visible
from .site_links_defaults import ensure_default_site_links


def _link_is_available(link):
    if link.custom_page_id:
        page = link.custom_page
        return bool(page and page.is_published and page.show_in_nav)
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
    sync_site_links_en_labels()
    sync_categories_en_names()
    sync_all_custom_pages_footer_nav()
    site = SiteSettings.get_solo()
    language_code = getattr(request, 'LANGUAGE_CODE', 'fr')
    return {
        'site_settings': site,
        'footer_bio_text': site.get_footer_bio(language_code),
        'social_links': _active_links(SiteLink.CATEGORY_SOCIAL),
        'nav_links': _active_links(SiteLink.CATEGORY_NAV),
        'footer_links': _active_links(SiteLink.CATEGORY_FOOTER),
        'main_nav_items': build_main_nav_items(language_code),
        'redirect_to': request.get_full_path() if request else '',
    }
