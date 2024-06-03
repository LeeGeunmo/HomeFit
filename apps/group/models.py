from django.conf import settings
from django.db import models
from ..user.models import User

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User)