from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0006_sitelink_route_nav_defaults'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='is_read',
            field=models.BooleanField(default=False, verbose_name='Lu'),
        ),
    ]
