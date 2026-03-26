from django.db import models
from django.conf import settings
import json


class HomeSettings(models.Model):
    """Paramètres dynamiques de la page d'accueil (singleton)"""
    hero_badge = models.CharField(max_length=100, blank=True)
    hero_badge_en = models.CharField(max_length=100, blank=True)
    hero_title_prefix = models.CharField(max_length=200, blank=True)
    hero_title_prefix_en = models.CharField(max_length=200, blank=True)
    hero_title_suffix = models.CharField(max_length=200, blank=True)
    hero_title_suffix_en = models.CharField(max_length=200, blank=True)
    hero_description = models.TextField(blank=True)
    hero_description_en = models.TextField(blank=True)
    hero_right_image = models.ImageField(upload_to='home/hero/', blank=True, null=True)
    hero_stats_youth_mentored = models.PositiveIntegerField(blank=True, null=True)
    hero_stats_years_experience = models.PositiveIntegerField(blank=True, null=True)
    hero_stats_continents = models.PositiveIntegerField(blank=True, null=True)
    
    quote_text = models.TextField(blank=True)
    quote_text_en = models.TextField(blank=True)
    quote_subtext = models.CharField(max_length=255, blank=True)
    quote_subtext_en = models.CharField(max_length=255, blank=True)
    quote_author_role = models.CharField(max_length=255, blank=True)
    quote_author_role_en = models.CharField(max_length=255, blank=True)
    quote_cta = models.CharField(max_length=100, blank=True)
    quote_cta_en = models.CharField(max_length=100, blank=True)
    quote_image = models.ImageField(upload_to='home/quote/', blank=True, null=True)
    
    vision_badge = models.CharField(max_length=100, blank=True)
    vision_badge_en = models.CharField(max_length=100, blank=True)
    vision_title = models.CharField(max_length=255, blank=True)
    vision_title_en = models.CharField(max_length=255, blank=True)
    vision_description = models.TextField(blank=True)
    vision_description_en = models.TextField(blank=True)
    
    values_leadership_title = models.CharField(max_length=200, blank=True)
    values_leadership_title_en = models.CharField(max_length=200, blank=True)
    values_leadership_desc = models.TextField(blank=True)
    values_leadership_desc_en = models.TextField(blank=True)
    values_excellence_title = models.CharField(max_length=200, blank=True)
    values_excellence_title_en = models.CharField(max_length=200, blank=True)
    values_excellence_desc = models.TextField(blank=True)
    values_excellence_desc_en = models.TextField(blank=True)
    values_impact_title = models.CharField(max_length=200, blank=True)
    values_impact_title_en = models.CharField(max_length=200, blank=True)
    values_impact_desc = models.TextField(blank=True)
    values_impact_desc_en = models.TextField(blank=True)
    
    barika_desc = models.TextField(blank=True)
    barika_desc_en = models.TextField(blank=True)
    barika_education_title = models.CharField(max_length=200, blank=True)
    barika_education_title_en = models.CharField(max_length=200, blank=True)
    barika_education_desc = models.TextField(blank=True)
    barika_education_desc_en = models.TextField(blank=True)
    barika_sport_title = models.CharField(max_length=200, blank=True)
    barika_sport_title_en = models.CharField(max_length=200, blank=True)
    barika_sport_desc = models.TextField(blank=True)
    barika_sport_desc_en = models.TextField(blank=True)
    barika_entrepreneurship_title = models.CharField(max_length=200, blank=True)
    barika_entrepreneurship_title_en = models.CharField(max_length=200, blank=True)
    barika_entrepreneurship_desc = models.TextField(blank=True)
    barika_entrepreneurship_desc_en = models.TextField(blank=True)
    barika_cta = models.CharField(max_length=100, blank=True)
    barika_cta_en = models.CharField(max_length=100, blank=True)
    
    join_badge = models.CharField(max_length=100, blank=True)
    join_badge_en = models.CharField(max_length=100, blank=True)
    join_title_prefix = models.CharField(max_length=255, blank=True)
    join_title_prefix_en = models.CharField(max_length=255, blank=True)
    join_desc = models.TextField(blank=True)
    join_desc_en = models.TextField(blank=True)
    join_cta = models.CharField(max_length=100, blank=True)
    join_cta_en = models.CharField(max_length=100, blank=True)
    
    articles_title_prefix = models.CharField(max_length=255, blank=True)
    articles_title_prefix_en = models.CharField(max_length=255, blank=True)
    articles_title_suffix = models.CharField(max_length=255, blank=True)
    articles_title_suffix_en = models.CharField(max_length=255, blank=True)
    articles_desc = models.TextField(blank=True)
    articles_desc_en = models.TextField(blank=True)
    articles_view_all = models.CharField(max_length=100, blank=True)
    articles_view_all_en = models.CharField(max_length=100, blank=True)
    articles_read_more = models.CharField(max_length=100, blank=True)
    articles_read_more_en = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = "Paramètres d'accueil"
        verbose_name_plural = "Paramètres d'accueil"
    
    def __str__(self):
        return "Paramètres de la page d'accueil"
    
    @classmethod
    def get_solo(cls, language_code='fr'):
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create()
        obj.apply_static_defaults_if_missing(language_code=language_code)
        return obj
    
    @classmethod
    def load_static_defaults(cls, language_code='fr'):
        lang = (language_code or 'fr').split('-')[0].lower()
        if lang not in ('fr', 'en'):
            lang = 'fr'
        path = settings.BASE_DIR / 'i18n' / f'{lang}.json'
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
        except Exception:
            data = {}
        
        mapping = {
            'hero_badge': 'site.home.hero.badge',
            'hero_title_prefix': 'site.home.hero.title_prefix',
            'hero_title_suffix': 'site.home.hero.title_suffix',
            'hero_description': 'site.home.hero.description',
            'quote_text': 'site.home.quote.text',
            'quote_subtext': 'site.home.quote.subtext',
            'quote_author_role': 'site.home.quote.author_role',
            'quote_cta': 'site.home.quote.cta',
            'vision_badge': 'site.home.vision.badge',
            'vision_title': 'site.home.vision.title',
            'vision_description': 'site.home.vision.description',
            'values_leadership_title': 'site.home.values.leadership.title',
            'values_leadership_desc': 'site.home.values.leadership.desc',
            'values_excellence_title': 'site.home.values.excellence.title',
            'values_excellence_desc': 'site.home.values.excellence.desc',
            'values_impact_title': 'site.home.values.impact.title',
            'values_impact_desc': 'site.home.values.impact.desc',
            'barika_desc': 'site.home.barika.desc',
            'barika_education_title': 'site.home.barika.education.title',
            'barika_education_desc': 'site.home.barika.education.desc',
            'barika_sport_title': 'site.home.barika.sport.title',
            'barika_sport_desc': 'site.home.barika.sport.desc',
            'barika_entrepreneurship_title': 'site.home.barika.entrepreneurship.title',
            'barika_entrepreneurship_desc': 'site.home.barika.entrepreneurship.desc',
            'barika_cta': 'site.home.barika.cta',
            'join_badge': 'site.home.join.badge',
            'join_title_prefix': 'site.home.join.title_prefix',
            'join_desc': 'site.home.join.desc',
            'join_cta': 'site.home.join.cta',
            'articles_title_prefix': 'site.home.articles.title_prefix',
            'articles_title_suffix': 'site.home.articles.title_suffix',
            'articles_desc': 'site.home.articles.desc',
            'articles_view_all': 'site.home.articles.view_all',
            'articles_read_more': 'site.home.articles.read_more',
        }
        defaults = {field: data.get(key, '') for field, key in mapping.items()}
        defaults['hero_stats_youth_mentored'] = 500
        defaults['hero_stats_years_experience'] = 15
        defaults['hero_stats_continents'] = 3
        return defaults
    
    def apply_static_defaults_if_missing(self, language_code='fr'):
        fr_defaults = self.load_static_defaults(language_code='fr')
        en_defaults = self.load_static_defaults(language_code='en')

        defaults = dict(fr_defaults)
        for key, value in en_defaults.items():
            if key.startswith('hero_stats_'):
                defaults[key] = value
            else:
                defaults[f'{key}_en'] = value

        changed_fields = []
        for field_name, default_value in defaults.items():
            current = getattr(self, field_name)
            if current is None or current == '':
                setattr(self, field_name, default_value)
                changed_fields.append(field_name)
        if changed_fields:
            self.save(update_fields=changed_fields)


class HomeGalleryImage(models.Model):
    """Images de galerie pour la section Accueil"""
    home = models.ForeignKey(HomeSettings, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='home/gallery/')
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Image de galerie"
        verbose_name_plural = "Images de galerie"
    
    def __str__(self):
        return f"Image #{self.pk} (ordre {self.order})"
