from django.urls import path
from . import views

app_name = 'group'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('header/', views.header, name='header'),
    path('add_group/', views.add_group, name='add_group'),
    path('del_group/',views.del_group, name='del_group'),
    path('join_group/', views.join_group, name='join_group'),
    path('leave_group/', views.leave_group, name='leave_group'),
    path('group_members/',views.group_members, name='group_members'),
    path('list_group/',views.list_group, name='list_group'),
    path('find_group/',views.find_group, name='find_group'),
    path('kick_group/',views.kick_group, name='kick_group'),
]