import ckeditor_uploader.fields
from django.db import migrations, models


DEFAULT_SITE_PAGES = [
    ('blog:home', 'Accueil', 'Home', 0),
    ('blog:about', 'À propos', 'About', 10),
    ('blog:article_list', 'Blog', 'Blog', 20),
    ('blog:gallery', 'Galerie', 'Gallery', 30),
    ('blog:contact', 'Contact', 'Contact', 40),
]


def seed_site_pages(apps, schema_editor):
    SitePage = apps.get_model('homepage', 'SitePage')
    for route_name, label, label_en, order in DEFAULT_SITE_PAGES:
        SitePage.objects.get_or_create(
            route_name=route_name,
            defaults={
                'label': label,
                'label_en': label_en,
                'order': order,
                'is_visible': True,
                'show_in_nav': True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0008_remove_sitelink_useful_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='SitePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_name', models.CharField(choices=[('blog:home', 'Accueil'), ('blog:about', 'À propos'), ('blog:article_list', 'Blog'), ('blog:gallery', 'Galerie'), ('blog:contact', 'Contact')], max_length=80, unique=True)),
                ('label', models.CharField(blank=True, max_length=120)),
                ('label_en', models.CharField(blank=True, max_length=120)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_visible', models.BooleanField(default=True, help_text='Page accessible publiquement (404 si désactivée). L’accueil reste toujours accessible.')),
                ('show_in_nav', models.BooleanField(default=True, help_text='Afficher dans le menu principal.')),
            ],
            options={
                'verbose_name': 'Page du site',
                'verbose_name_plural': 'Pages du site',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='CustomPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=120, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('title_en', models.CharField(blank=True, max_length=255)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Contenu')),
                ('content_en', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Contenu (EN)')),
                ('is_published', models.BooleanField(default=False)),
                ('show_in_nav', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=100)),
                ('meta_description', models.CharField(blank=True, max_length=160)),
                ('meta_description_en', models.CharField(blank=True, max_length=160)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Page personnalisée',
                'verbose_name_plural': 'Pages personnalisées',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.RunPython(seed_site_pages, migrations.RunPython.noop),
    ]
