from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    join_date = models.DateTimeField(default=timezone.now)
    height = models.FloatField(null=True, blank=True)  # 키 (예: cm)
    weight = models.FloatField(null=True, blank=True)  # 몸무게 (예: kg)
    age = models.PositiveIntegerField(null=True, blank=True)  # 나이
    gender = models.CharField(
        max_length=10, 
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], 
        null=True, 
        blank=True
    )  # 성별
    fitness_goal = models.CharField(
        max_length=20,
        choices=[('muscle_gain', '근성장'), ('diet', '다이어트'), ('bulk_up', '벌크업')],
        null=True,
        blank=True
    )
    activity_level = models.CharField(
        max_length=20,
        choices=[('0', '주 0회'), ('1-2', '주 1-2회'), ('3-4', '주 3-4회'), ('5-7', '주 5-7회')],
        null=True,
        blank=True
    )
