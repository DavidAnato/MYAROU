from django import forms
from django.forms import inlineformset_factory, modelformset_factory

from homepage.models_site import (
    SiteSettings,
    SiteLink,
    AboutPageSettings,
    AboutGalleryImage,
    GalleryPageSettings,
    GalleryPageImage,
    ContactPageSettings,
)

WIDGET_CLASS = (
    'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 '
    'focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white '
    'dark:placeholder-gray-400 transition-colors'
)


def _style_form(form):
    for field in form.fields.values():
        w = field.widget
        if isinstance(w, forms.CheckboxInput):
            w.attrs['class'] = 'rounded border-gray-300 text-emerald-600 focus:ring-emerald-500'
        elif isinstance(w, forms.FileInput):
            w.attrs['class'] = (w.attrs.get('class', '') + ' ' + WIDGET_CLASS).strip()
            w.attrs.setdefault('accept', 'image/*')
        elif isinstance(w, forms.NumberInput):
            w.attrs['class'] = WIDGET_CLASS
        elif not isinstance(w, forms.HiddenInput):
            w.attrs['class'] = WIDGET_CLASS
        if isinstance(w, forms.Textarea):
            w.attrs.setdefault('rows', 3)


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'contact_email',
            'contact_location',
            'footer_bio',
            'footer_bio_en',
        ]
        widgets = {
            'footer_bio': forms.Textarea(attrs={'rows': 3}),
            'footer_bio_en': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style_form(self)


class SiteLinkForm(forms.ModelForm):
    class Meta:
        model = SiteLink
        fields = [
            'category', 'platform', 'label', 'route_name', 'url',
            'order', 'is_active', 'open_in_new_tab',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].required = False
        _style_form(self)

    def clean(self):
        cleaned = super().clean()
        url = (cleaned.get('url') or '').strip()
        route_name = cleaned.get('route_name') or ''
        if not url and not route_name:
            raise forms.ValidationError('Indiquez une page interne ou une URL.')
        if url and not url.startswith(('http://', 'https://', 'mailto:', '/')):
            if not route_name:
                cleaned['url'] = f'https://{url}'
        return cleaned

    def clean_url(self):
        return (self.cleaned_data.get('url') or '').strip()


class BaseSiteLinkFormSet(forms.BaseModelFormSet):
    """Ignore les lignes vides ; n'enregistre que les liens avec une URL."""

    def save(self, commit=True):
        if not commit:
            return super().save(commit=False)
        for form in self.deleted_forms:
            if form.instance.pk:
                form.instance.delete()
        saved = []
        for form in self.forms:
            if form in self.deleted_forms:
                continue
            if not form.cleaned_data:
                continue
            url = (form.cleaned_data.get('url') or '').strip()
            route_name = form.cleaned_data.get('route_name') or ''
            if not url and not route_name:
                continue
            saved.append(form.save())
        return saved


SiteLinkFormSet = modelformset_factory(
    SiteLink,
    form=SiteLinkForm,
    formset=BaseSiteLinkFormSet,
    extra=2,
    can_delete=True,
)


def _all_model_fields(model, exclude=()):
    return [f.name for f in model._meta.fields if f.name != 'id' and f.name not in exclude]


class AboutPageSettingsForm(forms.ModelForm):
    class Meta:
        model = AboutPageSettings
        fields = _all_model_fields(AboutPageSettings, exclude=())
        widgets = {
            'hero_description': forms.Textarea(attrs={'rows': 3}),
            'hero_description_en': forms.Textarea(attrs={'rows': 3}),
            'profile_p1': forms.Textarea(attrs={'rows': 4}),
            'profile_p1_en': forms.Textarea(attrs={'rows': 4}),
            'profile_p2': forms.Textarea(attrs={'rows': 4}),
            'profile_p2_en': forms.Textarea(attrs={'rows': 4}),
            'profile_p3': forms.Textarea(attrs={'rows': 4}),
            'profile_p3_en': forms.Textarea(attrs={'rows': 4}),
            'journey_description': forms.Textarea(attrs={'rows': 2}),
            'journey_description_en': forms.Textarea(attrs={'rows': 2}),
            'video_description': forms.Textarea(attrs={'rows': 2}),
            'video_description_en': forms.Textarea(attrs={'rows': 2}),
            'values_description': forms.Textarea(attrs={'rows': 2}),
            'values_description_en': forms.Textarea(attrs={'rows': 2}),
            'vision_quote': forms.Textarea(attrs={'rows': 3}),
            'vision_quote_en': forms.Textarea(attrs={'rows': 3}),
            'cta_description': forms.Textarea(attrs={'rows': 2}),
            'cta_description_en': forms.Textarea(attrs={'rows': 2}),
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style_form(self)


class AboutGalleryImageForm(forms.ModelForm):
    class Meta:
        model = AboutGalleryImage
        fields = ('image', 'order')
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
            'order': forms.NumberInput(attrs={'min': 0, 'step': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style_form(self)


AboutGalleryImageFormSet = inlineformset_factory(
    AboutPageSettings,
    AboutGalleryImage,
    form=AboutGalleryImageForm,
    fields=('image', 'order'),
    extra=2,
    can_delete=True,
    max_num=24,
    validate_max=True,
)


class GalleryPageSettingsForm(forms.ModelForm):
    class Meta:
        model = GalleryPageSettings
        fields = _all_model_fields(GalleryPageSettings, exclude=())
        widgets = {
            'hero_description': forms.Textarea(attrs={'rows': 3}),
            'hero_description_en': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style_form(self)


class GalleryPageImageForm(forms.ModelForm):
    class Meta:
        model = GalleryPageImage
        fields = ('image', 'caption', 'order')
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
            'caption': forms.TextInput(attrs={'placeholder': 'Légende optionnelle'}),
            'order': forms.NumberInput(attrs={'min': 0, 'step': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style_form(self)


GalleryPageImageFormSet = inlineformset_factory(
    GalleryPageSettings,
    GalleryPageImage,
    form=GalleryPageImageForm,
    fields=('image', 'caption', 'order'),
    extra=2,
    can_delete=True,
    max_num=50,
    validate_max=True,
)


GALLERY_SECTIONS = [
    ('En-tête de la page', [
        'hero_badge', 'hero_badge_en', 'hero_title', 'hero_title_en',
        'hero_description', 'hero_description_en',
    ]),
]


class ContactPageSettingsForm(forms.ModelForm):
    class Meta:
        model = ContactPageSettings
        fields = _all_model_fields(ContactPageSettings, exclude=())
        widgets = {
            'hero_description': forms.Textarea(attrs={'rows': 3}),
            'hero_description_en': forms.Textarea(attrs={'rows': 3}),
            'form_description': forms.Textarea(attrs={'rows': 2}),
            'form_description_en': forms.Textarea(attrs={'rows': 2}),
            'faq_description': forms.Textarea(attrs={'rows': 2}),
            'faq_description_en': forms.Textarea(attrs={'rows': 2}),
            'faq_a1': forms.Textarea(attrs={'rows': 3}),
            'faq_a1_en': forms.Textarea(attrs={'rows': 3}),
            'faq_a2': forms.Textarea(attrs={'rows': 3}),
            'faq_a2_en': forms.Textarea(attrs={'rows': 3}),
            'faq_a3': forms.Textarea(attrs={'rows': 3}),
            'faq_a3_en': forms.Textarea(attrs={'rows': 3}),
            'faq_a4': forms.Textarea(attrs={'rows': 3}),
            'faq_a4_en': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style_form(self)


ABOUT_SECTIONS = [
    ('Hero', [
        'hero_badge', 'hero_badge_en', 'hero_title_prefix', 'hero_title_prefix_en',
        'hero_title_suffix', 'hero_title_suffix_en', 'hero_description', 'hero_description_en',
    ]),
    ('Profil', [
        'profile_image', 'profile_years_number', 'profile_years_label', 'profile_years_label_en',
        'profile_title_prefix', 'profile_title_prefix_en', 'profile_title_suffix', 'profile_title_suffix_en',
        'profile_p1', 'profile_p1_en', 'profile_p2', 'profile_p2_en', 'profile_p3', 'profile_p3_en',
        'profile_stat_youth', 'profile_stat_youth_en', 'profile_stat_continents', 'profile_stat_continents_en',
    ]),
    ('Parcours (timeline)', [
        'journey_title', 'journey_title_en', 'journey_description', 'journey_description_en',
        'journey_item1_badge', 'journey_item1_badge_en', 'journey_item1_title', 'journey_item1_title_en',
        'journey_item1_desc', 'journey_item1_desc_en',
        'journey_item2_badge', 'journey_item2_badge_en', 'journey_item2_title', 'journey_item2_title_en',
        'journey_item2_desc', 'journey_item2_desc_en',
        'journey_item3_badge', 'journey_item3_badge_en', 'journey_item3_title', 'journey_item3_title_en',
        'journey_item3_desc', 'journey_item3_desc_en',
        'journey_item4_badge', 'journey_item4_badge_en', 'journey_item4_title', 'journey_item4_title_en',
        'journey_item4_desc', 'journey_item4_desc_en',
    ]),
    ('Vidéo', ['video_title', 'video_title_en', 'video_description', 'video_description_en', 'video_embed_url']),
    ('Valeurs', [
        'values_title', 'values_title_en', 'values_description', 'values_description_en',
        'values_excellence_title', 'values_excellence_title_en', 'values_excellence_desc', 'values_excellence_desc_en',
        'values_solidarity_title', 'values_solidarity_title_en', 'values_solidarity_desc', 'values_solidarity_desc_en',
        'values_authenticity_title', 'values_authenticity_title_en', 'values_authenticity_desc', 'values_authenticity_desc_en',
        'values_impact_title', 'values_impact_title_en', 'values_impact_desc', 'values_impact_desc_en',
    ]),
    ('Vision & CTA', [
        'vision_quote', 'vision_quote_en', 'vision_role', 'vision_role_en',
        'cta_title', 'cta_title_en', 'cta_description', 'cta_description_en',
        'cta_blog_btn', 'cta_blog_btn_en', 'cta_contact_btn', 'cta_contact_btn_en',
    ]),
]

CONTACT_SECTIONS = [
    ('Hero', [
        'hero_title_prefix', 'hero_title_prefix_en', 'hero_description', 'hero_description_en',
        'hero_response_time', 'hero_response_time_en',
    ]),
    ('Formulaire', ['form_title', 'form_title_en', 'form_description', 'form_description_en']),
    ('Encadrés latéraux', [
        'info_title', 'info_title_en', 'actions_title', 'actions_title_en',
        'actions_discover', 'actions_discover_en', 'actions_support', 'actions_support_en',
        'social_title', 'social_title_en',
    ]),
    ('FAQ', [
        'faq_title', 'faq_title_en', 'faq_description', 'faq_description_en',
        'faq_q1', 'faq_q1_en', 'faq_a1', 'faq_a1_en',
        'faq_q2', 'faq_q2_en', 'faq_a2', 'faq_a2_en',
        'faq_q3', 'faq_q3_en', 'faq_a3', 'faq_a3_en',
        'faq_q4', 'faq_q4_en', 'faq_a4', 'faq_a4_en',
    ]),
]


def build_form_sections(form, sections_spec):
    result = []
    for title, names in sections_spec:
        fields = [form[name] for name in names if name in form.fields]
        if fields:
            result.append((title, fields))
    return result
