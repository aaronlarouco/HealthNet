"""
HealthNet Appointments models
"""

from django.db import models
from profiles.models import *


class Appointment(models.Model):
    title = models.CharField(max_length=32)
    startDate = models.DateField()
    startTime = models.CharField(max_length=10)
    endDate = models.DateField()
    endTime = models.CharField(max_length=10)
    patient = models.ForeignKey(Patient)
    doctor = models.ForeignKey(Staff)
    hospital = models.ForeignKey(Hospital)
    room = models.CharField(max_length=32)
    reason = models.TextField();
    STATUS_CHOICES = (
        ('P', 'Pending Approval'),
        ('A', 'Approved'),
        ('D', 'Denied'),
        ('C', 'Cancelled'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    notes = models.TextField(null = True);
    case = models.ForeignKey(MedicalCase, null=True)

    def startHours(self):
        splox = self.startTime.split(':')
        splox[0] = int(splox[0])
        if (splox[1][-2:].upper() == 'PM'):
            splox[0] += 12
        if (splox[0] == 12):
            splox[0] = 0
        if (splox[0] == 24):
            splox[0] = 12
        return splox[0]

    def startMinutes(self):
        splox = self.startTime.split(':')
        splox[0] = int(splox[0])
        splox[1] = int(splox[1][:-2])
        return splox[1]

    def endHours(self):
        splox = self.endTime.split(':')
        splox[0] = int(splox[0])
        if (splox[1][-2:].upper() == 'PM'):
            splox[0] += 12
        if (splox[0] == 12):
            splox[0] = 0
        if (splox[0] == 24):
            splox[0] = 12
        return splox[0]

    def endMinutes(self):
        splox = self.endTime.split(':')
        splox[0] = int(splox[0])
        splox[1] = int(splox[1][:-2])
        return splox[1]

    def __str__(self):
        return self.title
