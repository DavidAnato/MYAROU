from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from blog.models import Article, Category
from .forms import ArticleForm, CategoryForm, HomeSettingsForm, HomeGalleryImageFormSet
from .site_forms import (
    SiteSettingsForm,
    SiteLinkFormSet,
    AboutPageSettingsForm,
    AboutGalleryImageFormSet,
    GalleryPageSettingsForm,
    GalleryPageImageFormSet,
    GALLERY_SECTIONS,
    ContactPageSettingsForm,
    ABOUT_SECTIONS,
    CONTACT_SECTIONS,
    SitePageFormSet,
)
from dashboard.page_block_forms import (
    CustomPageMetaForm,
    CustomPageBlockFormSet,
    CustomPageBlockImageFormSet,
)
from homepage.page_blocks import BLOCK_CATALOG, BLOCK_TYPE_CHOICES
from .form_layout import build_section_layout, SITE_FORM_SECTIONS
from homepage.models import HomeSettings, HomeGalleryImage
import json

from django.urls import NoReverseMatch, reverse

from homepage.models_site import (
    SiteSettings,
    SiteLink,
    AboutPageSettings,
    AboutGalleryImage,
    ContactPageSettings,
    ContactMessage,
    GalleryPageSettings,
    GalleryPageImage,
    SitePage,
    CustomPage,
    CustomPageBlock,
    CustomPageBlockImage,
)
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
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    total_messages = ContactMessage.objects.count()

    context = {
        'total_articles': total_articles,
        'published_articles': published_articles,
        'draft_articles': draft_articles,
        'total_categories': total_categories,
        'recent_articles': recent_articles,
        'popular_articles': popular_articles,
        'categories_stats': categories_stats,
        'recent_count': recent_count,
        'unread_messages': unread_messages,
        'total_messages': total_messages,
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
def home_settings_edit(request):
    home = HomeSettings.get_solo(language_code=getattr(request, 'LANGUAGE_CODE', 'fr'))
    preview_url = f"{reverse('blog:home_dashboard_preview')}?dashboard_preview=1"
    
    if request.method == 'POST':
        form = HomeSettingsForm(request.POST, request.FILES, instance=home)
        formset = HomeGalleryImageFormSet(request.POST, request.FILES, instance=home)
        if form.is_valid() and formset.is_valid():
            instance = form.save(commit=False)
            if request.POST.get('clear_hero_right_image') == '1':
                if instance.hero_right_image:
                    instance.hero_right_image.delete(save=False)
                instance.hero_right_image = None
            if request.POST.get('clear_quote_image') == '1':
                if instance.quote_image:
                    instance.quote_image.delete(save=False)
                instance.quote_image = None
            instance.save()
            formset.save()
            messages.success(request, "Page d'accueil mise à jour avec succès.")
            return redirect('dashboard:home_settings')
    else:
        form = HomeSettingsForm(instance=home)
        formset = HomeGalleryImageFormSet(instance=home)
    
    return render(request, 'dashboard/home_settings_form.html', {'form': form, 'formset': formset, 'preview_url': preview_url})


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def about_settings_edit(request):
    about = AboutPageSettings.get_solo()
    preview_url = f"{reverse('blog:about')}?dashboard_preview=1"

    if request.method == 'POST':
        form = AboutPageSettingsForm(request.POST, request.FILES, instance=about)
        formset = AboutGalleryImageFormSet(request.POST, request.FILES, instance=about)
        if form.is_valid() and formset.is_valid():
            instance = form.save(commit=False)
            if request.POST.get('clear_profile_image') == '1':
                if instance.profile_image:
                    instance.profile_image.delete(save=False)
                instance.profile_image = None
            instance.save()
            formset.save()
            messages.success(request, "Page À propos mise à jour avec succès.")
            return redirect('dashboard:about_settings')
    else:
        form = AboutPageSettingsForm(instance=about)
        formset = AboutGalleryImageFormSet(instance=about)

    return render(request, 'dashboard/page_settings_form.html', {
        'form': form,
        'formset': formset,
        'formset_label': 'Photos galerie (page À propos)',
        'formset_type': 'about',
        'section_layouts': build_section_layout(form, ABOUT_SECTIONS, clear_image_field='profile_image'),
        'page_title': 'Page À propos',
        'preview_url': preview_url,
        'clear_image_field': 'profile_image',
        'gallery_max': 24,
        'page_note': 'Galerie complète : menu « Galerie » (/galerie/). Aperçu accueil : « Page d\'accueil ».',
    })


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def gallery_settings_edit(request):
    gallery = GalleryPageSettings.get_solo()
    preview_url = f"{reverse('blog:gallery')}?dashboard_preview=1"

    if request.method == 'POST':
        form = GalleryPageSettingsForm(request.POST, instance=gallery)
        formset = GalleryPageImageFormSet(request.POST, request.FILES, instance=gallery)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Page Galerie mise à jour avec succès.")
            return redirect('dashboard:gallery_settings')
    else:
        form = GalleryPageSettingsForm(instance=gallery)
        formset = GalleryPageImageFormSet(instance=gallery)

    return render(request, 'dashboard/page_settings_form.html', {
        'form': form,
        'formset': formset,
        'formset_label': 'Photos de la page Galerie (/galerie/)',
        'formset_type': 'gallery',
        'page_note': 'Galerie sur À propos : menu « À propos ». Aperçu accueil (max 4) : « Page d\'accueil ».',
        'section_layouts': build_section_layout(form, GALLERY_SECTIONS),
        'page_title': 'Page Galerie',
        'preview_url': preview_url,
        'gallery_max': 50,
    })


def _site_route_urls_json():
    urls = {}
    for route_name, _label in SiteLink.INTERNAL_ROUTE_CHOICES:
        if not route_name:
            continue
        try:
            urls[route_name] = reverse(route_name)
        except NoReverseMatch:
            continue
    return json.dumps(urls)


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def contact_settings_edit(request):
    from homepage.site_links_defaults import ensure_default_site_links

    ensure_default_site_links()
    contact_page = ContactPageSettings.get_solo()
    site = SiteSettings.get_solo()
    links_queryset = SiteLink.objects.all()
    preview_url = f"{reverse('blog:contact')}?dashboard_preview=1"

    if request.method == 'POST':
        form = ContactPageSettingsForm(request.POST, instance=contact_page)
        site_form = SiteSettingsForm(request.POST, instance=site)
        links_formset = SiteLinkFormSet(request.POST, queryset=links_queryset)
        if form.is_valid() and site_form.is_valid() and links_formset.is_valid():
            form.save()
            site_form.save()
            links_formset.save()
            messages.success(request, "Page Contact, coordonnées et liens mis à jour.")
            return redirect('dashboard:contact_settings')
        if not links_formset.is_valid():
            messages.error(
                request,
                "Liens : vérifiez les URLs (https://…) et corrigez les erreurs dans la section Liens.",
            )
    else:
        form = ContactPageSettingsForm(instance=contact_page)
        site_form = SiteSettingsForm(instance=site)
        links_formset = SiteLinkFormSet(queryset=links_queryset)

    return render(request, 'dashboard/page_settings_form.html', {
        'form': form,
        'site_form': site_form,
        'links_formset': links_formset,
        'links_formset_label': 'Liens du site',
        'site_form_note': "E-mail et adresse affichés sur la page Contact. Les messages du formulaire arrivent dans Messages (menu).",
        'site_section_layouts': build_section_layout(site_form, SITE_FORM_SECTIONS),
        'section_layouts': build_section_layout(form, CONTACT_SECTIONS),
        'page_title': 'Page Contact',
        'preview_url': preview_url,
        'site_route_urls_json': _site_route_urls_json(),
    })


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def contact_message_list(request):
    qs = ContactMessage.objects.all()
    status = request.GET.get('status', '')
    if status == 'unread':
        qs = qs.filter(is_read=False)
    elif status == 'read':
        qs = qs.filter(is_read=True)

    search = request.GET.get('q', '').strip()
    if search:
        qs = qs.filter(
            Q(name__icontains=search)
            | Q(email__icontains=search)
            | Q(subject__icontains=search)
            | Q(message__icontains=search)
        )

    request_type = request.GET.get('type', '')
    if request_type:
        qs = qs.filter(request_type=request_type)

    list_query = request.GET.urlencode()

    context = {
        'messages_list': qs[:200],
        'total_count': ContactMessage.objects.count(),
        'unread_count': ContactMessage.objects.filter(is_read=False).count(),
        'search': search,
        'status': status,
        'request_type': request_type,
        'request_type_choices': ContactMessage.REQUEST_TYPE_CHOICES,
        'list_query': list_query,
        'page_title': 'Messages reçus',
    }
    return render(request, 'dashboard/contact_message_list.html', context)


def _contact_messages_list_redirect(request, extra_query=None):
    """Retour liste en conservant filtres (paramètre next ou query actuelle)."""
    query = (request.POST.get('next') or request.GET.get('next') or extra_query or '').strip()
    base = reverse('dashboard:contact_message_list')
    if query:
        return redirect(f'{base}?{query}')
    return redirect(base)


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def contact_message_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if not msg.is_read:
        msg.is_read = True
        msg.save(update_fields=['is_read'])
    list_query = request.GET.get('next', '').strip()
    return render(request, 'dashboard/contact_message_detail.html', {
        'msg': msg,
        'list_query': list_query,
        'page_title': f'Message — {msg.subject[:50]}',
    })


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
@require_POST
def contact_message_toggle_read(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = not msg.is_read
    msg.save(update_fields=['is_read'])
    if msg.is_read:
        messages.success(request, 'Message marqué comme lu.')
    else:
        messages.success(request, 'Message marqué comme non lu.')
    return _contact_messages_list_redirect(request)


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
@require_POST
def contact_message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.delete()
    messages.success(request, 'Message supprimé.')
    return _contact_messages_list_redirect(request)


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
@require_POST
def contact_message_mark_all_read(request):
    updated = ContactMessage.objects.filter(is_read=False).update(is_read=True)
    messages.success(request, f'{updated} message(s) marqué(s) comme lu(s).')
    return _contact_messages_list_redirect(request)


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def site_page_list(request):
    from homepage.page_defaults import ensure_default_site_pages

    ensure_default_site_pages()
    queryset = SitePage.objects.all()

    if request.method == 'POST':
        formset = SitePageFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Visibilité et ordre des pages mis à jour.')
            return redirect('dashboard:site_page_list')
    else:
        formset = SitePageFormSet(queryset=queryset)

    custom_pages = CustomPage.objects.all()
    return render(request, 'dashboard/site_page_list.html', {
        'formset': formset,
        'custom_pages': custom_pages,
        'page_title': 'Pages du site',
    })


def _build_custom_page_save_mapping(block_formset, image_formset):
    """Retourne les PK créées/mises à jour indexées par préfixe de formulaire Django."""
    blocks = []
    for i, bf in enumerate(block_formset.forms):
        if not bf.cleaned_data or bf.cleaned_data.get('DELETE'):
            continue
        inst = bf.instance
        if not inst.pk:
            continue
        blocks.append({
            'form_prefix': i,
            'id': inst.pk,
            'block_type': inst.block_type,
            'image_url': inst.image.url if inst.image else '',
        })

    images = []
    for i, imgf in enumerate(image_formset.forms):
        if not imgf.cleaned_data or imgf.cleaned_data.get('DELETE'):
            continue
        inst = imgf.instance
        if not inst.pk:
            continue
        images.append({
            'form_prefix': i,
            'id': inst.pk,
            'block_id': inst.block_id,
            'image_url': inst.image.url if inst.image else '',
        })

    return {'blocks': blocks, 'images': images}


def _save_custom_page_builder(request, page, *, publish=False):
    """
    Enregistre meta + blocs + images.
    publish=True met la page en ligne sans toucher aux autres champs via le formulaire.
    """
    image_qs = CustomPageBlockImage.objects.filter(block__page=page).select_related('block')
    post = request.POST.copy()

    if publish:
        post['is_published'] = 'on'
    elif page.pk and 'is_published' not in post:
        post['is_published'] = 'on' if page.is_published else ''

    form = CustomPageMetaForm(post, request.FILES, instance=page)
    block_formset = CustomPageBlockFormSet(request.POST, request.FILES, instance=page)
    image_formset = CustomPageBlockImageFormSet(
        request.POST, request.FILES, queryset=image_qs, prefix='images',
    )

    errors = {}
    if not form.is_valid():
        errors['meta'] = form.errors.get_json_data()
    if not block_formset.is_valid():
        errors['blocks'] = block_formset.errors.get_json_data()
    if not image_formset.is_valid():
        errors['images'] = image_formset.errors.get_json_data()

    if errors:
        return False, page, errors, None

    page = form.save()
    if publish and not page.is_published:
        page.is_published = True
        page.save(update_fields=['is_published', 'updated_at'])

    block_formset.instance = page
    block_formset.save()
    image_formset.save()

    mapping = _build_custom_page_save_mapping(block_formset, image_formset)
    page.refresh_from_db()
    return True, page, None, mapping


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def custom_page_create(request):
    if request.method == 'POST':
        form = CustomPageMetaForm(request.POST)
        if form.is_valid():
            page = form.save()
            messages.success(request, f'Page « {page.title} » créée. Ajoutez des blocs ci-dessous.')
            return redirect('dashboard:custom_page_edit', pk=page.pk)
    else:
        form = CustomPageMetaForm()
    return render(request, 'dashboard/custom_page_builder.html', {
        'form': form,
        'action': 'Créer',
        'page_title': 'Nouvelle page',
        'is_create': True,
    })


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def custom_page_edit(request, pk):
    page = get_object_or_404(CustomPage, pk=pk)
    preview_url = f"{page.get_href()}?dashboard_preview=1"
    image_qs = CustomPageBlockImage.objects.filter(block__page=page).select_related('block')

    if request.method == 'POST':
        ok, page, errors, _mapping = _save_custom_page_builder(request, page)
        if ok:
            messages.success(request, f'Page « {page.title} » enregistrée.')
            return redirect('dashboard:custom_page_edit', pk=page.pk)
        form = CustomPageMetaForm(request.POST, instance=page)
        block_formset = CustomPageBlockFormSet(request.POST, request.FILES, instance=page)
        image_formset = CustomPageBlockImageFormSet(
            request.POST, request.FILES, queryset=image_qs, prefix='images',
        )
        if errors.get('meta'):
            messages.error(request, f'Paramètres : {form.errors.as_text()}')
        if errors.get('blocks'):
            messages.error(request, f'Blocs : {block_formset.errors.as_text()}')
        if errors.get('images'):
            messages.error(request, f'Images : {image_formset.errors.as_text()}')
    else:
        form = CustomPageMetaForm(instance=page)
        block_formset = CustomPageBlockFormSet(instance=page)
        image_formset = CustomPageBlockImageFormSet(queryset=image_qs, prefix='images')

    gallery_images_by_block = {}
    for img_index, img_form in enumerate(image_formset):
        block_id = img_form.instance.block_id
        if block_id:
            gallery_images_by_block.setdefault(block_id, []).append((img_index, img_form))

    return render(request, 'dashboard/custom_page_builder.html', {
        'form': form,
        'block_formset': block_formset,
        'image_formset': image_formset,
        'gallery_images_by_block': gallery_images_by_block,
        'block_type_choices': BLOCK_TYPE_CHOICES,
        'block_catalog': BLOCK_CATALOG,
        'block_catalog_json': json.dumps({item['type']: item for item in BLOCK_CATALOG}, ensure_ascii=False),
        'save_api_url': reverse('dashboard:custom_page_save_api', kwargs={'pk': page.pk}),
        'page': page,
        'page_title': f'Page builder — {page.title}',
        'preview_url': preview_url,
    })


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
@require_POST
def custom_page_save_api(request, pk):
    """Sauvegarde AJAX (auto-save ou publication)."""
    page = get_object_or_404(CustomPage, pk=pk)
    publish = request.POST.get('builder_action') == 'publish'
    ok, page, errors, mapping = _save_custom_page_builder(request, page, publish=publish)

    if not ok:
        return JsonResponse({'ok': False, 'errors': errors}, status=400)

    payload = {
        'ok': True,
        'is_published': page.is_published,
        'preview_url': f"{page.get_href()}?dashboard_preview=1",
        'updated_at': page.updated_at.isoformat(),
        'page_href': page.get_href() if page.is_published else '',
    }
    if mapping:
        payload.update(mapping)
    return JsonResponse(payload)


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
@require_POST
def custom_page_delete(request, pk):
    page = get_object_or_404(CustomPage, pk=pk)
    title = page.title
    page.delete()
    messages.success(request, f'Page « {title} » supprimée.')
    return redirect('dashboard:site_page_list')


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
@require_POST
def delete_block_image_api(request, pk):
    obj = get_object_or_404(CustomPageBlockImage, pk=pk)
    obj.delete()
    return JsonResponse({'ok': True})


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
def site_links_edit(request):
    """Redirection : les liens sont gérés depuis la page Contact."""
    return redirect('dashboard:contact_settings')


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
@require_POST
def delete_site_link_api(request, pk):
    link = get_object_or_404(SiteLink, pk=pk)
    link.delete()
    return JsonResponse({'ok': True})


@login_required(login_url='dashboard:login')
@user_passes_test(is_staff, login_url='dashboard:login')
@require_POST
def delete_gallery_image_api(request, pk):
    model_kind = request.POST.get('model', 'gallery')
    if model_kind == 'about':
        obj = get_object_or_404(AboutGalleryImage, pk=pk)
    elif model_kind == 'home':
        obj = get_object_or_404(HomeGalleryImage, pk=pk)
    else:
        obj = get_object_or_404(GalleryPageImage, pk=pk)
    obj.delete()
    return JsonResponse({'ok': True})


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
