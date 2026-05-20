from .models_site import SiteSettings, SiteLink


def site_globals(request):
    site = SiteSettings.get_solo()
    return {
        'site_settings': site,
        'social_links': SiteLink.objects.filter(
            category=SiteLink.CATEGORY_SOCIAL,
            is_active=True,
        ),
        'footer_links': SiteLink.objects.filter(
            category=SiteLink.CATEGORY_FOOTER,
            is_active=True,
        ),
        'useful_links': SiteLink.objects.filter(
            category=SiteLink.CATEGORY_USEFUL,
            is_active=True,
        ),
    }
