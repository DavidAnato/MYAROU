from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import Http404

from django.views.generic import ListView, DetailView
from .models import Article, Category
from homepage.models import HomeSettings
from homepage.models_site import (
    AboutPageSettings,
    ContactPageSettings,
    ContactMessage,
    GalleryPageSettings,
    CustomPage,
)
from homepage.page_visibility import VisiblePageMixin, is_staff_preview, require_visible_page


class ArticleListView(VisiblePageMixin, ListView):
    visible_route_name = 'blog:article_list'
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


class ArticleDetailView(VisiblePageMixin, DetailView):
    visible_route_name = 'blog:article_list'
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
    home_settings = HomeSettings.get_solo(language_code=getattr(request, 'LANGUAGE_CODE', 'fr'))
    
    context = {
        'recent_articles': recent_articles,
        'categories': categories,
        'popular_articles': popular_articles,
        'home': home_settings,
    }
    return render(request, 'blog/home.html', context)


@xframe_options_sameorigin
def home_dashboard_preview(request):
    recent_articles = Article.objects.filter(status='published').order_by('-published_at')[:3]
    categories = Category.objects.all()[:6]
    popular_articles = Article.objects.filter(status='published').order_by('-views')[:3]
    home_settings = HomeSettings.get_solo(language_code=getattr(request, 'LANGUAGE_CODE', 'fr'))
    
    context = {
        'recent_articles': recent_articles,
        'categories': categories,
        'popular_articles': popular_articles,
        'home': home_settings,
    }
    return render(request, 'blog/home.html', context)


@xframe_options_sameorigin
@require_visible_page('blog:about')
def about(request):
    """Page à propos"""
    about_page = AboutPageSettings.get_solo()
    return render(request, 'blog/about.html', {'about': about_page})


@xframe_options_sameorigin
@require_visible_page('blog:gallery')
def gallery(request):
    """Page galerie dédiée (toutes les photos)."""
    gallery_page = GalleryPageSettings.get_solo()
    return render(request, 'blog/gallery.html', {'gallery': gallery_page})


@xframe_options_sameorigin
@require_visible_page('blog:contact')
def contact(request):
    """Page de contact — messages enregistrés dans le dashboard admin."""
    contact_page = ContactPageSettings.get_solo()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        request_type = request.POST.get('request_type', '').strip()
        subject = request.POST.get('subject', '').strip()
        body = request.POST.get('message', '').strip()

        errors = []
        if not name:
            errors.append('Le nom est obligatoire.')
        if not email:
            errors.append("L'e-mail est obligatoire.")
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors.append("L'e-mail n'est pas valide.")
        if not subject:
            errors.append('Le sujet est obligatoire.')
        if not body:
            errors.append('Le message est obligatoire.')

        if errors:
            for err in errors:
                messages.error(request, err)
        else:
            ContactMessage.objects.create(
                name=name,
                email=email,
                request_type=request_type,
                subject=subject,
                message=body,
            )
            messages.success(
                request,
                'Votre message a bien été envoyé. Nous vous répondrons dans les meilleurs délais.',
            )
            return redirect('blog:contact')

    return render(request, 'blog/contact.html', {'contact_page': contact_page})


@xframe_options_sameorigin
def custom_page(request, slug):
    """Page libre créée depuis le dashboard."""
    page = get_object_or_404(CustomPage, slug=slug)
    if not page.is_published and not is_staff_preview(request):
        raise Http404
    language_code = getattr(request, 'LANGUAGE_CODE', 'fr')
    return render(request, 'blog/custom_page.html', {
        'page': page,
        'page_title': page.get_title(language_code),
        'page_content': page.get_content(language_code),
        'page_meta_description': page.get_meta_description(language_code),
    })


class CategoryDetailView(VisiblePageMixin, DetailView):
    visible_route_name = 'blog:article_list'
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
