import json

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone

from profiles.models import *
from .forms import *
from .models import *
from log.views import createLogEvent

def newMessage(request, username):
    if request.user.is_authenticated():
        person = request.user.healthnetuser

        if request.method == 'POST':
            message = Message()
            message.sender = person
            message.receiver = Contact.objects.get(pk=request.POST['receiver']).user
            message.body = request.POST['body']
            message.subject = request.POST['subject']
            message.send_date_time = timezone.now()

            message.save()
            createLogEvent(request.user.username, request.user.username, 21, "Message sent")

            return HttpResponse()

        else:
            form = NewMessageForm()
            mimetype = 'application/json'
            people = Contact.objects.filter(relation='se').exclude(user_id=person.id)
            html = render_to_string('messaging/ajax_new_message.html', {'form': form, 'people': people})
            res = {'html': html}
            return HttpResponse(json.dumps(res), mimetype)

def viewMessage(request, username, pk):
    if request.user.is_authenticated():
        person = request.user.healthnetuser
        message = Message.objects.get(pk=pk)
        message.was_read = True
        message.save()
        form = ViewMessageForm(instance=message)
        mimetype = 'application/json'
        html = render_to_string('messaging/ajax_message.html', {'form': form, 'message': message})
        res = {'html': html}
        return HttpResponse(json.dumps(res), mimetype)

def replyMessage(request, username, pk):
    if request.user.is_authenticated():
        person = request.user.healthnetuser
        message_reply = Message.objects.get(pk=pk)

        reply = Message()
        reply.receiver = message_reply.sender
        reply.sender = person
        reply.subject = "Re {0}".format(message_reply.subject)

        if request.method == 'POST':
            reply.body = request.POST['body']
            reply.subject = request.POST['subject']
            reply.send_date_time = timezone.now()

            reply.save()
            createLogEvent(request.user.username, request.user.username, 21, "Message sent")

            return HttpResponse()

        else:
            form = NewMessageForm(instance=reply)
            mimetype = 'application/json'
            html = render_to_string('messaging/ajax_reply.html', {'form': form, 'message': reply})
            res = {'html': html}
            return HttpResponse(json.dumps(res), mimetype)

