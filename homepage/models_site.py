from django.db import models
from django.conf import settings

from .i18n_defaults import apply_i18n_defaults, merge_fr_en_defaults


class SiteSettings(models.Model):
    """Paramètres globaux du site (singleton)."""
    contact_email = models.EmailField(blank=True, default='contact@myarou.com')
    contact_location = models.CharField(max_length=255, blank=True, default='Paris, France')
    contact_notify_email = models.EmailField(
        blank=True,
        help_text="Destinataire des messages du formulaire de contact (vide = email de contact public).",
    )
    footer_bio = models.TextField(blank=True)
    footer_bio_en = models.TextField(blank=True)

    class Meta:
        verbose_name = "Paramètres du site"
        verbose_name_plural = "Paramètres du site"

    def __str__(self):
        return "Paramètres du site"

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create()
        obj.apply_defaults_if_missing()
        return obj

    def apply_defaults_if_missing(self):
        mapping = {
            'footer_bio': 'site.footer.bio',
        }
        mapping = merge_fr_en_defaults(mapping)
        changed = apply_i18n_defaults(self, mapping)
        if changed:
            self.save(update_fields=changed)

    @property
    def notify_email(self):
        return self.contact_notify_email or self.contact_email


class SiteLink(models.Model):
    CATEGORY_SOCIAL = 'social'
    CATEGORY_FOOTER = 'footer'
    CATEGORY_USEFUL = 'useful'
    CATEGORY_CHOICES = [
        (CATEGORY_SOCIAL, 'Réseaux sociaux'),
        (CATEGORY_FOOTER, 'Liens footer'),
        (CATEGORY_USEFUL, 'Liens utiles'),
    ]

    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter / X'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('website', 'Site web'),
        ('email', 'Email'),
        ('other', 'Autre'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_SOCIAL)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='other')
    label = models.CharField(max_length=120, blank=True)
    url = models.URLField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    open_in_new_tab = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'order', 'id']
        verbose_name = "Lien du site"
        verbose_name_plural = "Liens du site"

    def __str__(self):
        return self.label or self.get_platform_display() or self.url


ABOUT_I18N_MAP = merge_fr_en_defaults({
    'hero_badge': 'site.about.hero.badge',
    'hero_title_prefix': 'site.about.hero.title_prefix',
    'hero_title_suffix': 'site.about.hero.title_suffix',
    'hero_description': 'site.about.hero.description',
    'profile_years_label': 'site.about.profile.years_experience',
    'profile_title_prefix': 'site.about.profile.title_prefix',
    'profile_title_suffix': 'site.about.profile.title_suffix',
    'profile_p1': 'site.about.profile.p1',
    'profile_p2': 'site.about.profile.p2',
    'profile_p3': 'site.about.profile.p3',
    'profile_stat_youth': 'site.about.profile.stats.youth',
    'profile_stat_continents': 'site.about.profile.stats.continents',
    'journey_title': 'site.about.journey.title',
    'journey_description': 'site.about.journey.description',
    'journey_item1_badge': 'site.about.journey.item1.badge',
    'journey_item1_title': 'site.about.journey.item1.title',
    'journey_item1_desc': 'site.about.journey.item1.desc',
    'journey_item2_badge': 'site.about.journey.item2.badge',
    'journey_item2_title': 'site.about.journey.item2.title',
    'journey_item2_desc': 'site.about.journey.item2.desc',
    'journey_item3_badge': 'site.about.journey.item3.badge',
    'journey_item3_title': 'site.about.journey.item3.title',
    'journey_item3_desc': 'site.about.journey.item3.desc',
    'journey_item4_badge': 'site.about.journey.item4.badge',
    'journey_item4_title': 'site.about.journey.item4.title',
    'journey_item4_desc': 'site.about.journey.item4.desc',
    'video_title': 'site.about.video.title',
    'video_description': 'site.about.video.description',
    'values_title': 'site.about.values.title',
    'values_description': 'site.about.values.description',
    'values_excellence_title': 'site.about.values.excellence.title',
    'values_excellence_desc': 'site.about.values.excellence.desc',
    'values_solidarity_title': 'site.about.values.solidarity.title',
    'values_solidarity_desc': 'site.about.values.solidarity.desc',
    'values_authenticity_title': 'site.about.values.authenticity.title',
    'values_authenticity_desc': 'site.about.values.authenticity.desc',
    'values_impact_title': 'site.about.values.impact.title',
    'values_impact_desc': 'site.about.values.impact.desc',
    'vision_quote': 'site.about.vision.quote',
    'vision_role': 'site.about.vision.role',
    'cta_title': 'site.about.cta.title',
    'cta_description': 'site.about.cta.description',
    'cta_blog_btn': 'site.about.cta.blog_btn',
    'cta_contact_btn': 'site.about.cta.contact_btn',
})


