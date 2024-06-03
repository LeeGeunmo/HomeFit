from django.shortcuts import render
from apps.fitness.models import ExerciseCategory
# Create your views here.
def home(request):
    exerciseCategory = ExerciseCategory.objects.exclude(name = '유산소')
    return render(request, 'fitness/selectRoutine.html',{'categories': exerciseCategory})
