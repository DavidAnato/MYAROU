from django import forms
from blog.models import Article, Category
from django.forms import inlineformset_factory
from homepage.models import HomeSettings, HomeGalleryImage


class CategorySelectWithEn(forms.Select):
    """Select catégorie avec data-name-en pour l'aperçu live."""

    @staticmethod
    def _choice_pk(value):
        if value in (None, ''):
            return None
        if hasattr(value, 'value'):
            return value.value
        return value

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        pk = self._choice_pk(value)
        if pk is not None:
            try:
                cat = Category.objects.get(pk=pk)
                option.setdefault('attrs', {})
                option['attrs']['data-name-en'] = cat.get_name('en')
            except (Category.DoesNotExist, TypeError, ValueError):
                pass
        return option


class ArticleForm(forms.ModelForm):
    """Formulaire pour créer/modifier un article"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category_field = self.fields['category']
        category_field.widget = CategorySelectWithEn(attrs=category_field.widget.attrs)
    
    class Meta:
        model = Article
        fields = [
            'title', 'title_en', 'slug', 'author', 'category',
            'content', 'content_en', 'excerpt', 'excerpt_en',
            'image', 'video_file', 'video_url', 'tags', 'status',
            'meta_description', 'meta_description_en', 'meta_keywords',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'placeholder': 'Titre de l\'article'
            }),
            'title_en': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'placeholder': 'Article title (EN)'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'placeholder': 'slug-automatique'
            }),
            'author': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'placeholder': 'Nom de l\'auteur'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'rows': 3,
                'placeholder': 'Court extrait...'
            }),
            'excerpt_en': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'rows': 3,
                'placeholder': 'Short excerpt (EN)...'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'placeholder': 'tag1, tag2, tag3'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white transition-colors'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white transition-colors'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white transition-colors',
                'accept': 'image/*'
            }),
            'video_file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white transition-colors',
                'accept': 'video/*'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'placeholder': 'https://www.youtube.com/watch?v=...'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'rows': 2,
                'placeholder': 'Description SEO (max 160 caractères)'
            }),
            'meta_description_en': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'rows': 2,
                'placeholder': 'SEO description (EN, max 160 chars)'
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'placeholder': 'mot-clé1, mot-clé2'
            }),
        }


from django import forms
from blog.models import Category


class CategoryForm(forms.ModelForm):
    """Formulaire pour créer/modifier une catégorie"""
    
    class Meta:
        model = Category
        fields = ['name', 'name_en', 'slug', 'description', 'description_en', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'placeholder': 'Nom de la catégorie'
            }),
            'name_en': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'placeholder': 'Category name (EN)'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'placeholder': 'slug-automatique'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'placeholder': 'Description de la catégorie...',
                'rows': 4
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white transition-colors',
                'accept': 'image/*'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre le slug optionnel (il sera généré automatiquement)
        self.fields['slug'].required = False


class HomeSettingsForm(forms.ModelForm):
    class Meta:
        model = HomeSettings
        fields = [
            'hero_badge', 'hero_badge_en',
            'hero_title_prefix', 'hero_title_prefix_en',
            'hero_title_suffix', 'hero_title_suffix_en',
            'hero_description', 'hero_description_en',
            'hero_right_image',
            'hero_stats_youth_mentored', 'hero_stats_years_experience', 'hero_stats_continents',
            'quote_text', 'quote_text_en',
            'quote_subtext', 'quote_subtext_en',
            'quote_author_role', 'quote_author_role_en',
            'quote_cta', 'quote_cta_en',
            'quote_image',
            'vision_badge', 'vision_badge_en',
            'vision_title', 'vision_title_en',
            'vision_description', 'vision_description_en',
            'values_leadership_title', 'values_leadership_title_en',
            'values_leadership_desc', 'values_leadership_desc_en',
            'values_excellence_title', 'values_excellence_title_en',
            'values_excellence_desc', 'values_excellence_desc_en',
            'values_impact_title', 'values_impact_title_en',
            'values_impact_desc', 'values_impact_desc_en',
            'barika_desc', 'barika_desc_en',
            'barika_education_title', 'barika_education_title_en',
            'barika_education_desc', 'barika_education_desc_en',
            'barika_sport_title', 'barika_sport_title_en',
            'barika_sport_desc', 'barika_sport_desc_en',
            'barika_entrepreneurship_title', 'barika_entrepreneurship_title_en',
            'barika_entrepreneurship_desc', 'barika_entrepreneurship_desc_en',
            'barika_cta', 'barika_cta_en',
            'join_badge', 'join_badge_en',
            'join_title_prefix', 'join_title_prefix_en',
            'join_desc', 'join_desc_en',
            'join_cta', 'join_cta_en',
            'articles_title_prefix', 'articles_title_prefix_en',
            'articles_title_suffix', 'articles_title_suffix_en',
            'articles_desc', 'articles_desc_en',
            'articles_view_all', 'articles_view_all_en',
            'articles_read_more', 'articles_read_more_en',
        ]
        widgets = {
            'hero_description': forms.Textarea(attrs={'rows': 3}),
            'hero_description_en': forms.Textarea(attrs={'rows': 3}),
            'quote_text': forms.Textarea(attrs={'rows': 3}),
            'quote_text_en': forms.Textarea(attrs={'rows': 3}),
            'vision_description': forms.Textarea(attrs={'rows': 3}),
            'vision_description_en': forms.Textarea(attrs={'rows': 3}),
            'values_leadership_desc': forms.Textarea(attrs={'rows': 3}),
            'values_leadership_desc_en': forms.Textarea(attrs={'rows': 3}),
            'values_excellence_desc': forms.Textarea(attrs={'rows': 3}),
            'values_excellence_desc_en': forms.Textarea(attrs={'rows': 3}),
            'values_impact_desc': forms.Textarea(attrs={'rows': 3}),
            'values_impact_desc_en': forms.Textarea(attrs={'rows': 3}),
            'barika_desc': forms.Textarea(attrs={'rows': 3}),
            'barika_desc_en': forms.Textarea(attrs={'rows': 3}),
            'barika_education_desc': forms.Textarea(attrs={'rows': 2}),
            'barika_education_desc_en': forms.Textarea(attrs={'rows': 2}),
            'barika_sport_desc': forms.Textarea(attrs={'rows': 2}),
            'barika_sport_desc_en': forms.Textarea(attrs={'rows': 2}),
            'barika_entrepreneurship_desc': forms.Textarea(attrs={'rows': 2}),
            'barika_entrepreneurship_desc_en': forms.Textarea(attrs={'rows': 2}),
            'join_desc': forms.Textarea(attrs={'rows': 3}),
            'join_desc_en': forms.Textarea(attrs={'rows': 3}),
            'articles_desc': forms.Textarea(attrs={'rows': 3}),
            'articles_desc_en': forms.Textarea(attrs={'rows': 3}),
            'hero_right_image': forms.FileInput(attrs={'accept': 'image/*'}),
            'quote_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_classes = 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors'
        for name, field in self.fields.items():
            widget = field.widget
            existing = widget.attrs.get('class', '')
            widget.attrs['class'] = (existing + ' ' + base_classes).strip()


class HomeGalleryImageForm(forms.ModelForm):
    class Meta:
        model = HomeGalleryImage
        fields = ('image', 'order')
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
            'order': forms.NumberInput(attrs={'min': 0, 'step': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_classes = (
            'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 '
            'focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white '
            'dark:placeholder-gray-400 transition-colors'
        )
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                continue
            if isinstance(widget, forms.FileInput):
                widget.attrs.setdefault('accept', 'image/*')
            existing = widget.attrs.get('class', '')
            widget.attrs['class'] = (existing + ' ' + base_classes).strip()


HomeGalleryImageFormSet = inlineformset_factory(
    HomeSettings,
    HomeGalleryImage,
    form=HomeGalleryImageForm,
    fields=('image', 'order'),
    extra=0,
    can_delete=True,
    max_num=4,
    validate_max=True,
)