class AboutPageSettings(models.Model):
    """Contenu éditable de la page À propos (singleton)."""

    hero_badge = models.CharField(max_length=100, blank=True)
    hero_badge_en = models.CharField(max_length=100, blank=True)
    hero_title_prefix = models.CharField(max_length=200, blank=True)
    hero_title_prefix_en = models.CharField(max_length=200, blank=True)
    hero_title_suffix = models.CharField(max_length=200, blank=True)
    hero_title_suffix_en = models.CharField(max_length=200, blank=True)
    hero_description = models.TextField(blank=True)
    hero_description_en = models.TextField(blank=True)

    profile_image = models.ImageField(upload_to='about/profile/', blank=True, null=True)
    profile_years_number = models.PositiveIntegerField(blank=True, null=True, default=15)
    profile_years_label = models.CharField(max_length=100, blank=True)
    profile_years_label_en = models.CharField(max_length=100, blank=True)
    profile_title_prefix = models.CharField(max_length=200, blank=True)
    profile_title_prefix_en = models.CharField(max_length=200, blank=True)
    profile_title_suffix = models.CharField(max_length=200, blank=True)
    profile_title_suffix_en = models.CharField(max_length=200, blank=True)
    profile_p1 = models.TextField(blank=True)
    profile_p1_en = models.TextField(blank=True)
    profile_p2 = models.TextField(blank=True)
    profile_p2_en = models.TextField(blank=True)
    profile_p3 = models.TextField(blank=True)
    profile_p3_en = models.TextField(blank=True)
    profile_stat_youth = models.CharField(max_length=120, blank=True)
    profile_stat_youth_en = models.CharField(max_length=120, blank=True)
    profile_stat_continents = models.CharField(max_length=120, blank=True)
    profile_stat_continents_en = models.CharField(max_length=120, blank=True)

    journey_title = models.CharField(max_length=255, blank=True)
    journey_title_en = models.CharField(max_length=255, blank=True)
    journey_description = models.TextField(blank=True)
    journey_description_en = models.TextField(blank=True)
    journey_item1_badge = models.CharField(max_length=120, blank=True)
    journey_item1_badge_en = models.CharField(max_length=120, blank=True)
    journey_item1_title = models.CharField(max_length=200, blank=True)
    journey_item1_title_en = models.CharField(max_length=200, blank=True)
    journey_item1_desc = models.TextField(blank=True)
    journey_item1_desc_en = models.TextField(blank=True)
    journey_item2_badge = models.CharField(max_length=120, blank=True)
    journey_item2_badge_en = models.CharField(max_length=120, blank=True)
    journey_item2_title = models.CharField(max_length=200, blank=True)
    journey_item2_title_en = models.CharField(max_length=200, blank=True)
    journey_item2_desc = models.TextField(blank=True)
    journey_item2_desc_en = models.TextField(blank=True)
    journey_item3_badge = models.CharField(max_length=120, blank=True)
    journey_item3_badge_en = models.CharField(max_length=120, blank=True)
    journey_item3_title = models.CharField(max_length=200, blank=True)
    journey_item3_title_en = models.CharField(max_length=200, blank=True)
    journey_item3_desc = models.TextField(blank=True)
    journey_item3_desc_en = models.TextField(blank=True)
    journey_item4_badge = models.CharField(max_length=120, blank=True)
    journey_item4_badge_en = models.CharField(max_length=120, blank=True)
    journey_item4_title = models.CharField(max_length=200, blank=True)
    journey_item4_title_en = models.CharField(max_length=200, blank=True)
    journey_item4_desc = models.TextField(blank=True)
    journey_item4_desc_en = models.TextField(blank=True)

    video_title = models.CharField(max_length=255, blank=True)
    video_title_en = models.CharField(max_length=255, blank=True)
    video_description = models.TextField(blank=True)
    video_description_en = models.TextField(blank=True)
    video_embed_url = models.URLField(
        max_length=500,
        blank=True,
        default='https://www.youtube.com/embed/MlCA-DC9WP8',
    )

    values_title = models.CharField(max_length=255, blank=True)
    values_title_en = models.CharField(max_length=255, blank=True)
    values_description = models.TextField(blank=True)
    values_description_en = models.TextField(blank=True)
    values_excellence_title = models.CharField(max_length=200, blank=True)
    values_excellence_title_en = models.CharField(max_length=200, blank=True)
    values_excellence_desc = models.TextField(blank=True)
    values_excellence_desc_en = models.TextField(blank=True)
    values_solidarity_title = models.CharField(max_length=200, blank=True)
    values_solidarity_title_en = models.CharField(max_length=200, blank=True)
    values_solidarity_desc = models.TextField(blank=True)
    values_solidarity_desc_en = models.TextField(blank=True)
    values_authenticity_title = models.CharField(max_length=200, blank=True)
    values_authenticity_title_en = models.CharField(max_length=200, blank=True)
    values_authenticity_desc = models.TextField(blank=True)
    values_authenticity_desc_en = models.TextField(blank=True)
    values_impact_title = models.CharField(max_length=200, blank=True)
    values_impact_title_en = models.CharField(max_length=200, blank=True)
    values_impact_desc = models.TextField(blank=True)
    values_impact_desc_en = models.TextField(blank=True)

    vision_quote = models.TextField(blank=True)
    vision_quote_en = models.TextField(blank=True)
    vision_role = models.CharField(max_length=200, blank=True)
    vision_role_en = models.CharField(max_length=200, blank=True)

    cta_title = models.CharField(max_length=255, blank=True)
    cta_title_en = models.CharField(max_length=255, blank=True)
    cta_description = models.TextField(blank=True)
    cta_description_en = models.TextField(blank=True)
    cta_blog_btn = models.CharField(max_length=100, blank=True)
    cta_blog_btn_en = models.CharField(max_length=100, blank=True)
    cta_contact_btn = models.CharField(max_length=100, blank=True)
    cta_contact_btn_en = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Page À propos"
        verbose_name_plural = "Page À propos"

    def __str__(self):
        return "Contenu page À propos"

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create()
        obj.apply_defaults_if_missing()
        return obj

    def apply_defaults_if_missing(self):
        changed = apply_i18n_defaults(self, ABOUT_I18N_MAP)
        if changed:
            self.save(update_fields=changed)


