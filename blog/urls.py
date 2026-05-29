from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard-preview/home/', views.home_dashboard_preview, name='home_dashboard_preview'),
    path('about/', views.about, name='about'),
    path('galerie/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('pages/<slug:slug>/', views.custom_page, name='custom_page'),
    path('blog/', views.ArticleListView.as_view(), name='article_list'),
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('categorie/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
]
