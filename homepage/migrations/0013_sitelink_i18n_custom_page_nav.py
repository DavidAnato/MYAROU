import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0012_alter_contactmessage_email_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitelink',
            name='label_en',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='sitelink',
            name='custom_page',
            field=models.ForeignKey(
                blank=True,
                help_text='Lien auto-généré pour une page libre du menu.',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='nav_links',
                to='homepage.custompage',
            ),
        ),
    ]
