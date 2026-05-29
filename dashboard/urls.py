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

    # Pages éditables
    path('home/', views.home_settings_edit, name='home_settings'),
    path('about/', views.about_settings_edit, name='about_settings'),
    path('gallery/', views.gallery_settings_edit, name='gallery_settings'),
    path('contact/', views.contact_settings_edit, name='contact_settings'),
    path('pages/', views.site_page_list, name='site_page_list'),
    path('pages/custom/create/', views.custom_page_create, name='custom_page_create'),
    path('pages/custom/<int:pk>/edit/', views.custom_page_edit, name='custom_page_edit'),
    path('pages/custom/<int:pk>/delete/', views.custom_page_delete, name='custom_page_delete'),
    path('messages/', views.contact_message_list, name='contact_message_list'),
    path('messages/<int:pk>/', views.contact_message_detail, name='contact_message_detail'),
    path('messages/<int:pk>/toggle-read/', views.contact_message_toggle_read, name='contact_message_toggle_read'),
    path('messages/<int:pk>/delete/', views.contact_message_delete, name='contact_message_delete'),
    path('messages/mark-all-read/', views.contact_message_mark_all_read, name='contact_message_mark_all_read'),
    path('links/', views.site_links_edit, name='site_links'),
    
    # API
    path('api/stats/', views.stats_api, name='stats_api'),
    path('api/links/<int:pk>/delete/', views.delete_site_link_api, name='delete_site_link'),
    path('api/gallery-image/<int:pk>/delete/', views.delete_gallery_image_api, name='delete_gallery_image'),
    path('api/block-image/<int:pk>/delete/', views.delete_block_image_api, name='delete_block_image'),
]
