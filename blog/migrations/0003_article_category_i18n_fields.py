from django.db import migrations, models
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_article_video_file_article_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='title_en',
            field=models.CharField(blank=True, help_text="Titre en anglais (repli sur le français si vide).", max_length=255, verbose_name='Titre (EN)'),
        ),
        migrations.AddField(
            model_name='article',
            name='content_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, config_name='awesome_ckeditor', help_text="Contenu en anglais (repli sur le français si vide).", verbose_name='Contenu (EN)'),
        ),
        migrations.AddField(
            model_name='article',
            name='excerpt_en',
            field=models.TextField(blank=True, help_text="Extrait en anglais (repli sur le français si vide).", max_length=500, verbose_name='Extrait (EN)'),
        ),
        migrations.AddField(
            model_name='article',
            name='meta_description_en',
            field=models.CharField(blank=True, help_text="Description SEO en anglais (repli sur le français si vide).", max_length=160, verbose_name='Meta description (EN)'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_en',
            field=models.CharField(blank=True, help_text="Nom en anglais (repli sur le français si vide).", max_length=100, verbose_name='Nom (EN)'),
        ),
        migrations.AddField(
            model_name='category',
            name='description_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, config_name='awesome_ckeditor', help_text="Description en anglais (repli sur le français si vide).", verbose_name='Description (EN)'),
        ),
    ]
