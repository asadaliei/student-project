from django.db import models

# Create your models here.
class StudentDetails(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    registration_number =models.TextField(unique=True)
    class_name = models.TextField()
    course = models.TextField()

class Signup (models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.TextField()
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
