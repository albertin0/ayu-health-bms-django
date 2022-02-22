from django.db import models

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=1000)

class Cinema(models.Model):
    name = models.CharField(max_length=100)
    layout_id = models.IntegerField(default=1)

class Time(models.Model):
    movie_id = models.IntegerField(null=False, blank=False)
    cinema_id = models.IntegerField(null=False, blank=False)
    start_dt = models.CharField(max_length=100)
    end_dt = models.CharField(max_length=100)

class Inventory(models.Model):
    time_id = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(default=500)

class Layout(models.Model):
    layout_id = models.IntegerField(null=False, blank=False)
    seat = models.CharField(max_length=10)

class User(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=1000)

BOOKING_STATUS = (
    ('P','Pending'),
    ('C','Confirmed')
)

class Booking(models.Model):
    time_id = models.IntegerField(null=False, blank=False)
    user_id = models.IntegerField(null=False, blank=False)
    status = models.CharField(choices=BOOKING_STATUS, max_length=1)
    seat = models.CharField(max_length=10)