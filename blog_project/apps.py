from django.apps import AppConfig
from .utils.i18n import load_translations

class BlogProjectConfig(AppConfig):
    name = 'blog_project'

    def ready(self):
        load_translations()
