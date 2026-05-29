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
