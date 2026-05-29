"""Pages intégrées par défaut (visibilité / menu)."""

from .models_site import BUILTIN_PAGE_LABELS_EN, SitePage

DEFAULT_SITE_PAGES = [
    {'route_name': 'blog:home', 'label': 'Accueil', 'order': 0},
    {'route_name': 'blog:about', 'label': 'À propos', 'order': 10},
    {'route_name': 'blog:article_list', 'label': 'Blog', 'order': 20},
    {'route_name': 'blog:gallery', 'label': 'Galerie', 'order': 30},
    {'route_name': 'blog:contact', 'label': 'Contact', 'order': 40},
]


def ensure_default_site_pages():
    """Crée les pages intégrées si absentes (idempotent)."""
    for item in DEFAULT_SITE_PAGES:
        route_name = item['route_name']
        if SitePage.objects.filter(route_name=route_name).exists():
            continue
        SitePage.objects.create(
            route_name=route_name,
            label=item['label'],
            label_en=BUILTIN_PAGE_LABELS_EN.get(route_name, item['label']),
            order=item['order'],
            is_visible=True,
            show_in_nav=True,
        )
