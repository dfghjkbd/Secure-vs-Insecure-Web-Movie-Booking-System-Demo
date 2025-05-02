from django.db import models
from django.db import models
from django.utils import timezone

# Create your models here.from django.db import models

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=15)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.username

# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=100)
    show_time = models.CharField(max_length=100)
    total_seats = models.IntegerField()
    remaining_seats = models.IntegerField()
    price = models.FloatField()

class Booking(models.Model):
    user = models.CharField(max_length=150)  # username as plain text
    movie = models.CharField(max_length=100)  # movie name
    number_of_seats = models.IntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)




class Feedback(models.Model):
    username = models.CharField(max_length=150)
    message = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"
