import json
from django.conf import settings
from pathlib import Path
from django.utils.translation import get_language

_TRANSLATIONS = {}

def load_translations():
    """Charge les fichiers JSON de traduction en mémoire."""
    base_path = Path(settings.BASE_DIR) / "i18n"
    if not base_path.exists():
        return

    for file in base_path.glob("*.json"):
        lang = file.stem
        try:
            with open(file, encoding="utf-8") as f:
                _TRANSLATIONS[lang] = json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement de {file}: {e}")

def t(key, lang=None, **kwargs):
    """
    Récupère une traduction pour une clé donnée.
    Si lang n'est pas fourni, utilise la langue courante de Django.
    """
    if lang is None:
        lang = get_language()
        if lang:
            # Django utilise 'fr-fr' ou 'en-us', mais nos fichiers sont 'fr' ou 'en'
            lang = lang.split('-')[0]
    
    # Fallback to 'fr' if lang is not found or None
    if not lang or lang not in _TRANSLATIONS:
        lang = 'fr'

    text = _TRANSLATIONS.get(lang, {}).get(key, key)
    
    # Interpolation des variables {{variable}}
    if isinstance(text, str):
        for k, v in kwargs.items():
            text = text.replace(f"{{{{{k}}}}}", str(v))
            
    return text
