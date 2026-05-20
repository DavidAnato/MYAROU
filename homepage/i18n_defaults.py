"""Chargement des textes par défaut depuis i18n/*.json pour les pages éditables."""
import json
from django.conf import settings


def _load_lang(language_code: str) -> dict:
    lang = (language_code or 'fr').split('-')[0].lower()
    if lang not in ('fr', 'en'):
        lang = 'fr'
    path = settings.BASE_DIR / 'i18n' / f'{lang}.json'
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {}


def apply_i18n_defaults(instance, mapping: dict, language_code: str = 'fr') -> list[str]:
    """
    mapping: {field_name: i18n_key}
    Pour les champs *_en, ajouter la clé avec suffixe _en dans mapping si besoin.
    """
    fr = _load_lang('fr')
    en = _load_lang('en')
    changed = []
    for field_name, i18n_key in mapping.items():
        if field_name.endswith('_en'):
            base_key = i18n_key
            value = en.get(base_key, '')
        else:
            value = fr.get(i18n_key, '')
        current = getattr(instance, field_name, None)
        if current is None or current == '':
            setattr(instance, field_name, value)
            changed.append(field_name)
    return changed


def merge_fr_en_defaults(mapping: dict) -> dict:
    """Duplique le mapping FR vers champs _en (même clé i18n, fichier en.json)."""
    merged = dict(mapping)
    for field, key in list(mapping.items()):
        if not field.endswith('_en'):
            merged[f'{field}_en'] = key
    return merged
