# from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    # path converters
    # str, int, uuid, slug, path
    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name='home'),
    path('events', views.all_events, name='list-events'),
    path('add_venue', views.add_venue, name='add-venue'),
    path('add_events', views.add_events, name='add-events'),
    path('list_venues', views.list_venues, name='list-venue'),
    path('show_venues/<venue_id>', views.show_venues, name='show-venue'),
    path('search_venues', views.search_venues, name='search-venues'),
    path('update_venues/<venue_id>', views.update_venues, name='update-venues'),
    path('update_events/<event_id>', views.update_events, name='update-event'),
    path('delete_event/<event_id>', views.delete_event, name='delete-event'),
    path('delete_venues/<venue_id>', views.delete_venues, name='delete-venues'),
    path('venues_text', views.venues_text, name='venues_text'),
    path('venues_pdf', views.venues_pdf, name='venues-pdf'),
    path('my_events', views.my_events, name='my_events'),
    path('search_events', views.search_events, name='search-events'),
    path('admin_approval', views.admin_approval, name='admin_approval'),

]