class AboutGalleryImage(models.Model):
    """Images de galerie sur la page À propos (distinct de la page /galerie/)."""
    about = models.ForeignKey(
        AboutPageSettings,
        on_delete=models.CASCADE,
        related_name='gallery_images',
    )
    image = models.ImageField(upload_to='about/gallery/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Image galerie (À propos)"
        verbose_name_plural = "Images galerie (À propos)"

    def __str__(self):
        return f"Photo À propos #{self.pk}"


GALLERY_PAGE_I18N_MAP = merge_fr_en_defaults({
    'hero_badge': 'site.gallery.hero.badge',
    'hero_title': 'site.gallery.hero.title',
    'hero_description': 'site.gallery.hero.description',
})


class GalleryPageSettings(models.Model):
    """Page galerie dédiée (singleton) — toutes les photos, distinct de l'aperçu sur l'accueil."""
    hero_badge = models.CharField(max_length=100, blank=True)
    hero_badge_en = models.CharField(max_length=100, blank=True)
    hero_title = models.CharField(max_length=255, blank=True)
    hero_title_en = models.CharField(max_length=255, blank=True)
    hero_description = models.TextField(blank=True)
    hero_description_en = models.TextField(blank=True)

    class Meta:
        verbose_name = "Page Galerie"
        verbose_name_plural = "Page Galerie"

    def __str__(self):
        return "Page Galerie"

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create()
        obj.apply_defaults_if_missing()
        return obj

    def apply_defaults_if_missing(self):
        changed = apply_i18n_defaults(self, GALLERY_PAGE_I18N_MAP)
        if changed:
            self.save(update_fields=changed)


class GalleryPageImage(models.Model):
    gallery = models.ForeignKey(
        GalleryPageSettings,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(upload_to='gallery/page/')
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Photo galerie"
        verbose_name_plural = "Photos galerie"

    def __str__(self):
        return self.caption or f"Photo #{self.pk}"


CONTACT_I18N_MAP = merge_fr_en_defaults({
    'hero_title_prefix': 'site.contact.hero.title_prefix',
    'hero_description': 'site.contact.hero.description',
    'hero_response_time': 'site.contact.hero.response_time',
    'form_title': 'site.contact.form.title',
    'form_description': 'site.contact.form.description',
    'info_title': 'site.contact.info.title',
    'actions_title': 'site.contact.actions.title',
    'actions_discover': 'site.contact.actions.discover',
    'actions_support': 'site.contact.actions.support',
    'social_title': 'site.contact.social.title',
    'faq_title': 'site.contact.faq.title',
    'faq_description': 'site.contact.faq.description',
    'faq_q1': 'site.contact.faq.q1',
    'faq_a1': 'site.contact.faq.q1.answer',
    'faq_q2': 'site.contact.faq.q2',
    'faq_a2': 'site.contact.faq.q2.answer',
    'faq_q3': 'site.contact.faq.q3',
    'faq_a3': 'site.contact.faq.q3.answer',
    'faq_q4': 'site.contact.faq.q4',
    'faq_a4': 'site.contact.faq.q4.answer',
})


class ContactPageSettings(models.Model):
    """Contenu éditable de la page Contact (singleton)."""

    hero_title_prefix = models.CharField(max_length=200, blank=True)
    hero_title_prefix_en = models.CharField(max_length=200, blank=True)
    hero_description = models.TextField(blank=True)
    hero_description_en = models.TextField(blank=True)
    hero_response_time = models.CharField(max_length=120, blank=True)
    hero_response_time_en = models.CharField(max_length=120, blank=True)

    form_title = models.CharField(max_length=255, blank=True)
    form_title_en = models.CharField(max_length=255, blank=True)
    form_description = models.TextField(blank=True)
    form_description_en = models.TextField(blank=True)

    info_title = models.CharField(max_length=200, blank=True)
    info_title_en = models.CharField(max_length=200, blank=True)

    actions_title = models.CharField(max_length=200, blank=True)
    actions_title_en = models.CharField(max_length=200, blank=True)
    actions_discover = models.CharField(max_length=200, blank=True)
    actions_discover_en = models.CharField(max_length=200, blank=True)
    actions_support = models.CharField(max_length=200, blank=True)
    actions_support_en = models.CharField(max_length=200, blank=True)

    social_title = models.CharField(max_length=200, blank=True)
    social_title_en = models.CharField(max_length=200, blank=True)

    faq_title = models.CharField(max_length=255, blank=True)
    faq_title_en = models.CharField(max_length=255, blank=True)
    faq_description = models.TextField(blank=True)
    faq_description_en = models.TextField(blank=True)
    faq_q1 = models.CharField(max_length=300, blank=True)
    faq_q1_en = models.CharField(max_length=300, blank=True)
    faq_a1 = models.TextField(blank=True)
    faq_a1_en = models.TextField(blank=True)
    faq_q2 = models.CharField(max_length=300, blank=True)
    faq_q2_en = models.CharField(max_length=300, blank=True)
    faq_a2 = models.TextField(blank=True)
    faq_a2_en = models.TextField(blank=True)
    faq_q3 = models.CharField(max_length=300, blank=True)
    faq_q3_en = models.CharField(max_length=300, blank=True)
    faq_a3 = models.TextField(blank=True)
    faq_a3_en = models.TextField(blank=True)
    faq_q4 = models.CharField(max_length=300, blank=True)
    faq_q4_en = models.CharField(max_length=300, blank=True)
    faq_a4 = models.TextField(blank=True)
    faq_a4_en = models.TextField(blank=True)

    class Meta:
        verbose_name = "Page Contact"
        verbose_name_plural = "Page Contact"

    def __str__(self):
        return "Contenu page Contact"

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if not obj:
            obj = cls.objects.create()
        obj.apply_defaults_if_missing()
        return obj

    def apply_defaults_if_missing(self):
        changed = apply_i18n_defaults(self, CONTACT_I18N_MAP)
        if changed:
            self.save(update_fields=changed)


class ContactMessage(models.Model):
    """Messages reçus via le formulaire de contact."""

    REQUEST_TYPE_CHOICES = [
        ('blog', 'Blog'),
        ('collaboration', 'Collaboration'),
        ('barika', 'MY BARIKA - Bénévolat'),
        ('barika_don', 'MY BARIKA - Don'),
        ('coaching', 'Coaching'),
        ('autre', 'Autre'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    request_type = models.CharField(max_length=30, blank=True, choices=REQUEST_TYPE_CHOICES)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"

    def __str__(self):
        return f"{self.name} — {self.subject[:40]}"
