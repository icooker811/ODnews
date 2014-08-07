from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birth_year = models.CharField(max_length=4, blank=True)