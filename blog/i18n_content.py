"""Helpers pour le contenu blog multilingue (repli FR si EN absent)."""


def normalize_lang(language_code):
    return (language_code or 'fr').split('-')[0].lower()


def pick_localized(language_code, fr_value, en_value):
    """Retourne la valeur EN si demandée et disponible, sinon FR."""
    lang = normalize_lang(language_code)
    fr = (fr_value or '').strip() if fr_value is not None else ''
    en = (en_value or '').strip() if en_value is not None else ''
    if lang == 'en':
        return en or fr
    return fr or en
