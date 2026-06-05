"""Libellés EN par défaut pour les liens du site (footer, navigation)."""

from blog_project.utils.i18n import load_translations

from .models_site import BUILTIN_PAGE_LABELS_EN

# Libellés FR → EN pour les liens footer par défaut
_STATIC_FR_TO_EN = {
    'Accueil': 'Home',
    'À propos': 'About',
    'Blog': 'Blog',
    'Galerie': 'Gallery',
    'Contact': 'Contact',
    'Nos programmes': 'Our programs',
    'Soutiens': 'Support',
    'Devenir bénévole': 'Become a volunteer',
}

_ROUTE_LABEL_EN = dict(BUILTIN_PAGE_LABELS_EN)
_ROUTE_LABEL_EN.update({
    'blog:contact': 'Contact',
})


def _i18n_fr_en_pairs():
    """Paires FR/EN extraites des clés menu et footer i18n."""
    load_translations()
    from blog_project.utils import i18n as i18n_mod
    fr = i18n_mod._TRANSLATIONS.get('fr', {})
    en = i18n_mod._TRANSLATIONS.get('en', {})
    pairs = dict(_STATIC_FR_TO_EN)
    prefixes = ('site.footer.', 'site.menu.')
    for key, fr_val in fr.items():
        if not key.startswith(prefixes):
            continue
        en_val = en.get(key)
        if fr_val and en_val and fr_val != en_val:
            pairs[fr_val.strip()] = en_val.strip()
    return pairs


FR_TO_EN_LABELS = _i18n_fr_en_pairs()


def guess_label_en(label_fr, route_name='', custom_page=None):
    """Devine le libellé EN à partir du français, de la route ou d'une page libre."""
    if custom_page is not None:
        return (custom_page.title_en or custom_page.title or '').strip()
    route = (route_name or '').strip()
    if route and route in _ROUTE_LABEL_EN:
        return _ROUTE_LABEL_EN[route]
    fr = (label_fr or '').strip()
    if fr:
        return FR_TO_EN_LABELS.get(fr, '')
    return ''
