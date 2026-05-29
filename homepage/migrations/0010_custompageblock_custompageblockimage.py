import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


def migrate_content_to_blocks(apps, schema_editor):
    CustomPage = apps.get_model('homepage', 'CustomPage')
    CustomPageBlock = apps.get_model('homepage', 'CustomPageBlock')
    for page in CustomPage.objects.all():
        if CustomPageBlock.objects.filter(page=page).exists():
            continue
        if not page.content and not page.content_en:
            continue
        CustomPageBlock.objects.create(
            page=page,
            block_type='richtext',
            order=0,
            is_visible=True,
            content=page.content or '',
            content_en=page.content_en or '',
        )


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0009_sitepage_custompage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPageBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_type', models.CharField(choices=[('hero', 'Hero'), ('richtext', 'Texte riche'), ('image', 'Image'), ('image_text', 'Image + texte'), ('gallery', 'Galerie'), ('video', 'Vidéo'), ('cta', 'Call-to-action'), ('faq', 'FAQ'), ('spacer', 'Espacement')], max_length=30)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_visible', models.BooleanField(default=True)),
                ('badge', models.CharField(blank=True, max_length=120)),
                ('badge_en', models.CharField(blank=True, max_length=120)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('title_en', models.CharField(blank=True, max_length=255)),
                ('subtitle', models.CharField(blank=True, max_length=500)),
                ('subtitle_en', models.CharField(blank=True, max_length=500)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Contenu')),
                ('content_en', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Contenu (EN)')),
                ('image', models.ImageField(blank=True, null=True, upload_to='pages/blocks/')),
                ('image_alt', models.CharField(blank=True, max_length=255)),
                ('video_url', models.URLField(blank=True, max_length=500)),
                ('button_text', models.CharField(blank=True, max_length=120)),
                ('button_text_en', models.CharField(blank=True, max_length=120)),
                ('button_url', models.CharField(blank=True, max_length=500)),
                ('layout', models.CharField(blank=True, default='', max_length=30)),
                ('config', models.JSONField(blank=True, default=dict)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks', to='homepage.custompage')),
            ],
            options={
                'verbose_name': 'Bloc de page',
                'verbose_name_plural': 'Blocs de page',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='CustomPageBlockImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='pages/blocks/gallery/')),
                ('caption', models.CharField(blank=True, max_length=255)),
                ('caption_en', models.CharField(blank=True, max_length=255)),
                ('order', models.PositiveIntegerField(default=0)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='homepage.custompageblock')),
            ],
            options={
                'verbose_name': 'Image de bloc',
                'verbose_name_plural': 'Images de bloc',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.RunPython(migrate_content_to_blocks, migrations.RunPython.noop),
    ]
