from django.urls import path
from blogapp import views

app_name = 'blogapp'

urlpatterns = [
path('', views.home_view, name='home'),
path('connexion/', views.connexion_view, name='connexion'),
path('register/', views.register_view, name='register'),
path('logout/', views.logout_view, name='logout'),
path('articles/create/', views.create_article_view, name='create_article'),
path('articles/<int:pk>/', views.article_detail_view, name='article_detail'),
path('articles/<int:pk>/update/', views.update_article_view, name='update_article'),
path('articles/<int:id>/delete/', views.delete_article_view, name='delete_article'),
]
