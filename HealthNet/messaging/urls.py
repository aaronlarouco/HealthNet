"""
HealthNet Appointments urls
"""

from django.conf.urls import url
from messaging import views

app_name = 'messaging'  # namespace

urlpatterns = [
    # Url for new message JPop
    url(r'^(?P<username>\w+)/newmessage$', views.newMessage, name='newMessage'),

    # Url for view message JPop
    url(r'^(?P<username>\w+)/viewmessage/(?P<pk>[0-9]+)$', views.viewMessage, name='viewMessage'),

    # Url for a reply
    url(r'^(?P<username>\w+)/reply/(?P<pk>[0-9]+)$', views.replyMessage, name='replyMessage'),

]
