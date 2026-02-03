from django.core.management.base import BaseCommand
from blog.models import Article
import random

class Command(BaseCommand):
    help = 'Ajoute une vidéo ou un lien vidéo aux articles existants'

    def handle(self, *args, **kwargs):
        articles = Article.objects.all()
        
        # Liste de vidéos YouTube d'exemple (Tech, Nature, Motivation)
        video_urls = [
            'https://www.youtube.com/watch?v=LXb3EKWsInQ', # Nature 4K
            'https://www.youtube.com/watch?v=fJ9rUzIMcZQ', # Queen - Bohemian Rhapsody
            'https://www.youtube.com/watch?v=jNQXAC9IVRw', # Me at the zoo
            'https://www.youtube.com/watch?v=9bZkp7q19f0', # PSY - GANGNAM STYLE
        ]
        
        updated_count = 0
        
        self.stdout.write('Début de la mise à jour des articles...')
        
        for article in articles:
            # On ne touche pas aux articles qui ont déjà une vidéo (fichier ou URL)
            if not article.video_file and not article.video_url:
                article.video_url = random.choice(video_urls)
                article.save()
                self.stdout.write(self.style.SUCCESS(f'Vidéo ajoutée à "{article.title}"'))
                updated_count += 1
            else:
                self.stdout.write(f'Article "{article.title}" a déjà une vidéo')
                
        self.stdout.write(self.style.SUCCESS(f'\nTerminé ! {updated_count} articles mis à jour.'))
