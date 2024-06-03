from django.db import models
from apps.user.models import User
# Create your models here.

class ExerciseCategory(models.Model):
    name = models.CharField(max_length=50)  # 운동 부위 이름 (예: 전신, 가슴, 등, 하체 등)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    category = models.ForeignKey(ExerciseCategory, on_delete=models.CASCADE, related_name='exercises')  # 운동 부위
    name = models.CharField(max_length=100)  # 운동 이름 (예: 벤치프레스, 스쿼트 등)
    calories_burned = models.FloatField()  # 운동으로 소모되는 칼로리
    description = models.TextField(null = True)  # 운동 방법 설명
    set_number = models.IntegerField(null = True)
    repetition_count = models.IntegerField(null = True)
    duration = models.DurationField(null=True, blank=True)  # 운동 시간 (선택 사항)
    image = models.ImageField(upload_to='static/img/fitness', null=True, blank=True)

    def __str__(self):
        return self.name
    
class ExerciseSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    set_number = models.IntegerField()
    repetition_count = models.IntegerField()
