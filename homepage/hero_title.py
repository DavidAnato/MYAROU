"""Taille du titre hero accueil selon la longueur du texte (préfixe + suffixe)."""

from blog_project.utils.i18n import t as translate_func


def _resolve_field(home, field_name: str, default_key: str, lang_short: str) -> str:
    if not home:
        return translate_func(default_key, lang=lang_short) or ''

    if lang_short == 'en':
        value = (getattr(home, f'{field_name}_en', '') or '').strip()
        if not value:
            value = (getattr(home, field_name, '') or '').strip()
    else:
        value = (getattr(home, field_name, '') or '').strip()

    if value:
        return value
    return (translate_func(default_key, lang=lang_short) or '').strip()


def home_hero_title_char_count(home, lang_short: str = 'fr') -> int:
    """Nombre de caractères du titre (préfixe + suffixe) pour la langue active."""
    lang_short = (lang_short or 'fr').split('-')[0].lower()
    prefix = _resolve_field(
        home,
        'hero_title_prefix',
        'site.home.hero.title_prefix',
        lang_short,
    )
    suffix = _resolve_field(
        home,
        'hero_title_suffix',
        'site.home.hero.title_suffix',
        lang_short,
    )
    return len(prefix) + len(suffix)
