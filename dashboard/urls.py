from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.dashboard_login, name='login'),
    path('logout/', views.dashboard_logout, name='logout'),
    
    # Articles
    path('articles/', views.article_list, name='article_list'),
    path('articles/create/', views.article_create, name='article_create'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('articles/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('articles/<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('articles/<int:pk>/publish/', views.article_publish, name='article_publish'),
    
    # Catégories
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('categories/create-ajax/', views.category_create_ajax, name='category_create_ajax'),

    
    # API
    path('api/stats/', views.stats_api, name='stats_api'),
]
