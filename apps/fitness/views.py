from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth import authenticate, get_user_model
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from .models import ExerciseCategory, Exercise, ExerciseSet
from django.http import JsonResponse
import random
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict


# def main(request):
#     return render(request, 'fitness/main.html')


def selectRoutine(request):
    exerciseCategory = ExerciseCategory.objects.exclude(name="유산소")
    return render(
        request, "fitness/selectRoutine.html", {"categories": exerciseCategory}
    )


def stat(request):
    user = request.user
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)
    two_weeks_ago = now - timedelta(days=14)

    exercise_sets_this_week = ExerciseSet.objects.filter(
        user=user, date__range=[one_week_ago, now]
    )
    exercise_sets_last_week = ExerciseSet.objects.filter(
        user=user, date__range=[two_weeks_ago, one_week_ago]
    )

    exercise_count_this_week = exercise_sets_this_week.count()

    exercise_frequency = defaultdict(int)
    for exercise_set in exercise_sets_this_week:
        exercise_name = exercise_set.exercise.name
        exercise_frequency[exercise_name] += 1
    most_frequent_exercise = max(
        exercise_frequency, key=exercise_frequency.get, default=None
    )

    exercise_count_last_week = exercise_sets_last_week.count()
    exercise_difference = exercise_count_this_week - exercise_count_last_week

    weekday_counts = defaultdict(int)
    for exercise_set in exercise_sets_this_week:
        weekday = exercise_set.date.weekday()  # 월요일=0, 일요일=6
        weekday_counts[weekday] += 1

    context = {
        "exercise_sets": exercise_sets_this_week,
        "exercise_count_this_week": exercise_count_this_week,
        "most_frequent_exercise": most_frequent_exercise,
        "exercise_difference": exercise_difference,
        "weekday_counts": [weekday_counts[i] for i in range(7)],
    }

    return render(request, "fitness/stat.html", context)


@login_required(login_url="/user/login/")
def startExercise(request):
    category_id = request.GET.get("category_id")
    user = request.user
    if category_id:
        exerciseCategory = get_object_or_404(ExerciseCategory, id=category_id)
        exercises = Exercise.objects.filter(category=exerciseCategory)
        if user.fitness_goal == "diet":
            exercises_list = list(exercises)
            running_category = get_object_or_404(ExerciseCategory, name="유산소")
            running = Exercise.objects.filter(category=running_category)
            exercises_list.extend(running)
            exercises = exercises_list

    else:
        exercises = Exercise.objects.all()

    context = {"category": exerciseCategory, "exercises": exercises}

    return render(request, "fitness/startExercise.html", context)


def doExercise(request, category_id=None, exercise_id=None):
    exercises = Exercise.objects.none()
    exercise = None
    next_exercise = None

    if category_id:
        exerciseCategory = get_object_or_404(ExerciseCategory, id=category_id)
        if int(category_id) == 1:
            exercises = Exercise.objects.all()
        else:
            exercises = Exercise.objects.filter(category=exerciseCategory)

        if exercise_id is None:
            exercise = exercises.first()
        else:
            exercise = get_object_or_404(exercises, id=exercise_id)

        next_exercise = (
            exercises.filter(id__gt=exercise.id).first() if exercise else None
        )

    else:
        exercises = Exercise.objects.all()

    context = {
        "category_id": category_id,
        "exercise": exercise,
        "next_exercise": next_exercise,
    }

    return render(request, "fitness/doExercise.html", context)


def saveExerciseSet(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        exercise_id = request.POST.get("exercise_id")
        set_number = request.POST.get("set_number")
        repetition_count = request.POST.get("repetition_count")
        exercises = get_object_or_404(ExerciseCategory, id=category_id)
        exercise = get_object_or_404(exercises, id=exercise_id)
        ExerciseSet.objects.create(
            user=request.user,
            exercise=exercise,
            set_number=set_number,
            repetition_count=repetition_count,
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "fail"}, status=400)


def statAll(request):
    user = request.user
    today = timezone.now().date()
    today_exercise_sets = ExerciseSet.objects.filter(user=user, date__date=today)

    total_calories = sum(
        es.exercise.calories_burned * es.set_number for es in today_exercise_sets
    )

    context = {
        "today_exercise_sets": today_exercise_sets,
        "total_calories": total_calories,
    }

    return render(request, "fitness/dailyStatistics.html", context)
