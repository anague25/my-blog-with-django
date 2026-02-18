from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('blogapp.urls')),
]

handler404 = "blogapp.views.custom_404_view"
