from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_aboutgalleryimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitelink',
            name='url',
            field=models.URLField(blank=True, max_length=500),
        ),
    ]
