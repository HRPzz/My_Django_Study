from django.db import models

# Create your models here.
class Student(models.Model):
    student_id = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=30)
    age = models.IntegerField()