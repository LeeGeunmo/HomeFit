from django.urls import path
from . import views

app_name = 'fitness'

urlpatterns = [
    # path('main/', views.main, name='main'),
    path('selectRoutine/', views.selectRoutine, name='selectRoutine'),
    path('stat/', views.stat, name='stat'),
    path('startExercise/', views.startExercise, name='startExercise'),
    path('doExercise/', views.doExercise, name='doExercise'),
    path('doExercise/<int:exercise_id>/', views.doExercise, name='doExercise_with_id'),
    # path('doExercise/<int:category_id>/<int:exercise_id>', views.doExercise, name='doExercise_with_id'),
    path('dailyStatistics/', views.statAll, name='dailyStatistics'),
    path('saveExerciseSet/', views.saveExerciseSet, name='saveExerciseSet'),
    
]