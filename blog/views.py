from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from django.views.generic import ListView, DetailView
from .models import Article, Category


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/blog_list.html'
    context_object_name = 'articles'
    paginate_by = 9

    def get_queryset(self):
        queryset = Article.objects.filter(status='published').select_related('category')

        # Recherche multi-mots
        search = self.request.GET.get('search')
        if search:
            words = search.split()  # Sépare par espace
            search_query = Q()
            for word in words:
                search_query |= (
                    Q(title__icontains=word) |
                    Q(excerpt__icontains=word) |
                    Q(tags__icontains=word) |
                    Q(author__icontains=word)
                )
            queryset = queryset.filter(search_query)

        # Filtre par catégorie (slug)
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset.order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        context['category_filter'] = self.request.GET.get('category', '')
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
    
    def get_queryset(self):
        return Article.objects.filter(status='published')
    
    def get_object(self):
        article = super().get_object()
        article.views += 1
        article.save(update_fields=['views'])
        return article


def home(request):
    """Page d'accueil"""
    recent_articles = Article.objects.filter(status='published').order_by('-published_at')[:3]
    categories = Category.objects.all()[:6]
    popular_articles = Article.objects.filter(status='published').order_by('-views')[:3]
    
    context = {
        'recent_articles': recent_articles,
        'categories': categories,
        'popular_articles': popular_articles,
    }
    return render(request, 'blog/home.html', context)


def about(request):
    """Page à propos"""
    return render(request, 'blog/about.html')


def contact(request):
    """Page de contact"""
    # if request.method == 'POST':
    #     # Traitement du formulaire (à implémenter si besoin)
    #     messages.success(request, 'Votre message a été envoyé avec succès !')
    return render(request, 'blog/contact.html')


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category_detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(
            category=self.object,
            status='published'
        ).order_by('-published_at')
        return context
