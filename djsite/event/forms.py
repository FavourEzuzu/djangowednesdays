from django import forms
from django.forms import ModelForm
from .models import Venue, Event


# create a venue from
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'zipcode', 'phone', 'web', 'email_address', 'venue_image')
        label = {
            'name': '',
            'address': '',
            'zipcode': '',
            'phone': '',
            'web': '',
            'email_address': '',
            'venue_image': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Web Address'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '  Email Address'}),

        }


# Admin superuser event form
class EventFormAdmin(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'manager', 'attendees', 'description')
        label = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'venue': 'Venue',
            'manager': 'Manager',
            'attendees': 'Attendees',
            'description': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
            'venue': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Venue'}),
            'manager': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Manager'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'}),
            'descriptions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'attendees', 'description')
        label = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'venue': 'Venue',
            'attendees': 'Attendees',
            'description': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
            'venue': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Venue'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'}),
            'descriptions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }