import json

from django import forms
from django.forms import inlineformset_factory, modelformset_factory

from homepage.models_site import CustomPage, CustomPageBlock, CustomPageBlockImage
from homepage.page_blocks import (
    BLOCK_FIELDS,
    BLOCK_TYPE_CHOICES,
    get_layout_choices,
    normalize_layout,
)
from dashboard.site_forms import WIDGET_CLASS, _style_form


class CustomPageMetaForm(forms.ModelForm):
    """Métadonnées page (sans contenu — géré par blocs)."""

    class Meta:
        model = CustomPage
        fields = [
            'title', 'title_en', 'slug',
            'is_published', 'show_in_nav', 'order',
            'meta_description', 'meta_description_en',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre de la page'}),
            'title_en': forms.TextInput(attrs={'placeholder': 'Page title (EN)'}),
            'slug': forms.TextInput(attrs={'placeholder': 'mentions-legales'}),
            'meta_description': forms.Textarea(attrs={'rows': 2}),
            'meta_description_en': forms.Textarea(attrs={'rows': 2}),
            'order': forms.NumberInput(attrs={'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style_form(self)
        self.fields['slug'].required = False

    def clean_slug(self):
        from homepage.models_site import RESERVED_CUSTOM_PAGE_SLUGS
        slug = self.cleaned_data.get('slug', '').strip()
        title = self.cleaned_data.get('title', '')
        if not slug and title:
            from django.utils.text import slugify
            slug = slugify(title)
        if slug in RESERVED_CUSTOM_PAGE_SLUGS:
            raise forms.ValidationError('Ce slug est réservé par le site.')
        qs = CustomPage.objects.filter(slug=slug)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Une page avec ce slug existe déjà.')
        return slug


class CustomPageBlockForm(forms.ModelForm):
    faq_json = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label='FAQ (JSON)',
    )

    class Meta:
        model = CustomPageBlock
        fields = [
            'block_type', 'order', 'is_visible',
            'badge', 'badge_en', 'title', 'title_en',
            'subtitle', 'subtitle_en', 'content', 'content_en',
            'image', 'image_alt', 'video_url',
            'button_text', 'button_text_en', 'button_url',
            'layout',
        ]
        widgets = {
            'block_type': forms.Select(attrs={
                'class': WIDGET_CLASS + ' builder-type-select',
                'data-block-type-select': '1',
                'x-on:change': 'blockType = $event.target.value',
            }),
            'order': forms.NumberInput(attrs={'min': 0, 'class': 'builder-order-hidden'}),
            'layout': forms.Select(choices=[]),
            'content': forms.Textarea(attrs={'rows': 4}),
            'content_en': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style_form(self)
        self.fields['order'].widget.attrs['class'] = 'builder-order-hidden'
        self.fields['block_type'].widget.attrs['class'] = (
            WIDGET_CLASS + ' builder-type-select'
        )
        block_type = getattr(self.instance, 'block_type', None) or self.initial.get('block_type', '')
        if not block_type and self.data and self.prefix:
            block_type = self.data.get(f'{self.prefix}-block_type', '')
        layout_choices = get_layout_choices(block_type or '')
        self.fields['layout'].widget.choices = layout_choices or [('', '—')]
        if self.instance.pk and self.instance.block_type == 'faq':
            items = (self.instance.config or {}).get('items') or []
            self.fields['faq_json'].initial = json.dumps(items, ensure_ascii=False)

    def clean(self):
        cleaned = super().clean()
        block_type = cleaned.get('block_type') or getattr(self.instance, 'block_type', '')
        cleaned['layout'] = normalize_layout(block_type, cleaned.get('layout', ''))
        if block_type == 'faq':
            raw = cleaned.get('faq_json') or '[]'
            try:
                items = json.loads(raw) if raw else []
            except json.JSONDecodeError as exc:
                raise forms.ValidationError({'faq_json': 'Format FAQ invalide.'}) from exc
            if not isinstance(items, list):
                raise forms.ValidationError({'faq_json': 'La FAQ doit être une liste.'})
            cleaned['config'] = {'items': items}
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.block_type == 'faq':
            instance.config = self.cleaned_data.get('config') or {'items': []}
        if commit:
            instance.save()
        return instance


class CustomPageBlockImageForm(forms.ModelForm):
    class Meta:
        model = CustomPageBlockImage
        fields = ['block', 'image', 'caption', 'caption_en', 'order']
        widgets = {
            'block': forms.HiddenInput(),
            'order': forms.NumberInput(attrs={'min': 0, 'class': 'builder-order-hidden'}),
            'caption': forms.TextInput(attrs={'placeholder': 'Légende'}),
            'caption_en': forms.TextInput(attrs={'placeholder': 'Caption (EN)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style_form(self)
        self.fields['image'].required = False
        self.fields['order'].widget.attrs['class'] = 'builder-order-hidden'

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('DELETE'):
            return cleaned
        image = cleaned.get('image')
        if self.instance.pk and self.instance.image and not image:
            cleaned['image'] = self.instance.image
            return cleaned
        if not image and not (self.instance.pk and self.instance.image):
            cleaned['_empty'] = True
        return cleaned


class BaseCustomPageBlockImageFormSet(forms.BaseModelFormSet):
    """Ignore les lignes galerie ajoutées sans fichier (builder)."""

    def save(self, commit=True):
        if not self.is_valid():
            raise ValueError('The formset is not valid')
        saved = []
        for form in self.forms:
            if not form.cleaned_data:
                continue
            if form.cleaned_data.get('DELETE'):
                if form.instance.pk and commit:
                    form.instance.delete()
                continue
            if form.cleaned_data.get('_empty'):
                continue
            saved.append(form.save(commit=commit))
        return saved


CustomPageBlockFormSet = inlineformset_factory(
    CustomPage,
    CustomPageBlock,
    form=CustomPageBlockForm,
    extra=0,
    can_delete=True,
)

CustomPageBlockImageFormSet = modelformset_factory(
    CustomPageBlockImage,
    form=CustomPageBlockImageForm,
    formset=BaseCustomPageBlockImageFormSet,
    extra=0,
    can_delete=True,
)


def fields_for_block_type(block_type):
    return BLOCK_FIELDS.get(block_type, [])
