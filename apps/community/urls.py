from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('header/', views.header, name='header'),
]