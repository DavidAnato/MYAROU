import homepage.models_site
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0010_custompageblock_custompageblockimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custompageblock',
            name='image',
            field=models.ImageField(
                blank=True,
                max_length=255,
                null=True,
                upload_to=homepage.models_site.block_image_upload_to,
            ),
        ),
        migrations.AlterField(
            model_name='custompageblockimage',
            name='image',
            field=models.ImageField(
                max_length=255,
                upload_to=homepage.models_site.block_gallery_image_upload_to,
            ),
        ),
    ]
