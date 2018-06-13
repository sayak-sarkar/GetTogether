from django.test import TestCase, Client
from django.shortcuts import resolve_url
from django.utils import timezone

from model_mommy import mommy
import mock
import geocoder
import datetime

from django.contrib.auth.models import User
from events.models import Event, Place, Attendee, UserProfile
# Create your tests here.

def mock_get_geoip(latlng=(0.0, 0.0)):
    def get_geoip(request):
        g = geocoder.ip('8.8.8.8')
        g.latlng = latlng
        return g
    return get_geoip

class EventDisplayTests(TestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    @mock.patch("events.location.get_geoip", mock_get_geoip((0.0, 0.0)))
    def test_events_list(self):
        place = mommy.make(Place, name="Test Place", latitude=0.0, longitude=0.0)
        event = mommy.make(Event, name="Test Event", place=place, start_time=timezone.now() + datetime.timedelta(days=1), end_time=timezone.now() + datetime.timedelta(days=2))
        event.save()

        c = Client()
        response = c.get(resolve_url('all-events'))
        assert(response.status_code == 200)

    @mock.patch("events.location.get_geoip", mock_get_geoip(None))
    def test_events_list_no_geoip(self):
        place = mommy.make(Place, name="Test Place", latitude=0.0, longitude=0.0)
        event = mommy.make(Event, name="Test Event", place=place, start_time=timezone.now() + datetime.timedelta(days=1), end_time=timezone.now() + datetime.timedelta(days=2))
        event.save()

        c = Client()
        response = c.get(resolve_url('all-events'))
        assert(response.status_code == 200)

    def test_show_event(self):
        event = mommy.make(Event)
        event.save()

        event_url = event.get_absolute_url()

        c = Client()
        response = c.get(event_url)
        assert(response.status_code == 200)

    def test_show_event_attendee_without_avatar(self):
        event = mommy.make(Event)
        event.save()

        profile = mommy.make(UserProfile, avatar='')
        profile.save()

        attendee = mommy.make(Attendee, event=event, user=profile, role=Attendee.NORMAL, status= Attendee.YES)
        attendee.save()

        c = Client()
        response = c.get(event.get_absolute_url())
        assert(response.status_code == 200)

