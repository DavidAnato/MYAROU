from django.db import migrations, models


def delete_useful_links(apps, schema_editor):
    SiteLink = apps.get_model('homepage', 'SiteLink')
    SiteLink.objects.filter(category='useful').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0007_contactmessage_is_read'),
    ]

    operations = [
        migrations.RunPython(delete_useful_links, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='sitelink',
            name='category',
            field=models.CharField(
                choices=[
                    ('social', 'Réseaux sociaux'),
                    ('nav', 'Navigation (footer)'),
                    ('footer', 'MY BARIKA (footer)'),
                ],
                default='social',
                max_length=20,
            ),
        ),
    ]
