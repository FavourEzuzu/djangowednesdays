from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator  # for pagination
# for pdf files
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Favour"
    month = month.capitalize()
    # convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create a calendar
    cal = HTMLCalendar().formatmonth(year, month_number)
    #  get current year
    now = datetime.now()
    current_year = now.year

    event_list = Event.objects.filter(
        event_date__year=year,
        event_date__month=month_number,
    )

    return render(request, 'events/home.html', {'name': name,
                                                "year": year,
                                                "month": month,
                                                "month_number": month_number,
                                                "cal": cal,
                                                "current_year": current_year,
                                                'event_list': event_list,
                                                })


def all_events(request):
    events_list = Event.objects.all().order_by('-event_date')
    return render(request, 'events/events_list.html',
                  {
                      'events_list': events_list,
                  })


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            # form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_venue.html',
                  {
                      'form': form,
                      'submitted': submitted,
                  })


def add_events(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_events?submitted=True')
        else:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/add_events?submitted=True')
    else:
        # just going to the page, not submitting
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_events.html',
                  {
                      'form': form,
                      'submitted': submitted,
                  })


def list_venues(request):
    # venue_list = Venue.objects.all().order_by('name')
    venue_list = Venue.objects.all()

    # setup pagination
    p = Paginator(Venue.objects.all(), 1)
    page = request.GET.get('page')
    venues = p.get_page(page)

    nums = "a" * venues.paginator.num_pages

    return render(request, 'events/venues.html',
                  {
                      'venue_list': venue_list,
                      'venues': venues,
                      'nums': nums,
                  })


def show_venues(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/show_venue.html',
                  {
                      'venue': venue,
                      'venue_owner': venue_owner,
                  })


def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_venues.html',
                      {
                          'searched': searched,
                          'venues': venues,
                      })
    else:
        return render(request, 'events/search_venues.html',
                      {})


def search_events(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        events = Event.objects.filter(name__contains=searched)
        return render(request, 'events/search_events.html',
                      {
                          'searched': searched,
                          'events': events,
                      })
    else:
        return render(request, 'events/search_events.html',
                      {})


def update_venues(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venue')
    return render(request, 'events/update_venue.html',
                  {
                      'venue': venue,
                      'form': form,
                  })


def update_events(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 'events/update_events.html',
                  {
                      'event': event,
                      'form': form,
                  })


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, "Event Deleted!!")
        return redirect('list-events')
    else:
        messages.success(request, "Only the Manager is allowed to Delete Events!!")
        return redirect('list-events')


def delete_venues(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venue')


# generate text file venue list
def venues_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    # designate the models
    venues = Venue.objects.all()

    # loop through and output
    lines = []

    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.zipcode}\n{venue.phone}\n{venue.web}'
                     f'\n{venue.email_address}\n\n')

    # lines = ["My name is Ezuzu Favour\n",
    #          "I am a Python Programmer and web app developer\n",
    #          "Thank you"]

    # write to text file
    response.writelines(lines)
    return response


def venues_pdf(request):
    # create a bytestream buffer
    buf = io.BytesIO()
    # create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    # add some lines of text
    # lines = [
    #     "Hello",
    #     "I am ",
    #     "Favour",
    # ]

    venues = Venue.objects.all()
    lines = []
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zipcode)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")

    # loop
    for line in lines:
        textob.textLine(line)

    # finish up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    # return something
    return FileResponse(buf, as_attachment=True, filename="venue.pdf")


def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        return render(request, 'events/myevents.html',
                      {
                        'me': me,
                      })
    else:
        messages.success(request, "You are not authorized to view this page")
        return redirect('home')


def admin_approval(request):
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()

    event_list = Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method == "POST":
            id_list = request.POST.getlist('boxes')
            # uncheck all events
            event_list.update(approved=False)
            # update database
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)
            messages.success(request, "Event List Approval has been Updated")
            return redirect('list-events')
        else:
            return render(request, 'events/admin_approval.html',
                          {
                              'event_list': event_list,
                              'event_count': event_count,
                              'venue_count': venue_count,
                              'user_count': user_count,
                          })
    else:
        messages.success(request, "You are not authorized to view this page")
        return redirect('home')