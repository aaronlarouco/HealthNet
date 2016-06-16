from django.db import models

from profiles.models import HealthNetUser


class Message(models.Model):
    """
    Class to represent a message sent from one user to another.

    @class-variable subject:            Subject line of the message.
    @class-variable body:               Body of the message.
    @class-variable sender:             Sender of the message.
    @class-variable receiver:           Receiver of the message.
    @class-variable send_date_time:     Date the message was sent.
    @class-variable reply:              The reply to this message.
    @class-variable is_draft:           Bool identifying a message as a draft.
    @class-variable was_read:           Bool identifying if a received message was read.
    """

    subject = models.CharField(max_length = 200, null = True, blank = True)
    body = models.TextField()

    sender = models.ForeignKey(HealthNetUser, related_name = 'sender')
    receiver = models.ForeignKey(HealthNetUser, related_name = 'receiver')
    send_date_time = models.DateTimeField()
    reply = models.OneToOneField('self', null = True)
    was_read = models.BooleanField(default = False)

    def preview(self):
        return "{0} ...".format(self.body[0:40])
