from django.contrib import admin
from .models import ExerciseCategory, Exercise

# Register your models here.

admin.site.register(ExerciseCategory)
admin.site.register(Exercise)
