from .models_site import SiteSettings, SiteLink


def _active_links(category):
    return SiteLink.objects.filter(
        category=category,
        is_active=True,
    ).exclude(url='')


def site_globals(request):
    site = SiteSettings.get_solo()
    return {
        'site_settings': site,
        'social_links': _active_links(SiteLink.CATEGORY_SOCIAL),
        'footer_links': _active_links(SiteLink.CATEGORY_FOOTER),
        'useful_links': _active_links(SiteLink.CATEGORY_USEFUL),
    }
