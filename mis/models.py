from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField()
    nptel_status = models.BooleanField()
    mobile_no = models.CharField()
    branch = models.CharField()
    section = models.CharField()


