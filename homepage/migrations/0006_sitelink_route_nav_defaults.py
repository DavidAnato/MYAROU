from django.db import migrations, models


def seed_default_links(apps, schema_editor):
    SiteLink = apps.get_model('homepage', 'SiteLink')
    nav = [
        ('blog:home', 'Accueil', 0),
        ('blog:about', 'À propos', 10),
        ('blog:article_list', 'Blog', 20),
        ('blog:gallery', 'Galerie', 30),
        ('blog:contact', 'Contact', 40),
    ]
    barika = [
        ('blog:contact', 'Nos programmes', 0),
        ('blog:contact', 'Soutiens', 10),
        ('blog:contact', 'Devenir bénévole', 20),
    ]
    if not SiteLink.objects.filter(category='nav').exists():
        for route_name, label, order in nav:
            SiteLink.objects.create(
                category='nav',
                platform='website',
                label=label,
                route_name=route_name,
                url='',
                order=order,
                is_active=True,
                open_in_new_tab=False,
            )
    if not SiteLink.objects.filter(category='footer').exists():
        for route_name, label, order in barika:
            SiteLink.objects.create(
                category='footer',
                platform='website',
                label=label,
                route_name=route_name,
                url='',
                order=order,
                is_active=True,
                open_in_new_tab=False,
            )


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0005_sitelink_url_blank'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitelink',
            name='route_name',
            field=models.CharField(
                blank=True,
                choices=[
                    ('', '— URL personnalisée —'),
                    ('blog:home', 'Accueil'),
                    ('blog:about', 'À propos'),
                    ('blog:article_list', 'Blog'),
                    ('blog:gallery', 'Galerie'),
                    ('blog:contact', 'Contact'),
                ],
                help_text='Page interne du site (prioritaire sur l’URL si renseigné).',
                max_length=80,
            ),
        ),
        migrations.AlterField(
            model_name='sitelink',
            name='category',
            field=models.CharField(
                choices=[
                    ('social', 'Réseaux sociaux'),
                    ('nav', 'Navigation (footer)'),
                    ('footer', 'MY BARIKA (footer)'),
                    ('useful', 'Liens utiles'),
                ],
                default='social',
                max_length=20,
            ),
        ),
        migrations.RunPython(seed_default_links, migrations.RunPython.noop),
    ]
