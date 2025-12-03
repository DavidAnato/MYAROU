from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    """Catégories pour organiser les articles"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom",
        help_text="Nom de la catégorie."
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        help_text="Généré automatiquement à partir du nom."
    )
    description = RichTextUploadingField(
        blank=True,
        config_name='awesome_ckeditor',
        verbose_name="Description",
        help_text="Description de la catégorie avec support HTML, images, etc."
    )
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        help_text="Image de la catégorie (optionnel)."
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_article_count(self):
        """Retourne le nombre d'articles publiés dans cette catégorie"""
        return self.articles.filter(status='published').count()
    get_article_count.short_description = "Articles publiés"


class Article(models.Model):
    """Articles de blog"""
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
        ('archived', 'Archivé'),
    ]
    
    # Contenu principal
    title = models.CharField(
        max_length=255,
        verbose_name="Titre",
        help_text="Titre de l'article."
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text="Slug généré automatiquement."
    )
    content = RichTextUploadingField(
        config_name='awesome_ckeditor',
        verbose_name="Contenu",
        help_text="Contenu principal de l'article avec éditeur HTML riche."
    )
    excerpt = models.TextField(
        blank=True,
        max_length=500,
        verbose_name="Extrait",
        help_text="Court extrait de l'article pour les listes (optionnel)."
    )
    image = models.ImageField(
        upload_to='articles/',
        blank=True,
        null=True,
        help_text="Image principale (optionnel)."
    )
    
    # Auteur en texte simple
    author = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Auteur",
        help_text="Nom de l'auteur"
    )
    
    # Relations
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
        verbose_name="Catégorie",
        help_text="Catégorie de l'article."
    )
    
    # Métadonnées
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text="Tags séparés par des virgules."
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Statut",
        help_text="Statut de publication."
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name="Vues",
        help_text="Nombre de vues de l'article."
    )
    
    # Dates
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )
    published_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Date de publication"
    )
    
    # SEO
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name="Meta description",
        help_text="Description SEO (max 160 caractères)."
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Mots-clés SEO",
        help_text="Mots-clés SEO séparés par des virgules."
    )
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        """Retourne les tags sous forme de liste"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
