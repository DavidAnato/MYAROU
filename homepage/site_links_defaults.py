"""Liens footer / navigation par défaut (équivalent à l’ancien footer figé)."""

from .models_site import SiteLink

DEFAULT_NAV_LINKS = [
    {'route_name': 'blog:home', 'label': 'Accueil', 'label_en': 'Home', 'order': 0},
    {'route_name': 'blog:about', 'label': 'À propos', 'label_en': 'About', 'order': 10},
    {'route_name': 'blog:article_list', 'label': 'Blog', 'label_en': 'Blog', 'order': 20},
    {'route_name': 'blog:gallery', 'label': 'Galerie', 'label_en': 'Gallery', 'order': 30},
    {'route_name': 'blog:contact', 'label': 'Contact', 'label_en': 'Contact', 'order': 40},
]

DEFAULT_BARIKA_LINKS = [
    {'route_name': 'blog:contact', 'label': 'Nos programmes', 'label_en': 'Our programs', 'order': 0},
    {'route_name': 'blog:contact', 'label': 'Soutiens', 'label_en': 'Support', 'order': 10},
    {'route_name': 'blog:contact', 'label': 'Devenir bénévole', 'label_en': 'Become a volunteer', 'order': 20},
]


def ensure_default_site_links():
    """Crée les liens navigation / MY BARIKA s’ils manquent (idempotent)."""
    if not SiteLink.objects.filter(category=SiteLink.CATEGORY_NAV).exists():
        for item in DEFAULT_NAV_LINKS:
            SiteLink.objects.create(
                category=SiteLink.CATEGORY_NAV,
                platform='website',
                label=item['label'],
                label_en=item.get('label_en', ''),
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
                label_en=item.get('label_en', ''),
                route_name=item['route_name'],
                url='',
                order=item['order'],
                is_active=True,
                open_in_new_tab=False,
            )
