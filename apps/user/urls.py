from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('additional/', views.additional, name='additional'),
    path('additional/fitness_goal', views.additional_fitness_goal, name='additional_fitness_goal'),
    path('additional/activity_level', views.additional_activity_level, name='additional_activity_level'),
    path('mypage', views.mypage, name='mypage'),
]