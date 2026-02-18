from django.urls import path
from blogapp import views

app_name = 'blogapp'

urlpatterns = [
path('', views.home_view, name='home'),
path('about/', views.about_view, name='about'),
path('archive/', views.archive_view, name='archive'),
path('authors/', views.authors_view, name='authors'),
path('authors/<str:username>/', views.author_profile_view, name='author_profile'),
path('contact/', views.contact_view, name='contact'),
path('categories/', views.categories_view, name='categories'),
path('search/', views.search_view, name='search'),
path('newsletter/', views.newsletter_view, name='newsletter'),
path('faq/', views.faq_view, name='faq'),
path('privacy/', views.privacy_view, name='privacy'),
path('terms/', views.terms_view, name='terms'),
path('404-preview/', views.not_found_preview_view, name='not_found_preview'),
path('connexion/', views.connexion_view, name='connexion'),
path('register/', views.register_view, name='register'),
path('logout/', views.logout_view, name='logout'),
path('articles/create/', views.create_article_view, name='create_article'),
path('articles/<int:pk>/', views.article_detail_view, name='article_detail'),
path('articles/<int:pk>/update/', views.update_article_view, name='update_article'),
path('articles/<int:id>/delete/', views.delete_article_view, name='delete_article'),
]
