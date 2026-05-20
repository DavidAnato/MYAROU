"""Liens footer / navigation par défaut (équivalent à l’ancien footer figé)."""

from .models_site import SiteLink

DEFAULT_NAV_LINKS = [
    {'route_name': 'blog:home', 'label': 'Accueil', 'order': 0},
    {'route_name': 'blog:about', 'label': 'À propos', 'order': 10},
    {'route_name': 'blog:article_list', 'label': 'Blog', 'order': 20},
    {'route_name': 'blog:gallery', 'label': 'Galerie', 'order': 30},
    {'route_name': 'blog:contact', 'label': 'Contact', 'order': 40},
]

DEFAULT_BARIKA_LINKS = [
    {'route_name': 'blog:contact', 'label': 'Nos programmes', 'order': 0},
    {'route_name': 'blog:contact', 'label': 'Soutiens', 'order': 10},
    {'route_name': 'blog:contact', 'label': 'Devenir bénévole', 'order': 20},
]


def ensure_default_site_links():
    """Crée les liens navigation / MY BARIKA s’ils manquent (idempotent)."""
    if not SiteLink.objects.filter(category=SiteLink.CATEGORY_NAV).exists():
        for item in DEFAULT_NAV_LINKS:
            SiteLink.objects.create(
                category=SiteLink.CATEGORY_NAV,
                platform='website',
                label=item['label'],
                route_name=item['route_name'],
                url='',
                order=item['order'],
                is_active=True,
                open_in_new_tab=False,
            )

    if not SiteLink.objects.filter(category=SiteLink.CATEGORY_FOOTER).exists():
        for item in DEFAULT_BARIKA_LINKS:
            SiteLink.objects.create(
                category=SiteLink.CATEGORY_FOOTER,
                platform='website',
                label=item['label'],
                route_name=item['route_name'],
                url='',
                order=item['order'],
                is_active=True,
                open_in_new_tab=False,
            )
