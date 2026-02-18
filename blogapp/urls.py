from django.urls import path
from blogapp import views

app_name = 'blogapp'

urlpatterns = [
path('', views.home_view, name='home'),
path('connexion/', views.connexion_view, name='connexion'),
path('register/', views.register_view, name='register'),
path('logout/', views.logout_view, name='logout'),
]
