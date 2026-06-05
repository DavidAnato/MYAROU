"""Remplissage automatique des noms EN des catégories."""

from homepage.link_i18n_defaults import FR_TO_EN_LABELS

from .models import Category


def sync_categories_en_names():
    """Remplit name_en manquant pour toutes les catégories."""
    for category in Category.objects.all():
        if category.name_en:
            continue
        guessed = FR_TO_EN_LABELS.get((category.name or '').strip(), '')
        if guessed:
            category.name_en = guessed
            category.save(update_fields=['name_en'])
