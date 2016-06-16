"""
HealthNet Appointments urls
"""

from django.conf.urls import url

from . import views

app_name = 'appointments'  # namespace

urlpatterns = [
    # The URL to create an appointment
    url(r'^(?P<username>\w+)/createappointment$', views.createAppointment, name='createAppointment'),

    # The URL to view an appointment
    url(r'^(?P<username>\w+)/(?P<pk>[0-9]+)$', views.viewAppointment, name='viewAppointment'),

    # The URL to edit an appointment
    url(r'^(?P<username>\w+)/(?P<pk>[0-9]+)/edit$', views.editAppointment, name='editAppointment'),

    # The URL to cancel an appointment
    url(r'^(?P<username>\w+)/(?P<pk>[0-9]+)/cancel$', views.cancelAppointment, name='cancelAppointment'),

    url(r'^(?P<username>\w+)/updatecases/(?P<pk>[0-9]+)$', views.updateCases, name='updateCases'),

    url(r'^ui$', views.uiTest, name='uiTest'),
]
