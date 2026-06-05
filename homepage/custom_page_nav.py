"""Synchronisation des pages libres dans la navigation footer."""

from .models_site import CustomPage, SiteLink


def sync_custom_page_footer_nav(page):
    """Ajoute ou retire une page libre de la colonne Navigation du footer."""
    qs = SiteLink.objects.filter(category=SiteLink.CATEGORY_NAV, custom_page=page)
    if page.show_in_nav and page.is_published:
        link, created = SiteLink.objects.get_or_create(
            category=SiteLink.CATEGORY_NAV,
            custom_page=page,
            defaults={
                'platform': 'website',
                'label': page.title,
                'label_en': page.title_en,
                'url': '',
                'route_name': '',
                'order': page.order,
                'is_active': True,
                'open_in_new_tab': False,
            },
        )
        if not created:
            link.label = page.title
            link.label_en = page.title_en
            link.order = page.order
            link.is_active = True
            link.save(update_fields=['label', 'label_en', 'order', 'is_active'])
    else:
        qs.delete()


def sync_all_custom_pages_footer_nav():
    """Resynchronise toutes les pages libres visibles dans le menu."""
    linked_ids = set(
        SiteLink.objects.filter(
            category=SiteLink.CATEGORY_NAV,
            custom_page__isnull=False,
        ).values_list('custom_page_id', flat=True)
    )
    active_ids = set(
        CustomPage.objects.filter(is_published=True, show_in_nav=True).values_list('pk', flat=True)
    )
    for page in CustomPage.objects.filter(pk__in=active_ids):
        sync_custom_page_footer_nav(page)
    stale_ids = linked_ids - active_ids
    if stale_ids:
        SiteLink.objects.filter(
            category=SiteLink.CATEGORY_NAV,
            custom_page_id__in=stale_ids,
        ).delete()
