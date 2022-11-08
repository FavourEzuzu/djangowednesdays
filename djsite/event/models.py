from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.


class Venue(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=300)
    zipcode = models.CharField('zip code', max_length=15)
    phone = models.CharField('Phone contact', max_length=15, blank=True)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email Address', blank=True)
    owner = models.IntegerField("Venue Owner", blank=False, default=1)
    venue_image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name


class Clubuser(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email_address = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120, )
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(Clubuser, blank=True, null=True)
    approved = models.BooleanField('Approved', default=False)

    def __str__(self):
        return self.name

    @property
    def Days_till(self):
        today = date.today()
        days_till = self.event_date.date() - today
        days_till_striped = str(days_till).split(",", 1)[0]
        return days_till_striped
