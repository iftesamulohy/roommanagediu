from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms

# Create your models here.
class Classroom(models.Model):
    title = models.CharField(max_length=50)
    capacity = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(300)])
    image = models.ImageField(upload_to = "images/",null= True)
    def __str__(self):
        return f"{self.title} {self.capacity}"

class bookClassroom(models.Model):
    room = models.ForeignKey(Classroom,on_delete=models.CASCADE, null=True)
    reason = models.CharField(max_length=100, null=True)
    date = models.DateField()
    a_time = models.TimeField()
    d_time = models.TimeField()
    def __str__(self):
        return f"{self.room}"
