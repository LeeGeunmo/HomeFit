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

@login_required(login_url="/user/login/")
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
            
            print(exercises)
    else:
        exercises = Exercise.objects.all()
        
    request.session['exercises'] = [exercise.id for exercise in exercises]
        
    context = {
        'category' : exerciseCategory,
        'exercises' : exercises
    }
    
    return render(request, 'fitness/startExercise.html',context)

@login_required(login_url="/user/login/")
def doExercise(request, exercise_id=None):
    user = request.user
    exercises = Exercise.objects.none()
    exercise = None
    next_exercise = None
    check = False
    
    exercises_ids = request.session.get('exercises', [])
    
    if exercises_ids:
        exercises = Exercise.objects.filter(id__in=exercises_ids)
    print(exercises)
    
    activity_level = user.activity_level
    goal = user.fitness_goal
    
    # 사용자 activity_level에 따라 운동 난이도 필터링
    if activity_level == '0':
        multiplier = 1.0
    elif activity_level == '1-2':
        multiplier = 1.3
    elif activity_level == '3-4':
        multiplier = 1.6
    elif activity_level == '5-7':
        multiplier = 2.0
    else:
        multiplier = 1.0  # 기본값 설정
    
    if goal == 'muscle_gain':
        check = True
        

    # 반복 횟수를 배수로 조정
    adjusted_exercises = []
    for exercise in exercises:
        if (exercise.repetition_count is not None or exercise.set_number is not None):
            adjusted_exercise = exercise
            adjusted_exercise.repetition_count = int(exercise.repetition_count * multiplier)
            if (check):
                adjusted_exercise.set_number = int(exercise.set_number + 1)
            adjusted_exercises.append(adjusted_exercise)
        else:
            adjusted_exercises.append(exercise)
    
    if 'exercises' in request.session:
        del request.session['exercises']
    
    
    if adjusted_exercises:
        if (adjusted_exercises[0].name == "달리기"):
            first_exercise = adjusted_exercises.pop(0)
            adjusted_exercises.append(first_exercise)
            
    print(adjusted_exercises)
        

    context = {
        'exercises': adjusted_exercises,
    }
    

    return render(request, "fitness/doExercise.html", context)

@login_required(login_url="/user/login/")
def saveExerciseSet(request):
    if request.method == "POST":
        exercise_name = request.POST.get("exercise_name")
        set_number = request.POST.get("set_number")
        repetition_count = request.POST.get("repetition_count")
        exercise = get_object_or_404(Exercise, name=exercise_name)
        print(set_number,repetition_count)
        if (int(set_number) != 0 or int(repetition_count) != 0):
            ExerciseSet.objects.create(
            user=request.user,
            exercise=exercise,
            set_number=set_number,
            repetition_count=repetition_count,
            )
            print(request.user, exercise, set_number, repetition_count)
        
            return JsonResponse({"status": "success"})
        
    return JsonResponse({"status": "fail"}, status=400)


def statAll(request):
    user = request.user
    today = timezone.now().date()
    print(today)

# 현재 유저이고 오늘 운동한 ExerciseSet을 필터합니다.
    today_exercise_sets = ExerciseSet.objects.filter(user=user, date__date=today)
    print(today_exercise_sets)

    total_calories = sum(
        es.exercise.calories_burned * es.set_number for es in today_exercise_sets
    )

    context = {
        "today_exercise_sets": today_exercise_sets,
        "total_calories": total_calories,
    }

    return render(request, "fitness/dailyStatistics.html", context)
