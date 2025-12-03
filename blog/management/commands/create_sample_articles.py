# blog/management/commands/create_sample_articles.py

import os
import requests
from io import BytesIO
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Article, Category


class Command(BaseCommand):
    help = 'Crée 10 articles de blog avec du contenu et des images'

    def handle(self, *args, **kwargs):
        # Créer les catégories d'abord
        self.stdout.write(self.style.SUCCESS('Création des catégories...'))
        categories_data = [
            {
                'name': 'Leadership',
                'description': '<p>Développez vos compétences de leader et inspirez votre équipe.</p>',
                'image_url': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=800&q=80'
            },
            {
                'name': 'Entrepreneuriat',
                'description': '<p>Lancez et développez votre entreprise avec succès.</p>',
                'image_url': 'https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=800&q=80'
            },
            {
                'name': 'Développement Personnel',
                'description': '<p>Investissez en vous-même et atteignez vos objectifs.</p>',
                'image_url': 'https://images.unsplash.com/photo-1516534775068-ba3e7458af70?w=800&q=80'
            },
            {
                'name': 'Basketball',
                'description': '<p>Le basketball comme école de vie et de discipline.</p>',
                'image_url': 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800&q=80'
            },
            {
                'name': 'Éducation',
                'description': '<p>L\'importance de l\'éducation pour transformer l\'Afrique.</p>',
                'image_url': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&q=80'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created and cat_data.get('image_url'):
                self.download_and_save_image(category, cat_data['image_url'], 'category')
            categories[cat_data['name']] = category
            self.stdout.write(self.style.SUCCESS(f'✓ Catégorie "{cat_data["name"]}" créée'))

        # Données des articles
        articles_data = [
            {
                'title': 'Les 7 Habitudes des Leaders qui Réussissent',
                'category': 'Leadership',
                'excerpt': 'Découvrez les habitudes essentielles que partagent tous les grands leaders, du terrain de basket aux salles de conférence.',
                'content': '''
                    <h2>Introduction au Leadership d'Excellence</h2>
                    <p>Après 15 années passées sur les terrains de basketball professionnels et dans les salles de conseil d'administration, j'ai identifié 7 habitudes fondamentales que partagent tous les leaders exceptionnels.</p>
                    
                    <h2>1. La Vision Claire</h2>
                    <p>Un leader sans vision est comme un capitaine sans boussole. La première habitude des grands leaders est d'avoir une vision claire de là où ils veulent aller et de savoir communiquer cette vision à leur équipe.</p>
                    
                    <h2>2. L'Authenticité</h2>
                    <p>Restez fidèle à vos valeurs. L'authenticité crée la confiance, et la confiance est le fondement de tout leadership efficace.</p>
                    
                    <h2>3. L'Écoute Active</h2>
                    <p>Les meilleurs leaders écoutent plus qu'ils ne parlent. Ils comprennent que chaque membre de l'équipe a quelque chose de précieux à apporter.</p>
                    
                    <h2>4. La Discipline</h2>
                    <p>Le succès n'est pas le fruit du hasard. C'est le résultat d'une discipline quotidienne, de routines établies et d'une exécution constante.</p>
                    
                    <h2>5. L'Humilité</h2>
                    <p>Les grands leaders savent qu'ils ne savent pas tout. Ils sont ouverts à l'apprentissage et reconnaissent les contributions de leur équipe.</p>
                    
                    <h2>6. La Résilience</h2>
                    <p>Les obstacles sont inévitables. Ce qui distingue les leaders, c'est leur capacité à rebondir après l'échec et à tirer des leçons de chaque expérience.</p>
                    
                    <h2>7. L'Action</h2>
                    <p>Un leader qui ne passe pas à l'action reste un rêveur. L'exécution est la clé qui transforme la vision en réalité.</p>
                    
                    <h2>Conclusion</h2>
                    <p>Ces sept habitudes ne sont pas innées, elles se cultivent. Commencez dès aujourd'hui à les intégrer dans votre quotidien et observez la transformation dans votre leadership.</p>
                ''',
                'tags': 'leadership, développement personnel, réussite, habits',
                'image_url': 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1200&q=80',
                'meta_description': 'Découvrez les 7 habitudes essentielles des leaders qui réussissent, inspirées de 15 ans d\'expérience en basketball professionnel et en entrepreneuriat.'
            },
            {
                'title': 'Du Terrain de Basket au MBA HEC : Mon Parcours',
                'category': 'Développement Personnel',
                'excerpt': 'Comment le basketball m\'a préparé aux défis du monde des affaires et pourquoi la discipline sportive est transférable au business.',
                'content': '''
                    <h2>Les Débuts au Bénin</h2>
                    <p>Tout a commencé sur les terrains poussiéreux de Cotonou. Le basketball n'était pas juste un sport pour moi, c'était une école de vie qui m'enseignait des leçons que je n'aurais jamais apprises en classe.</p>
                    
                    <h2>Villanova University : Le Tremplin</h2>
                    <p>Obtenir une bourse pour Villanova University a été un tournant décisif. Là-bas, j'ai découvert que l'excellence académique et sportive pouvaient coexister et se renforcer mutuellement.</p>
                    
                    <blockquote>
                    "Le basketball m'a appris que le talent seul ne suffit pas. C'est le travail acharné et la discipline qui font la différence."
                    </blockquote>
                    
                    <h2>La Carrière Professionnelle en Europe</h2>
                    <p>Jouer professionnellement en Europe m'a exposé à différentes cultures et manières de penser. Chaque pays, chaque équipe avait sa propre philosophie, et j'ai appris à m'adapter constamment.</p>
                    
                    <h2>La Transition vers HEC Paris</h2>
                    <p>Passer du terrain de basket aux amphithéâtres de HEC Paris n'a pas été facile, mais les compétences acquises en tant qu'athlète professionnel se sont révélées inestimables :</p>
                    <ul>
                        <li>Gestion de la pression</li>
                        <li>Travail d'équipe</li>
                        <li>Leadership</li>
                        <li>Résilience face à l'échec</li>
                        <li>Discipline et rigueur</li>
                    </ul>
                    
                    <h2>Les Leçons Clés</h2>
                    <p>Ce parcours m'a enseigné que les frontières entre le sport et le business sont plus floues qu'on ne le pense. Les mêmes principes de travail, de discipline et d'excellence s'appliquent partout.</p>
                ''',
                'tags': 'parcours, basketball, MBA, HEC, développement personnel',
                'image_url': 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&q=80',
                'meta_description': 'Le parcours inspirant d\'un basketteur professionnel devenu diplômé MBA HEC Paris. Découvrez comment le sport prépare au monde des affaires.'
            },
            {
                'title': 'Créer une Entreprise Sociale en Afrique : Guide Complet',
                'category': 'Entrepreneuriat',
                'excerpt': 'Les étapes essentielles pour lancer une entreprise sociale qui a un impact positif sur les communautés africaines.',
                'content': '''
                    <h2>Pourquoi l'Entrepreneuriat Social ?</h2>
                    <p>L'Afrique ne manque pas de problèmes, mais elle regorge d'opportunités. L'entrepreneuriat social permet de créer de la valeur économique tout en résolvant des problèmes sociaux.</p>
                    
                    <h2>Étape 1 : Identifier un Problème Réel</h2>
                    <p>Ne créez pas une solution à la recherche d'un problème. Commencez par observer votre communauté et identifier les défis concrets que les gens rencontrent au quotidien.</p>
                    
                    <h2>Étape 2 : Comprendre Votre Marché</h2>
                    <p>Qui sont vos bénéficiaires ? Quels sont leurs besoins réels ? Ne supposez pas, allez sur le terrain et parlez aux personnes concernées.</p>
                    
                    <h2>Étape 3 : Créer un Modèle Économique Viable</h2>
                    <p>Une entreprise sociale doit être financièrement viable pour avoir un impact durable. Trouvez le juste équilibre entre impact social et rentabilité économique.</p>
                    
                    <h2>Étape 4 : Construire une Équipe Engagée</h2>
                    <p>L'entrepreneuriat social nécessite des personnes passionnées par la mission. Entourez-vous de collaborateurs qui partagent vos valeurs.</p>
                    
                    <h2>Étape 5 : Mesurer Votre Impact</h2>
                    <p>Comment saurez-vous si vous réussissez ? Établissez des indicateurs clairs pour mesurer à la fois votre impact social et votre performance économique.</p>
                    
                    <h2>Les Défis à Anticiper</h2>
                    <ul>
                        <li>Accès au financement</li>
                        <li>Infrastructure limitée</li>
                        <li>Réglementation complexe</li>
                        <li>Recrutement de talents</li>
                    </ul>
                    
                    <h2>Conclusion</h2>
                    <p>Créer une entreprise sociale en Afrique est un défi, mais c'est aussi l'une des aventures les plus gratifiantes. Avec MY BARIKA, nous avons prouvé que c'est possible.</p>
                ''',
                'tags': 'entrepreneuriat, afrique, entreprise sociale, impact social',
                'image_url': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1200&q=80',
                'meta_description': 'Guide complet pour créer une entreprise sociale en Afrique. Étapes, défis et solutions pour un entrepreneuriat à impact positif.'
            },
            {
                'title': '10 Leçons de Vie Apprises sur le Terrain de Basket',
                'category': 'Basketball',
                'excerpt': 'Le basketball est bien plus qu\'un sport. C\'est une métaphore de la vie qui enseigne des leçons précieuses applicables dans tous les domaines.',
                'content': '''
                    <h2>Introduction</h2>
                    <p>Quinze années sur les terrains de basketball m'ont enseigné des leçons que je n'aurais jamais apprises ailleurs. Voici les 10 plus importantes.</p>
                    
                    <h2>1. L'Échec est un Professeur</h2>
                    <p>Rater un panier décisif fait mal, mais c'est dans ces moments qu'on apprend le plus sur soi-même et sur la manière de rebondir.</p>
                    
                    <h2>2. Le Succès est Collectif</h2>
                    <p>Même les plus grands joueurs ne gagnent pas seuls. Le basketball enseigne que le succès est toujours le fruit d'un effort collectif.</p>
                    
                    <h2>3. La Préparation Détermine la Performance</h2>
                    <p>Les matchs se gagnent à l'entraînement, pas sur le terrain. La préparation est la clé de la performance.</p>
                    
                    <h2>4. L'Adaptation est Essentielle</h2>
                    <p>Chaque adversaire est différent, chaque match présente de nouveaux défis. La capacité à s'adapter rapidement est cruciale.</p>
                    
                    <h2>5. La Résilience Mentale</h2>
                    <p>Un match se joue autant dans la tête que sur le terrain. La force mentale fait la différence dans les moments critiques.</p>
                    
                    <h2>6. L'Humilité dans la Victoire</h2>
                    <p>Célébrez vos succès, mais restez humble. Il y aura toujours quelqu'un de meilleur que vous quelque part.</p>
                    
                    <h2>7. La Discipline Quotidienne</h2>
                    <p>L'excellence n'est pas un acte, c'est une habitude. La discipline quotidienne construit la grandeur.</p>
                    
                    <h2>8. Le Respect des Adversaires</h2>
                    <p>Vos adversaires vous poussent à être meilleur. Respectez-les et apprenez d'eux.</p>
                    
                    <h2>9. La Gestion de la Pression</h2>
                    <p>Les moments de pression révèlent qui vous êtes vraiment. Apprenez à les embrasser plutôt qu'à les fuir.</p>
                    
                    <h2>10. Le Leadership par l'Exemple</h2>
                    <p>On ne peut pas demander aux autres ce qu'on ne fait pas soi-même. Le vrai leadership commence par l'exemple.</p>
                ''',
                'tags': 'basketball, leçons de vie, sport, développement personnel',
                'image_url': 'https://images.unsplash.com/photo-1608245449230-4ac19066d2d0?w=1200&q=80',
                'meta_description': '10 leçons de vie puissantes apprises sur le terrain de basketball, applicables dans tous les domaines de la vie.'
            },
            {
                'title': 'MY BARIKA : L\'Histoire d\'un Projet qui Change des Vies',
                'category': 'Éducation',
                'excerpt': 'Découvrez comment MY BARIKA est né et comment ce projet transforme la vie de centaines de jeunes Africains à travers l\'éducation et le sport.',
                'content': '''
                    <h2>La Genèse du Projet</h2>
                    <p>MY BARIKA est né d'une conviction simple : chaque jeune Africain mérite d'avoir accès aux mêmes opportunités que j'ai eues. Le sport et l'éducation ont transformé ma vie, et je voulais offrir cette chance à d'autres.</p>
                    
                    <h2>La Vision</h2>
                    <p>Notre vision est de créer une génération de leaders africains équipés des compétences nécessaires pour transformer leurs communautés. Nous croyons que le sport est un vecteur puissant de développement personnel et social.</p>
                    
                    <h2>Les Trois Piliers</h2>
                    
                    <h3>1. Éducation</h3>
                    <p>Nous offrons des bourses scolaires et du soutien académique aux jeunes talents. L'éducation est la fondation sur laquelle tout le reste se construit.</p>
                    
                    <h3>2. Sport</h3>
                    <p>Nos camps de basketball enseignent bien plus que les techniques sportives. Ils enseignent la discipline, le travail d'équipe, et la résilience.</p>
                    
                    <h3>3. Entrepreneuriat</h3>
                    <p>Nous accompagnons les jeunes dans la création de leurs propres projets, leur donnant les outils pour devenir des acteurs économiques dans leurs communautés.</p>
                    
                    <h2>L'Impact en Chiffres</h2>
                    <ul>
                        <li>Plus de 500 jeunes accompagnés</li>
                        <li>50 bourses d'études attribuées</li>
                        <li>15 camps de basketball organisés</li>
                        <li>20 projets entrepreneuriaux soutenus</li>
                    </ul>
                    
                    <h2>Témoignages</h2>
                    <blockquote>
                    "MY BARIKA m'a donné l'opportunité de poursuivre mes études tout en continuant à jouer au basketball. Aujourd'hui, je suis à l'université et je rêve de devenir ingénieur." - Jean, 19 ans
                    </blockquote>
                    
                    <h2>Comment Vous Pouvez Aider</h2>
                    <p>MY BARIKA dépend du soutien de personnes généreuses qui partagent notre vision. Vous pouvez contribuer de plusieurs façons :</p>
                    <ul>
                        <li>Faire un don</li>
                        <li>Devenir bénévole</li>
                        <li>Parrainer un jeune</li>
                        <li>Partager notre mission</li>
                    </ul>
                ''',
                'tags': 'MY BARIKA, éducation, afrique, impact social, basketball',
                'image_url': 'https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1200&q=80',
                'meta_description': 'L\'histoire inspirante de MY BARIKA, un projet qui transforme la vie de centaines de jeunes Africains à travers l\'éducation et le sport.'
            },
            {
                'title': 'Comment Développer une Mentalité de Champion',
                'category': 'Développement Personnel',
                'excerpt': 'La mentalité fait toute la différence entre le succès et l\'échec. Découvrez comment développer une mentalité de champion dans tous les aspects de votre vie.',
                'content': '''
                    <h2>Qu'est-ce qu'une Mentalité de Champion ?</h2>
                    <p>Une mentalité de champion n'est pas réservée aux athlètes d'élite. C'est un état d'esprit qui peut être cultivé par quiconque est prêt à faire le travail nécessaire.</p>
                    
                    <h2>Les Caractéristiques Clés</h2>
                    
                    <h3>1. L'Obsession de l'Excellence</h3>
                    <p>Les champions ne se contentent jamais de "assez bien". Ils cherchent constamment à s'améliorer, même quand ils sont au sommet.</p>
                    
                    <h3>2. L'Acceptation de l'Inconfort</h3>
                    <p>La croissance se produit hors de votre zone de confort. Les champions embrassent l'inconfort comme une opportunité de croissance.</p>
                    
                    <h3>3. La Vision à Long Terme</h3>
                    <p>Les champions sacrifient la gratification immédiate pour des objectifs à long terme. Ils comprennent que le succès est un marathon, pas un sprint.</p>
                    
                    <h2>Les 5 Pratiques Quotidiennes</h2>
                    
                    <h3>1. La Visualisation</h3>
                    <p>Passez 10 minutes chaque matin à visualiser votre succès. Votre cerveau ne fait pas la différence entre l'imagination et la réalité.</p>
                    
                    <h3>2. L'Affirmation Positive</h3>
                    <p>Ce que vous vous dites devient votre réalité. Remplacez le dialogue intérieur négatif par des affirmations positives.</p>
                    
                    <h3>3. La Lecture</h3>
                    <p>Lisez 30 minutes par jour. Les champions sont des apprenants permanents.</p>
                    
                    <h3>4. L'Exercice Physique</h3>
                    <p>Un esprit sain dans un corps sain. L'exercice régulier booste votre énergie mentale et physique.</p>
                    
                    <h3>5. La Réflexion</h3>
                    <p>Prenez 10 minutes chaque soir pour réfléchir à votre journée. Qu'avez-vous appris ? Comment pouvez-vous vous améliorer ?</p>
                    
                    <h2>Surmonter les Obstacles Mentaux</h2>
                    <p>Les barrières les plus importantes sont souvent dans notre tête. Identifiez vos croyances limitantes et remplacez-les par des croyances habilitantes.</p>
                    
                    <h2>Conclusion</h2>
                    <p>Développer une mentalité de champion est un processus, pas un événement. Commencez aujourd'hui, soyez patient avec vous-même, et observez la transformation.</p>
                ''',
                'tags': 'mentalité, champion, développement personnel, mindset, excellence',
                'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=1200&q=80',
                'meta_description': 'Guide complet pour développer une mentalité de champion. Pratiques quotidiennes et stratégies pour exceller dans tous les domaines de la vie.'
            },
            {
                'title': 'L\'Importance de l\'Éducation pour Transformer l\'Afrique',
                'category': 'Éducation',
                'excerpt': 'L\'éducation est la clé qui déverrouillera le potentiel immense de l\'Afrique. Explorons pourquoi et comment investir dans l\'éducation africaine.',
                'content': '''
                    <h2>Le Défi Éducatif Africain</h2>
                    <p>L'Afrique possède la population la plus jeune du monde. D'ici 2050, un quart de la population mondiale sera africaine. Cette jeunesse représente un potentiel extraordinaire, mais seulement si elle est éduquée.</p>
                    
                    <h2>Les Obstacles Actuels</h2>
                    <ul>
                        <li>Manque d'infrastructures scolaires</li>
                        <li>Pénurie d'enseignants qualifiés</li>
                        <li>Pauvreté qui force les enfants à travailler</li>
                        <li>Inégalités entre zones urbaines et rurales</li>
                        <li>Disparités de genre dans l'accès à l'éducation</li>
                    </ul>
                    
                    <h2>Pourquoi l'Éducation est Cruciale</h2>
                    
                    <h3>1. Développement Économique</h3>
                    <p>Chaque année d'éducation supplémentaire augmente le revenu potentiel d'un individu de 10%. Une population éduquée crée une économie plus productive et innovante.</p>
                    
                    <h3>2. Santé Publique</h3>
                    <p>L'éducation améliore la santé. Les personnes éduquées prennent de meilleures décisions pour leur santé et celle de leur famille.</p>
                    
                    <h3>3. Gouvernance</h3>
                    <p>Une population éduquée exige une meilleure gouvernance et participe plus activement à la vie démocratique.</p>
                    
                    <h3>4. Innovation</h3>
                    <p>Les solutions aux problèmes africains viendront des Africains éduqués qui comprennent leurs contextes locaux.</p>
                    
                    <h2>Des Solutions Innovantes</h2>
                    
                    <h3>L'Éducation Numérique</h3>
                    <p>La technologie peut aider à surmonter le manque d'infrastructures. Les plateformes d'apprentissage en ligne rendent l'éducation accessible partout.</p>
                    
                    <h3>Les Partenariats Public-Privé</h3>
                    <p>Les gouvernements seuls ne peuvent pas résoudre le défi éducatif. Les entreprises et les ONGs doivent s'engager.</p>
                    
                    <h3>L'Éducation Pratique</h3>
                    <p>L'éducation doit être pertinente. Nous devons former les jeunes aux compétences dont l'économie africaine a besoin.</p>
                    
                    <h2>Le Rôle de MY BARIKA</h2>
                    <p>À travers MY BARIKA, nous travaillons à rendre l'éducation de qualité accessible aux jeunes défavorisés. Chaque bourse que nous offrons est un investissement dans l'avenir de l'Afrique.</p>
                    
                    <h2>Comment Vous Pouvez Contribuer</h2>
                    <p>La transformation de l'éducation africaine nécessite l'engagement de tous. Que vous soyez en Afrique ou ailleurs, vous pouvez contribuer par des dons, du bénévolat, ou en sensibilisant votre entourage.</p>
                ''',
                'tags': 'éducation, afrique, développement, transformation sociale',
                'image_url': 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=1200&q=80',
                'meta_description': 'L\'éducation comme levier de transformation de l\'Afrique. Défis, solutions et opportunités pour investir dans la jeunesse africaine.'
            },
            {
                'title': 'De la Théorie à la Pratique : Appliquer les Concepts MBA dans le Monde Réel',
                'category': 'Entrepreneuriat',
                'excerpt': 'Un MBA enseigne des concepts puissants, mais comment les appliquer concrètement ? Découvrez mes leçons tirées de l\'expérience HEC Paris.',
                'content': '''
                    <h2>Le Fossé entre Théorie et Pratique</h2>
                    <p>Quand j'ai commencé mon MBA à HEC Paris, j'étais enthousiaste d'apprendre tous ces concepts business. Mais rapidement, j'ai réalisé que savoir et faire sont deux choses très différentes.</p>
                    
                    <h2>Les Concepts MBA Essentiels</h2>
                    
                    <h3>1. L'Analyse SWOT</h3>
                    <p><strong>En théorie :</strong> Analysez vos forces, faiblesses, opportunités et menaces.<br>
                    <strong>En pratique :</strong> Soyez brutalement honnête dans votre auto-évaluation. La plupart des entrepreneurs surestiment leurs forces et sous-estiment leurs faiblesses.</p>
                    
                    <h3>2. Le Business Model Canvas</h3>
                    <p><strong>En théorie :</strong> Mappez votre modèle d'affaires sur neuf blocs.<br>
                    <strong>En pratique :</strong> Votre business model évoluera constamment. Mettez-le à jour régulièrement et testez vos hypothèses sur le terrain.</p>
                    
                    <h3>3. La Stratégie Blue Ocean</h3>
                    <p><strong>En théorie :</strong> Créez un nouvel espace de marché sans concurrence.<br>
                    <strong>En pratique :</strong> Les océans vraiment bleus sont rares. Cherchez plutôt des niches mal servies dans des marchés existants.</p>
                    
                    <h2>Les Leçons du Terrain</h2>
                    
                    <h3>Leçon 1 : Les Gens Avant tout</h3>
                    <p>Les cours MBA parlent beaucoup de stratégie et de finance, mais peu de l'importance des relations humaines. Dans la réalité, votre succès dépend de votre capacité à recruter, motiver et retenir les bonnes personnes.</p>
                    
                    <h3>Leçon 2 : L'Exécution > Stratégie</h3>
                    <p>Une stratégie moyenne bien exécutée bat une stratégie brillante mal exécutée. Focalisez-vous sur l'exécution quotidienne.</p>
                    
                    <h3>Leçon 3 : Le Cash est Roi</h3>
                    <p>On nous enseigne la comptabilité, mais beaucoup d'entrepreneurs ne comprennent pas vraiment la gestion de trésorerie. Plus d'entreprises meurent de problèmes de cash que de manque de rentabilité.</p>
                    
                    <h2>Appliquer les Concepts dans MY BARIKA</h2>
                    <p>Avec MY BARIKA, j'ai dû adapter constamment les concepts MBA au contexte africain. Voici comment :</p>
                    
                    <h3>Marketing</h3>
                    <p>Les stratégies marketing occidentales ne fonctionnent pas toujours en Afrique. Nous avons dû créer des approches adaptées aux réalités locales.</p>
                    
                    <h3>Finance</h3>
                    <p>L'accès au financement est différent. Nous avons diversifié nos sources de revenus et créé des partenariats innovants.</p>
                    
                    <h3>Opérations</h3>
                    <p>Les infrastructures limitées nous ont forcés à être créatifs. Chaque contrainte est devenue une opportunité d'innovation.</p>
                    
                    <h2>Conseils pour les Nouveaux Diplômés MBA</h2>
                    <ol>
                        <li>Restez humble - le terrain vous enseignera plus que les livres</li>
                        <li>Construisez votre réseau activement</li>
                        <li>N'ayez pas peur d'échouer - l'échec est le meilleur professeur</li>
                        <li>Adaptez les concepts à votre contexte</li>
                        <li>Continuez à apprendre - votre MBA n'est que le début</li>
                    </ol>
                ''',
                'tags': 'MBA, entrepreneuriat, HEC, business, stratégie',
                'image_url': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1200&q=80',
                'meta_description': 'Comment appliquer concrètement les concepts MBA dans le monde réel. Leçons tirées de l\'expérience HEC Paris et de l\'entrepreneuriat en Afrique.'
            },
            {
                'title': 'Construire une Équipe Performante : Les Clés du Succès',
                'category': 'Leadership',
                'excerpt': 'Une équipe performante ne se construit pas par hasard. Découvrez les principes essentiels pour créer et diriger une équipe exceptionnelle.',
                'content': '''
                    <h2>L'Équipe : Votre Plus Grand Atout</h2>
                    <p>Que ce soit sur un terrain de basket ou dans une salle de conférence, une chose reste constante : aucun succès significatif n'est individuel. Tout repose sur l'équipe.</p>
                    
                    <h2>Les Fondations d'une Équipe Performante</h2>
                    
                    <h3>1. La Vision Partagée</h3>
                    <p>Avant tout, votre équipe doit savoir où elle va. Une vision claire et partagée crée l'alignement et la motivation nécessaires pour surmonter les obstacles.</p>
                    
                    <h3>2. La Confiance Mutuelle</h3>
                    <p>La confiance se construit avec le temps, mais elle peut se détruire en un instant. Soyez transparent, tenez vos engagements et admettez vos erreurs.</p>
                    
                    <h3>3. La Communication Ouverte</h3>
                    <p>Créez un environnement où chacun se sent libre de s'exprimer. Les meilleures idées viennent souvent des endroits les plus inattendus.</p>
                    
                    <h2>Le Recrutement : Tout Commence Là</h2>
                    
                    <h3>Recruter pour les Valeurs</h3>
                    <p>Les compétences s'apprennent, les valeurs non. Recrutez des personnes qui partagent vos valeurs fondamentales, même si elles manquent de certaines compétences techniques.</p>
                    
                    <h3>La Diversité comme Force</h3>
                    <p>Une équipe homogène pense de la même manière. La diversité de perspectives, d'expériences et de backgrounds rend votre équipe plus innovante et résiliente.</p>
                    
                    <h2>Développer Votre Équipe</h2>
                    
                    <h3>Formation Continue</h3>
                    <p>Investissez dans le développement de votre équipe. Les personnes qui grandissent avec l'entreprise sont vos meilleurs atouts.</p>
                    
                    <h3>Feedback Constructif</h3>
                    <p>Donnez du feedback régulièrement, pas seulement lors des évaluations annuelles. Le feedback doit être spécifique, actionnable et délivré avec bienveillance.</p>
                    
                    <h3>Célébrer les Succès</h3>
                    <p>Reconnaissez et célébrez les victoires, grandes et petites. La reconnaissance booste la motivation et renforce la culture d'équipe.</p>
                    
                    <h2>Gérer les Conflits</h2>
                    <p>Les conflits sont inévitables. Ce qui compte, c'est comment vous les gérez :</p>
                    <ul>
                        <li>Adressez les problèmes rapidement</li>
                        <li>Écoutez toutes les parties</li>
                        <li>Focalisez-vous sur le problème, pas sur les personnes</li>
                        <li>Cherchez des solutions gagnant-gagnant</li>
                    </ul>
                    
                    <h2>Le Leadership par l'Exemple</h2>
                    <p>Vous ne pouvez pas demander à votre équipe ce que vous ne faites pas vous-même. Soyez le premier arrivé et le dernier parti. Montrez la voie.</p>
                    
                    <h2>L'Autonomisation</h2>
                    <p>Une fois que vous avez recruté les bonnes personnes et établi la vision, faites-leur confiance. L'autonomie crée l'engagement et libère la créativité.</p>
                    
                    <h2>Conclusion</h2>
                    <p>Construire une équipe performante est un processus continu. Cela demande de l'intention, de l'effort et de la patience. Mais quand vous y arrivez, il n'y a rien de plus gratifiant.</p>
                ''',
                'tags': 'équipe, leadership, management, collaboration, performance',
                'image_url': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1200&q=80',
                'meta_description': 'Guide complet pour construire et diriger une équipe performante. Recrutement, développement, communication et leadership par l\'exemple.'
            },
            {
                'title': 'La Résilience : Comment Rebondir Après l\'Échec',
                'category': 'Développement Personnel',
                'excerpt': 'L\'échec est inévitable, mais il n\'est pas fatal. Apprenez à développer la résilience nécessaire pour transformer vos échecs en tremplins vers le succès.',
                'content': '''
                    <h2>L'Échec : Une Partie Inévitable du Voyage</h2>
                    <p>J'ai raté plus de tirs que je n'en ai réussi. J'ai perdu plus de matchs que j'en ai gagné. J'ai lancé des projets qui ont échoué. Et c'est exactement pour ça que j'ai réussi.</p>
                    
                    <h2>Comprendre l'Échec</h2>
                    
                    <h3>L'Échec N'est Pas une Identité</h3>
                    <p>Vous avez échoué à quelque chose, vous n'êtes pas un échec. Cette distinction est cruciale. L'échec est un événement, pas une personne.</p>
                    
                    <h3>L'Échec Contient des Leçons</h3>
                    <p>Chaque échec est un professeur déguisé. La question n'est pas "Pourquoi cela m'est-il arrivé ?" mais "Qu'est-ce que cela peut m'enseigner ?"</p>
                    
                    <h2>Les Trois Phases de la Résilience</h2>
                    
                    <h3>Phase 1 : L'Acceptation</h3>
                    <p>Vous ne pouvez pas avancer si vous niez la réalité. Acceptez l'échec, ressentez les émotions qui viennent avec, puis décidez consciemment d'aller de l'avant.</p>
                    
                    <h3>Phase 2 : L'Analyse</h3>
                    <p>Qu'est-ce qui s'est passé ? Pourquoi ? Qu'auriez-vous pu faire différemment ? Soyez honnête dans votre analyse, mais pas dur envers vous-même.</p>
                    
                    <h3>Phase 3 : L'Action</h3>
                    <p>La connaissance sans action ne sert à rien. Appliquez ce que vous avez appris et réessayez. C'est dans l'action que la vraie guérison se produit.</p>
                    
                    <h2>Développer Votre Muscle de Résilience</h2>
                    
                    <h3>1. Changez Votre Narrative</h3>
                    <p>L'histoire que vous vous racontez détermine votre réalité. Au lieu de "Je suis nul", dites "Je suis en apprentissage".</p>
                    
                    <h3>2. Entourez-vous Bien</h3>
                    <p>Votre entourage influence votre résilience. Éloignez-vous des personnes toxiques et entourez-vous de gens qui vous soutiennent.</p>
                    
                    <h3>3. Prenez Soin de Vous</h3>
                    <p>La résilience mentale repose sur une base physique solide. Dormez bien, mangez sainement, faites de l'exercice.</p>
                    
                    <h3>4. Pratiquez la Gratitude</h3>
                    <p>Même dans l'échec, il y a des choses pour lesquelles être reconnaissant. La gratitude change votre perspective.</p>
                    
                    <h2>Mon Plus Grand Échec</h2>
                    <blockquote>
                    "La première année après ma carrière de basketteur, j'ai lancé une entreprise qui a complètement échoué. J'avais investi toutes mes économies. J'étais devasté. Mais cet échec m'a enseigné plus sur le business que n'importe quel cours MBA. Il m'a forcé à être humble et à vraiment écouter le marché."
                    </blockquote>
                    
                    <h2>Les Signes d'une Résilience Croissante</h2>
                    <ul>
                        <li>Vous rebondissez plus vite après les coups durs</li>
                        <li>Vous voyez les problèmes comme des opportunités</li>
                        <li>Vous n'avez plus peur de prendre des risques calculés</li>
                        <li>Vous apprenez de vos erreurs au lieu de les répéter</li>
                        <li>Vous restez optimiste face à l'adversité</li>
                    </ul>
                    
                    <h2>Un Message d'Espoir</h2>
                    <p>Si vous lisez ceci après un échec, sachez que vous n'êtes pas seul. Tous ceux qui ont réussi sont passés par là. La différence entre ceux qui réussissent et ceux qui abandonnent, c'est la résilience.</p>
                    
                    <h2>Exercice Pratique</h2>
                    <p>Prenez un papier et écrivez :</p>
                    <ol>
                        <li>Quel échec récent m'affecte ?</li>
                        <li>Qu'est-ce que cet échec m'enseigne ?</li>
                        <li>Quelle est la prochaine action que je peux prendre ?</li>
                    </ol>
                    
                    <h2>Conclusion</h2>
                    <p>L'échec n'est pas l'opposé du succès, c'est une partie du succès. Chaque personne que vous admirez a échoué de nombreuses fois. La résilience est ce qui les a rendus extraordinaires.</p>
                ''',
                'tags': 'résilience, échec, rebondir, développement personnel, mindset',
                'image_url': 'https://images.unsplash.com/photo-1494959764136-6be9eb3c261e?w=1200&q=80',
                'meta_description': 'Comment développer la résilience pour transformer vos échecs en succès. Stratégies pratiques et leçons tirées de l\'expérience personnelle.'
            }
        ]

        # Créer les articles
        self.stdout.write(self.style.SUCCESS('\nCréation des articles...'))
        for idx, article_data in enumerate(articles_data, 1):
            # Créer l'article
            article, created = Article.objects.get_or_create(
                title=article_data['title'],
                defaults={
                    'content': article_data['content'],
                    'excerpt': article_data['excerpt'],
                    'author': 'Mvingalakani Yércia',
                    'category': categories[article_data['category']],
                    'tags': article_data['tags'],
                    'status': 'published',
                    'views': idx * 47,  # Nombre de vues aléatoire
                    'meta_description': article_data['meta_description'],
                }
            )

            if created:
                # Télécharger et sauvegarder l'image
                if article_data.get('image_url'):
                    self.download_and_save_image(article, article_data['image_url'], 'article')
                
                self.stdout.write(self.style.SUCCESS(f'✓ Article "{article.title}" créé'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Article "{article.title}" existe déjà'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Terminé ! 10 articles créés avec succès.'))

    def download_and_save_image(self, instance, image_url, instance_type):
        """Télécharge une image depuis une URL et la sauvegarde"""
        try:
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                # Extraire le nom du fichier depuis l'URL
                filename = f"{instance_type}_{instance.slug}.jpg"
                
                # Créer un fichier Django depuis les bytes
                image_file = BytesIO(response.content)
                django_file = File(image_file, name=filename)
                
                # Sauvegarder l'image
                instance.image.save(filename, django_file, save=True)
                self.stdout.write(self.style.SUCCESS(f'  → Image téléchargée: {filename}'))
            else:
                self.stdout.write(self.style.WARNING(f'  → Erreur téléchargement image: {response.status_code}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  → Erreur: {str(e)}'))