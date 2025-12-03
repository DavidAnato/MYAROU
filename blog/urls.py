from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.ArticleListView.as_view(), name='article_list'),
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('categorie/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
]
