"""Disposition des champs de formulaire dashboard (style page d'accueil)."""

from django import forms

LONG_FIELD_PARTS = (
    'description', 'profile_p', 'vision_quote', 'faq_a', 'form_description',
    'footer_bio', 'journey_item', '_desc', 'quote_text',
)

IMAGE_FIELDS = frozenset({
    'profile_image', 'hero_right_image', 'quote_image',
})

SITE_FORM_SECTIONS = [
    ('Coordonnées & notifications', [
        'contact_email', 'contact_location', 'contact_notify_email',
        'footer_bio', 'footer_bio_en',
    ]),
]

SECTION_META = {
    'Hero': {'icon': 'sparkles', 'subtitle': 'Titre et introduction', 'open': True},
    'Profil': {'icon': 'user', 'subtitle': 'Photo, textes et statistiques', 'open': True},
    'Parcours (timeline)': {'icon': 'timeline', 'subtitle': 'Étapes du parcours', 'open': False},
    'Vidéo': {'icon': 'video', 'subtitle': 'Intégration YouTube', 'open': False},
    'Valeurs': {'icon': 'heart', 'subtitle': 'Piliers et descriptions', 'open': False},
    'Vision & CTA': {'icon': 'flag', 'subtitle': 'Citation et boutons', 'open': False},
    'En-tête de la page': {'icon': 'photo', 'subtitle': 'Titre de la galerie', 'open': True},
    'Formulaire': {'icon': 'mail', 'subtitle': 'Textes du formulaire', 'open': True},
    'Encadrés latéraux': {'icon': 'layout', 'subtitle': 'Blocs latéraux', 'open': False},
    'FAQ': {'icon': 'help', 'subtitle': 'Questions fréquentes', 'open': False},
    'Coordonnées & notifications': {'icon': 'settings', 'subtitle': 'E-mails et pied de page', 'open': True},
}


def _human_label(name):
    return name.replace('_', ' ').replace(' en', ' (EN)').title()


def _is_long_field(name):
    return any(part in name for part in LONG_FIELD_PARTS)


def _is_image_field(name, field):
    return (
        name in IMAGE_FIELDS
        or ('image' in name and isinstance(getattr(field, 'field', None), object)
            and isinstance(field.field.widget, forms.FileInput))
    )


def build_section_layout(form, sections_spec, clear_image_field=None):
    """Construit sections avec lignes pair / full / image / single."""
    layouts = []
    for title, field_names in sections_spec:
        meta = SECTION_META.get(title, {})
        rows = []
        names = [n for n in field_names if n in form.fields]
        i = 0
        while i < len(names):
            name = names[i]
            if name.endswith('_en'):
                i += 1
                continue

            en_name = f'{name}_en'
            field = form[name]

            if en_name in names and i + 1 < len(names) and names[i + 1] == en_name:
                if _is_image_field(name, field):
                    rows.append({
                        'type': 'image',
                        'name': name,
                        'label': _human_label(name),
                        'field': field,
                        'clear_flag': 'clear_profile_image' if name == clear_image_field else None,
                    })
                    i += 2
                    continue
                if _is_long_field(name):
                    rows.append({
                        'type': 'stacked',
                        'label': _human_label(name),
                        'fr_field': field,
                        'en_field': form[en_name],
                        'fr_name': name,
                        'en_name': en_name,
                    })
                else:
                    rows.append({
                        'type': 'pair',
                        'label': _human_label(name),
                        'fr_field': field,
                        'en_field': form[en_name],
                    })
                i += 2
                continue

            if _is_image_field(name, field):
                rows.append({
                    'type': 'image',
                    'name': name,
                    'label': _human_label(name),
                    'field': field,
                    'clear_flag': 'clear_profile_image' if name == clear_image_field else None,
                })
            elif _is_long_field(name):
                rows.append({
                    'type': 'single_full',
                    'label': _human_label(name),
                    'field': field,
                })
            else:
                rows.append({
                    'type': 'single',
                    'label': _human_label(name),
                    'field': field,
                })
            i += 1

        if rows:
            layouts.append({
                'title': title,
                'icon': meta.get('icon', 'doc'),
                'subtitle': meta.get('subtitle', ''),
                'open': meta.get('open', False),
                'rows': rows,
            })
    return layouts
