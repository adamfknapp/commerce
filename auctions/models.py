from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

class category(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}"

class listing(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=5000, default="None")
    min_bid = models.IntegerField(default=1)
    time_create = models.DateTimeField(default= datetime.now())
    hours_to_end = models.IntegerField(default=1)
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return f"title: {self.title} | minumum bid: {self.min_bid} | is active: {self.isactive}"


"""
Example model:

from django.db import models

# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"


class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id} : {self.origin} to {self.destination}"


class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"
"""
