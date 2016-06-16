"""
HealthNet appointments Forms
"""
from django import forms

from .models import Appointment
from profiles.models import *


class PatientAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('title', 'doctor', 'hospital', 'room', 'reason')
        labels = {
            'title': 'Title',
            'doctor': 'Doctor',
            'hospital': 'Hospital',
            'room': 'Room',
            'reason': 'Reason'
        }
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'ex. Check-up After Surgery',
                    'required': 'true',
                    'id': 'appointment-title-field',
                    'maxlength': '64',
                    'title': 'Max length of 64 characters',
                    'class': 'jval'
                }),
            'room': forms.TextInput(
                attrs={
                    'placeholder': 'ex. 4-b',
                    'required': 'true',
                    'id': 'appointment-room-field',
                    'pattern': '^[a-zA-Z0-9-,\'.\s]*$',
                    'title': 'Only alphanumerical and space - , \' . characters are allowed',
                    'class': 'jval'
                }),
            'reason': forms.Textarea(
                attrs={
                    'required': 'true',
                    'id': 'appointment-reason-field',
                    'class': 'jval',
                    'pattern': '^[a-zA-Z0-9-,\'.\s?\"\(\)%^&$#@!:;/+=*]*$'
                }),
        }


class StaffAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('title', 'patient', 'doctor', 'hospital', 'room', 'reason')
        labels = {
            'title': 'Title',
            'patient': 'Patient',
            'doctor': 'Doctor',
            'hospital': 'Hospital',
            'room': 'Room',
            'reason': 'Reason'
        }
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'ex. Check-up After Surgery',
                    'required': 'true',
                    'id': 'appointment-title-field',
                    'maxlength': '64',
                    'title': 'Max length of 64 characters',
                    'class': 'jval'
                }),
            'room': forms.TextInput(
                attrs={
                    'placeholder': 'ex. 4-b',
                    'required': 'true',
                    'id': 'appointment-room-field',
                    'pattern': '^[a-zA-Z0-9-,\'.\s]*$',
                    'title': 'Only alphanumerical and space - , \' . characters are allowed',
                    'class': 'jval'
                }),
            'reason': forms.Textarea(
                attrs={
                    'required': 'true',
                    'id': 'appointment-reason-field',
                    'class': 'jval',
                    'pattern': '^[a-zA-Z0-9-,\'.\s?\"\(\)%^&$#@!:;/+=*]*$'
                }),
        }
