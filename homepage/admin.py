from django.contrib import admin
from .models import HomeSettings, HomeGalleryImage
from .models_site import (
    SiteSettings,
    SiteLink,
    AboutPageSettings,
    AboutGalleryImage,
    GalleryPageSettings,
    GalleryPageImage,
    ContactPageSettings,
    ContactMessage,
    SitePage,
    CustomPage,
    CustomPageBlock,
    CustomPageBlockImage,
)


class HomeGalleryImageInline(admin.TabularInline):
    model = HomeGalleryImage
    extra = 1
    fields = ('image', 'order')


@admin.register(HomeSettings)
class HomeSettingsAdmin(admin.ModelAdmin):
    change_form_template = 'admin/homepage/home_settings/change_form.html'
    inlines = [HomeGalleryImageInline]

    def has_add_permission(self, request):
        return not HomeSettings.objects.exists()


class GalleryPageImageInline(admin.TabularInline):
    model = GalleryPageImage
    extra = 2
    fields = ('image', 'caption', 'order')


@admin.register(GalleryPageSettings)
class GalleryPageSettingsAdmin(admin.ModelAdmin):
    inlines = [GalleryPageImageInline]

    def has_add_permission(self, request):
        return not GalleryPageSettings.objects.exists()


class AboutGalleryImageInline(admin.TabularInline):
    model = AboutGalleryImage
    extra = 2
    fields = ('image', 'order')


@admin.register(AboutPageSettings)
class AboutPageSettingsAdmin(admin.ModelAdmin):
    inlines = [AboutGalleryImageInline]

    def has_add_permission(self, request):
        return not AboutPageSettings.objects.exists()


@admin.register(ContactPageSettings)
class ContactPageSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not ContactPageSettings.objects.exists()


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(SiteLink)
class SiteLinkAdmin(admin.ModelAdmin):
    list_display = ('label', 'platform', 'category', 'url', 'order', 'is_active')
    list_filter = ('category', 'platform', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'request_type', 'is_read', 'created_at')
    list_filter = ('request_type', 'is_read', 'created_at')
    list_editable = ('is_read',)
    readonly_fields = ('name', 'email', 'request_type', 'subject', 'message', 'created_at', 'email_sent')
    search_fields = ('name', 'email', 'subject', 'message')

    def has_add_permission(self, request):
        return False


@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    list_display = ('label', 'route_name', 'is_visible', 'show_in_nav', 'order')
    list_editable = ('is_visible', 'show_in_nav', 'order')
    ordering = ('order', 'id')


@admin.register(CustomPage)
class CustomPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'show_in_nav', 'order', 'updated_at')
    list_filter = ('is_published', 'show_in_nav')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class CustomPageBlockImageInline(admin.TabularInline):
    model = CustomPageBlockImage
    extra = 0
    fields = ('image', 'caption', 'caption_en', 'order')


@admin.register(CustomPageBlock)
class CustomPageBlockAdmin(admin.ModelAdmin):
    list_display = ('block_type', 'page', 'order', 'is_visible')
    list_filter = ('block_type', 'is_visible')
    inlines = [CustomPageBlockImageInline]
