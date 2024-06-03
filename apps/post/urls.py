from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
   path('main/',views.main, name='main'),
   path('create_post/',views.create_post, name='create_post'),
   path('edit_post/',views.edit_post, name='edit_post'),
   path('delete_post/',views.delete_post, name='delete_post'),
   path('post_list/',views.post_list, name='post_list')
]