from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_thumbnail', 'get_article_count']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_preview']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('name', 'slug', 'description', 'image', 'image_preview')
        }),
    )
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "Pas d'image"
    image_thumbnail.short_description = "Image"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="300" />', obj.image.url)
        return "Aucune image uploadée"
    image_preview.short_description = "Aperçu"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views', 'published_at', 'image_thumbnail']
    list_filter = ['status', 'category', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'tags', 'meta_description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    readonly_fields = ['created_at', 'updated_at', 'views', 'image_preview']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'slug', 'author', 'category', 'status')
        }),
        ('Contenu', {
            'fields': ('excerpt', 'content', 'image', 'image_preview')
        }),
        ('Métadonnées', {
            'fields': ('tags', 'views'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('published_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['publish_articles', 'unpublish_articles']
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="50" style="object-fit: cover;" />', obj.image.url)
        return "Pas d'image"
    image_thumbnail.short_description = "Image"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="400" />', obj.image.url)
        return "Aucune image uploadée"
    image_preview.short_description = "Aperçu"
    
    def publish_articles(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, f'{updated} article(s) ont été publiés.')
    publish_articles.short_description = "Publier les articles sélectionnés"
    
    def unpublish_articles(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} article(s) ont été mis en brouillon.')
    unpublish_articles.short_description = "Mettre en brouillon"
