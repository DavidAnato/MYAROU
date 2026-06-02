"""Métadonnées et helpers pour le page builder (blocs)."""

from django.utils.translation import gettext_lazy as _

BLOCK_TYPE_CHOICES = [
    ('hero', _('Hero')),
    ('richtext', _('Texte riche')),
    ('image', _('Image')),
    ('image_text', _('Image + texte')),
    ('gallery', _('Galerie')),
    ('video', _('Vidéo')),
    ('cta', _('Call-to-action')),
    ('faq', _('FAQ')),
    ('spacer', _('Espacement')),
]

BLOCK_TYPE_LABELS = dict(BLOCK_TYPE_CHOICES)

LAYOUT_IMAGE_TEXT = [
    ('image_left', 'Image à gauche'),
    ('image_right', 'Image à droite'),
]

LAYOUT_CTA = [
    ('primary', 'Vert (primaire)'),
    ('outline', 'Contour'),
]

LAYOUT_SPACER = [
    ('sm', 'Petit'),
    ('md', 'Moyen'),
    ('lg', 'Grand'),
]

BLOCK_LAYOUT_CHOICES = {
    'image_text': LAYOUT_IMAGE_TEXT,
    'cta': LAYOUT_CTA,
    'spacer': LAYOUT_SPACER,
}

BLOCK_LAYOUT_DEFAULTS = {
    'image_text': 'image_left',
    'cta': 'primary',
    'spacer': 'md',
}


def get_layout_choices(block_type):
    """Options de disposition valides pour un type de bloc."""
    return list(BLOCK_LAYOUT_CHOICES.get(block_type, []))


def get_layout_default(block_type):
    """Valeur par défaut de disposition pour un type de bloc."""
    return BLOCK_LAYOUT_DEFAULTS.get(block_type, '')


def normalize_layout(block_type, layout):
    """Retourne une disposition valide pour le type, ou la valeur par défaut."""
    choices = dict(get_layout_choices(block_type))
    if not choices:
        return ''
    if layout in choices:
        return layout
    return get_layout_default(block_type)


BLOCK_FIELDS = {
    'hero': ['badge', 'badge_en', 'title', 'title_en', 'subtitle', 'subtitle_en', 'image'],
    'richtext': ['content', 'content_en'],
    'image': ['image', 'image_alt', 'title', 'title_en'],
    'image_text': ['title', 'title_en', 'content', 'content_en', 'image', 'layout'],
    'gallery': ['title', 'title_en'],
    'video': ['title', 'title_en', 'subtitle', 'subtitle_en', 'video_url'],
    'cta': ['title', 'title_en', 'subtitle', 'subtitle_en', 'button_text', 'button_text_en', 'button_url', 'layout'],
    'faq': ['title', 'title_en', 'config'],
    'spacer': ['layout'],
}

SPACER_HEIGHTS = {'sm': 'h-8', 'md': 'h-16', 'lg': 'h-28'}

SECTION_BG_MAIN = 'main'
SECTION_BG_ALT = 'alt'

SECTION_BG_CLASSES = {
    SECTION_BG_MAIN: 'bg-white dark:bg-[#121212]',
    SECTION_BG_ALT: 'bg-gray-50 dark:bg-[#1a1a1a]',
}

SECTION_BACKGROUND_CHOICES = [
    ('inherit', 'Comme le bloc précédent'),
    ('main', 'Fond principal (blanc / sombre)'),
    ('alt', 'Fond alternatif (gris)'),
]


def section_bg_class(tone):
    """Classes Tailwind pour le fond d'une section."""
    if not tone:
        return ''
    return SECTION_BG_CLASSES.get(tone, SECTION_BG_CLASSES[SECTION_BG_MAIN])


def compute_section_backgrounds(blocks):
    """
    Calcule le fond de chaque bloc visible selon sa position.
    - Après un hero : alternance main → alt → main…
    - Espacement : couleur du bloc précédent par défaut (config.background)
    """
    result = {}
    tone_index = 0
    last_effective = SECTION_BG_MAIN

    for block in blocks:
        pk = block.pk
        if not pk:
            continue

        if block.block_type == 'hero':
            result[pk] = None
            tone_index = 0
            last_effective = SECTION_BG_MAIN
            continue

        if block.block_type == 'spacer':
            bg = (block.config or {}).get('background', 'inherit')
            if bg == SECTION_BG_MAIN:
                tone = SECTION_BG_MAIN
            elif bg == SECTION_BG_ALT:
                tone = SECTION_BG_ALT
            else:
                tone = last_effective
            result[pk] = tone
            last_effective = tone
            continue

        tone = SECTION_BG_MAIN if tone_index % 2 == 0 else SECTION_BG_ALT
        tone_index += 1
        result[pk] = tone
        last_effective = tone

    return result


BLOCK_CATALOG = [
    {'type': 'hero', 'label': 'Hero', 'description': 'Grande bannière en tête de page', 'color': 'emerald', 'icon': 'hero'},
    {'type': 'richtext', 'label': 'Texte riche', 'description': 'Paragraphes, listes, liens', 'color': 'sky', 'icon': 'text'},
    {'type': 'image', 'label': 'Image', 'description': 'Photo seule avec légende', 'color': 'violet', 'icon': 'image'},
    {'type': 'image_text', 'label': 'Image + texte', 'description': 'Photo et contenu côte à côte', 'color': 'indigo', 'icon': 'columns'},
    {'type': 'gallery', 'label': 'Galerie', 'description': 'Grille de plusieurs photos', 'color': 'pink', 'icon': 'gallery'},
    {'type': 'video', 'label': 'Vidéo', 'description': 'Intégration YouTube / Vimeo', 'color': 'rose', 'icon': 'video'},
    {'type': 'cta', 'label': 'Call-to-action', 'description': 'Encadré avec bouton', 'color': 'amber', 'icon': 'cta'},
    {'type': 'faq', 'label': 'FAQ', 'description': 'Questions / réponses', 'color': 'teal', 'icon': 'faq'},
    {'type': 'spacer', 'label': 'Espacement', 'description': 'Espace vertical entre sections', 'color': 'slate', 'icon': 'spacer'},
]

BLOCK_CATALOG_MAP = {item['type']: item for item in BLOCK_CATALOG}


def block_uses_gallery(block_type):
    return block_type == 'gallery'


def get_block_context(block, language_code='fr'):
    """Contexte de rendu pour un bloc."""
    return {
        'block': block,
        'lang': language_code,
        'title': block.get_title(language_code),
        'subtitle': block.get_subtitle(language_code),
        'content': block.get_content(language_code),
        'badge': block.get_badge(language_code),
        'button_text': block.get_button_text(language_code),
        'images': block.images.all() if block_uses_gallery(block.block_type) else [],
        'faq_items': block.get_faq_items(language_code),
        'template': f'blog/blocks/{block.block_type}.html',
    }
