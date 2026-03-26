from django.contrib import admin
from .models import HomeSettings, HomeGalleryImage


class HomeGalleryImageInline(admin.TabularInline):
     model = HomeGalleryImage
     extra = 1
     fields = ('image', 'order')


@admin.register(HomeSettings)
class HomeSettingsAdmin(admin.ModelAdmin):
     change_form_template = 'admin/homepage/home_settings/change_form.html'
     inlines = [HomeGalleryImageInline]
     list_display = ('__str__', 'hero_title_prefix', 'vision_title')
     fieldsets = (
         ('Hero', {
             'fields': (
                 'hero_badge', 'hero_title_prefix', 'hero_title_suffix',
                 'hero_description', 'hero_right_image',
                 'hero_stats_youth_mentored', 'hero_stats_years_experience', 'hero_stats_continents'
             )
         }),
         ('Citation', {
             'fields': ('quote_text', 'quote_subtext', 'quote_author_role', 'quote_cta', 'quote_image')
         }),
         ('Vision', {
             'fields': ('vision_badge', 'vision_title', 'vision_description')
         }),
         ('Valeurs', {
             'fields': (
                 'values_leadership_title', 'values_leadership_desc',
                 'values_excellence_title', 'values_excellence_desc',
                 'values_impact_title', 'values_impact_desc'
             )
         }),
         ('Section BARIKA', {
             'fields': (
                 'barika_desc',
                 'barika_education_title', 'barika_education_desc',
                 'barika_sport_title', 'barika_sport_desc',
                 'barika_entrepreneurship_title', 'barika_entrepreneurship_desc',
                 'barika_cta',
             )
         }),
         ('Rejoindre', {
             'fields': ('join_badge', 'join_title_prefix', 'join_desc', 'join_cta')
         }),
         ('Articles', {
             'fields': ('articles_title_prefix', 'articles_title_suffix', 'articles_desc', 'articles_view_all', 'articles_read_more')
         }),
     )
 
     def has_add_permission(self, request):
         return not HomeSettings.objects.exists()
