from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from blog.models import Article, Category
from .forms import ArticleForm, CategoryForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST


def is_staff(user):
    return user.is_staff


def dashboard_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard:index')
        else:
            messages.error(request, 'Identifiants invalides ou accès non autorisé.')
    
    return render(request, 'dashboard/login.html')


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def dashboard_logout(request):
    logout(request)
    return redirect('dashboard:login')


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def index(request):
    total_articles = Article.objects.count()
    published_articles = Article.objects.filter(status='published').count()
    draft_articles = Article.objects.filter(status='draft').count()
    total_categories = Category.objects.count()
    
    recent_articles = Article.objects.all()[:5]
    popular_articles = Article.objects.filter(status='published').order_by('-views')[:5]
    
    categories_stats = Category.objects.annotate(
        article_count=Count('articles')
    ).order_by('-article_count')[:5]
    
    week_ago = timezone.now() - timedelta(days=7)
    recent_count = Article.objects.filter(created_at__gte=week_ago).count()
    
    context = {
        'total_articles': total_articles,
        'published_articles': published_articles,
        'draft_articles': draft_articles,
        'total_categories': total_categories,
        'recent_articles': recent_articles,
        'popular_articles': popular_articles,
        'categories_stats': categories_stats,
        'recent_count': recent_count,
    }
    
    return render(request, 'dashboard/index.html', context)


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def article_list(request):
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    category = request.GET.get('category', '')
    
    articles = Article.objects.all()
    
    # Recherche
    if search:
        articles = articles.filter(
            Q(title__icontains=search) | 
            Q(content__icontains=search) |
            Q(tags__icontains=search)
        )
    
    # Filtre statut
    if status:
        articles = articles.filter(status=status)
    
    # Filtre catégorie
    if category:
        articles = articles.filter(category_id=category)
    
    # Tri
    articles = articles.order_by('-created_at')
    
    # Compteurs utiles (exemple dashboard)
    published_count = Article.objects.filter(status="published").count()
    draft_count = Article.objects.filter(status="draft").count()
    
    categories = Category.objects.all()
    
    context = {
        'articles': articles,
        'categories': categories,
        'search': search,
        'status_filter': status,
        'category_filter': category,
        'published_count': published_count,
        'draft_count': draft_count,
    }
    
    return render(request, 'dashboard/article_list.html', context)


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    context = {'article': article}
    return render(request, 'dashboard/article_detail.html', context)


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            messages.success(request, f'Article "{article.title}" créé avec succès.')
            return redirect('dashboard:article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    
    return render(request, 'dashboard/article_form.html', {'form': form, 'action': 'Créer'})


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save()
            messages.success(request, f'Article "{article.title}" modifié avec succès.')
            return redirect('dashboard:article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'dashboard/article_form.html', {'form': form, 'action': 'Modifier', 'article': article})


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
@require_POST
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    title = article.title
    article.delete()
    messages.success(request, f'Article "{title}" supprimé avec succès.')
    return redirect('dashboard:article_list')


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
@require_POST
def article_publish(request, pk):
    article = get_object_or_404(Article, pk=pk)
    
    if article.status == 'published':
        article.status = 'draft'
        article.published_at = None
        messages.info(request, f'Article "{article.title}" mis en brouillon.')
    else:
        article.status = 'published'
        if not article.published_at:
            article.published_at = timezone.now()
        messages.success(request, f'Article "{article.title}" publié avec succès.')
    
    article.save()
    return redirect('dashboard:article_list')


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def category_list(request):
    categories = Category.objects.annotate(
        article_count=Count('articles')
    ).order_by('name')
    
    return render(request, 'dashboard/category_list.html', {'categories': categories})


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Catégorie "{category.name}" créée avec succès.')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'dashboard/category_form.html', {'form': form, 'action': 'Créer'})


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Catégorie "{category.name}" modifiée avec succès.')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'dashboard/category_form.html', {'form': form, 'action': 'Modifier', 'category': category})


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
@require_POST
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    name = category.name
    category.delete()
    messages.success(request, f'Catégorie "{name}" supprimée avec succès.')
    return redirect('dashboard:category_list')


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def stats_api(request):
    status_data = {
        'labels': ['Publiés', 'Brouillons', 'Archivés'],
        'data': [
            Article.objects.filter(status='published').count(),
            Article.objects.filter(status='draft').count(),
            Article.objects.filter(status='archived').count(),
        ]
    }
    
    categories = Category.objects.annotate(
        count=Count('articles', filter=Q(articles__status='published'))
    ).order_by('-count')[:5]
    
    category_data = {
        'labels': [cat.name for cat in categories],
        'data': [cat.count for cat in categories]
    }
    
    return JsonResponse({
        'status': status_data,
        'categories': category_data,
    })

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.text import slugify
from blog.models import Category


@require_http_methods(["POST"])
def category_create_ajax(request):
    """Créer une catégorie via AJAX"""
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Requête invalide'}, status=400)
    
    name = request.POST.get('name', '').strip()
    description = request.POST.get('description', '').strip()
    
    if not name:
        return JsonResponse({'success': False, 'error': 'Le nom est requis'}, status=400)
    
    # Vérifier si la catégorie existe déjà
    if Category.objects.filter(name=name).exists():
        return JsonResponse({'success': False, 'error': 'Cette catégorie existe déjà'}, status=400)
    
    try:
        # Créer la catégorie
        category = Category.objects.create(
            name=name,
            slug=slugify(name),
            description=description
        )
        
        return JsonResponse({
            'success': True,
            'category': {
                'id': category.id,
                'name': category.name,
                'slug': category.slug
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)