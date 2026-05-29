"""Construction du menu principal dynamique."""

from .models_site import CustomPage, SitePage
from .page_defaults import ensure_default_site_pages


def build_main_nav_items(language_code='fr'):
    ensure_default_site_pages()
    items = []

    for page in SitePage.objects.filter(show_in_nav=True):
        if page.route_name != 'blog:home' and not page.is_visible:
            continue
        items.append({
            'href': page.get_href(),
            'label': page.get_label(language_code),
            'active_views': page.get_active_views(),
            'icon': page.get_nav_icon(),
            'kind': 'builtin',
            'slug': '',
            'order': page.order,
        })

    for page in CustomPage.objects.filter(is_published=True, show_in_nav=True):
        items.append({
            'href': page.get_href(),
            'label': page.get_title(language_code),
            'active_views': ['blog:custom_page'],
            'icon': 'fa-file-lines',
            'kind': 'custom',
            'slug': page.slug,
            'order': page.order,
        })

    items.sort(key=lambda item: (item['order'], item['label'].lower()))
    return items
