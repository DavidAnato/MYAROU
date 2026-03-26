from django import forms
from blog.models import Article, Category
from django.forms import inlineformset_factory
from homepage.models import HomeSettings, HomeGalleryImage


class ArticleForm(forms.ModelForm):
    """Formulaire pour créer/modifier un article"""
    
    class Meta:
        model = Article
        fields = [
            'title', 'slug', 'author', 'category',
            'content', 'excerpt', 'image', 'video_file', 'video_url', 'tags', 'status',
            'meta_description', 'meta_keywords'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'placeholder': 'Titre de l\'article'
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
        fields = ['name', 'slug', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 transition-colors',
                'placeholder': 'Nom de la catégorie'
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
            'hero_badge', 'hero_title_prefix', 'hero_title_suffix', 'hero_description', 'hero_right_image',
            'hero_stats_youth_mentored', 'hero_stats_years_experience', 'hero_stats_continents',
            'quote_text', 'quote_subtext', 'quote_author_role', 'quote_cta', 'quote_image',
            'vision_badge', 'vision_title', 'vision_description',
            'values_leadership_title', 'values_leadership_desc',
            'values_excellence_title', 'values_excellence_desc',
            'values_impact_title', 'values_impact_desc',
            'barika_desc',
            'barika_education_title', 'barika_education_desc',
            'barika_sport_title', 'barika_sport_desc',
            'barika_entrepreneurship_title', 'barika_entrepreneurship_desc',
            'barika_cta',
            'join_badge', 'join_title_prefix', 'join_desc', 'join_cta',
            'articles_title_prefix', 'articles_title_suffix', 'articles_desc', 'articles_view_all', 'articles_read_more',
        ]
        widgets = {
            'hero_description': forms.Textarea(attrs={'rows': 3}),
            'quote_text': forms.Textarea(attrs={'rows': 3}),
            'vision_description': forms.Textarea(attrs={'rows': 3}),
            'values_leadership_desc': forms.Textarea(attrs={'rows': 3}),
            'values_excellence_desc': forms.Textarea(attrs={'rows': 3}),
            'values_impact_desc': forms.Textarea(attrs={'rows': 3}),
            'barika_desc': forms.Textarea(attrs={'rows': 3}),
            'barika_education_desc': forms.Textarea(attrs={'rows': 2}),
            'barika_sport_desc': forms.Textarea(attrs={'rows': 2}),
            'barika_entrepreneurship_desc': forms.Textarea(attrs={'rows': 2}),
            'join_desc': forms.Textarea(attrs={'rows': 3}),
            'articles_desc': forms.Textarea(attrs={'rows': 3}),
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


HomeGalleryImageFormSet = inlineformset_factory(
    HomeSettings,
    HomeGalleryImage,
    fields=('image', 'order'),
    extra=0,
    can_delete=True,
    max_num=4,
    validate_max=True,
    widgets={
        'image': forms.FileInput(attrs={'accept': 'image/*'}),
    },
)
