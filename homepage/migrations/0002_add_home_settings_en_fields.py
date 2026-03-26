from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(model_name='homesettings', name='articles_desc_en', field=models.TextField(blank=True)),
        migrations.AddField(model_name='homesettings', name='articles_read_more_en', field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name='homesettings', name='articles_title_prefix_en', field=models.CharField(blank=True, max_length=255)),
        migrations.AddField(model_name='homesettings', name='articles_title_suffix_en', field=models.CharField(blank=True, max_length=255)),
        migrations.AddField(model_name='homesettings', name='articles_view_all_en', field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name='homesettings', name='barika_cta_en', field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name='homesettings', name='barika_desc_en', field=models.TextField(blank=True)),
        migrations.AddField(model_name='homesettings', name='barika_education_desc_en', field=models.TextField(blank=True)),
        migrations.AddField(model_name='homesettings', name='barika_education_title_en', field=models.CharField(blank=True, max_length=200)),
        migrations.AddField(model_name='homesettings', name='barika_entrepreneurship_desc_en', field=models.TextField(blank=True)),
        migrations.AddField(model_name='homesettings', name='barika_entrepreneurship_title_en', field=models.CharField(blank=True, max_length=200)),
        migrations.AddField(model_name='homesettings', name='barika_sport_desc_en', field=models.TextField(blank=True)),
        migrations.AddField(model_name='homesettings', name='barika_sport_title_en', field=models.CharField(blank=True, max_length=200)),
        migrations.AddField(model_name='homesettings', name='hero_badge_en', field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name='homesettings', name='hero_description_en', field=models.TextField(blank=True)),
        migrations.AddField(model_name='homesettings', name='hero_title_prefix_en', field=models.CharField(blank=True, max_length=200)),
        migrations.AddField(model_name='homesettings', name='hero_title_suffix_en', field=models.CharField(blank=True, max_length=200)),
        migrations.AddField(model_name='homesettings', name='join_badge_en', field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name='homesettings', name='join_cta_en', field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name='homesettings', name='join_desc_en', field=models.TextField(blank=True)),
        migrations.AddField(model_name='homesettings', name='join_title_prefix_en', field=models.CharField(blank=True, max_length=255)),
        migrations.AddField(model_name='homesettings', name='quote_author_role_en', field=models.CharField(blank=True, max_length=255)),
        migrations.AddField(model_name='homesettings', name='quote_cta_en', field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name='homesettings', name='quote_subtext_en', field=models.CharField(blank=True, max_length=255)),
        migrations.AddField(model_name='homesettings', name='quote_text_en', field=models.TextField(blank=True)),
        migrations.AddField(model_name='homesettings', name='values_excellence_desc_en', field=models.TextField(blank=True)),
        migrations.AddField(model_name='homesettings', name='values_excellence_title_en', field=models.CharField(blank=True, max_length=200)),
        migrations.AddField(model_name='homesettings', name='values_impact_desc_en', field=models.TextField(blank=True)),
        migrations.AddField(model_name='homesettings', name='values_impact_title_en', field=models.CharField(blank=True, max_length=200)),
        migrations.AddField(model_name='homesettings', name='values_leadership_desc_en', field=models.TextField(blank=True)),
        migrations.AddField(model_name='homesettings', name='values_leadership_title_en', field=models.CharField(blank=True, max_length=200)),
        migrations.AddField(model_name='homesettings', name='vision_badge_en', field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name='homesettings', name='vision_description_en', field=models.TextField(blank=True)),
        migrations.AddField(model_name='homesettings', name='vision_title_en', field=models.CharField(blank=True, max_length=255)),
    ]
