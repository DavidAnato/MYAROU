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
    list_display = ('name', 'email', 'subject', 'request_type', 'created_at', 'email_sent')
    list_filter = ('request_type', 'email_sent', 'created_at')
    readonly_fields = ('name', 'email', 'request_type', 'subject', 'message', 'created_at', 'email_sent')
    search_fields = ('name', 'email', 'subject', 'message')

    def has_add_permission(self, request):
        return False
