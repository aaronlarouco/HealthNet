
from django import forms

from messaging.models import *


class NewMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('receiver', 'body', 'subject',)
        widgets={
            'subject': forms.TextInput(
                attrs = {
                    'placeholder': 'Subject...',
                    'id': 'message-subject-field',
                    'required': 'true',
                    'pattern': '^[a-zA-Z0-9.\s]*$',
                }),
            'body': forms.Textarea(
                attrs = {
                    'placeholder': 'Message body...',
                    'required': 'true',
                    'id': 'message-body-field',
                }),
        }


class ViewMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('sender', 'subject', 'body')
        widgets={
            'subject': forms.TextInput(
                attrs = {
                    'id': 'message-subject',
                    'readonly': 'true',
                }),
            'body': forms.Textarea(
                attrs = {
                    'readonly': 'true',
                    'id': 'message-body',
                }),
        }