"""
HealthNet Profile Forms
"""
from django import forms

from .models import User, Contact, Patient


# This form contains a text field for a username and a password field for a password.
# It is shown on the index page used to login to the system.
class IndexForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': 'Username',
            'password': 'Password',
        }
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'required': 'true',
                    'placeholder': 'username',
                    'id': 'username-field',
                    'pattern': '^[a-zA-z0-9]*$',
                    'minlength': '2',
                    'maxlength': '32',
                    'title': 'Enter only letters and numbers.  Must be between 5 and 32 characters long',
                }),
            'password': forms.PasswordInput(
                attrs={
                    'required': 'true',
                    'placeholder': 'password',
                    'id': 'password-field',
                    'pattern': '^[a-zA-Z0-9-_.!@#$%^&*?:+=]*$',
                    'title': 'Valid password characters are any letter, number or the following: - _ . ! @ # $ % ^ & * ? + ='
                }),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            'firstName', 'middleInitial', 'lastName', 'phoneNumber', 'street', 'city', 'state', 'zipcode', 'relation')
        labels = {
            'firstName': 'First Name',
            'middleInitial': 'M.I.',
            'lastName': 'Last Name',
            'phoneNumber': 'Phone Number',
            'street': 'Street Address',
            'city': 'City',
            'state': 'State',
            'zipcode': 'Zip Code',
            'relation': 'Relationship',
        }

        widgets = {
            'firstName': forms.TextInput(
                attrs={
                    'placeholder': 'ex. John',
                    'required': 'true',
                    'id': 'firstName-field',
                    'pattern': '^[a-zA-Z\s-]*$',
                    'title': 'Name can only be letters',
                    'class': 'jval',
                    'maxlength': '32'
                }),
            'middleInitial': forms.TextInput(
                attrs={
                    'placeholder': 'ex. J',
                    'id': 'middleInitial-field',
                    'pattern': '[A-Za-z-\.]{1,2}',
                    'title': 'Initial must be a single letter',
                    'class': 'jval',
                    'maxlength': '4'
                }),
            'lastName': forms.TextInput(
                attrs={
                    'placeholder': 'ex. Doe',
                    'required': 'true',
                    'id': 'lastName-field',
                    'pattern': '^[a-zA-Z\s-]*$',
                    'title': 'Name can only be letters',
                    'class': 'jval',
                    'maxlength': '32'
                }),
            'phoneNumber': forms.TextInput(
                attrs={
                    'placeholder': 'ex. (123) 456-7890',
                    'required': 'true',
                    'id': 'phoneNumber-field',
                    'pattern': '^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)'
                               '|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9]'
                               '[02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)'
                               '\s*(\d+))?$',
                    'maxlength': '14',
                    'title': 'Enter a valid phone number',
                    'class': 'jval'
                }),
            'street': forms.TextInput(
                attrs={
                    'placeholder': 'ex. 123 Health st. Apt. 1',
                    'required': 'true',
                    'id': 'street-field',
                    'pattern': '^[0-9a-zA-Z\s-.\',]*$',
                    'title': 'Street address must contain letters, numbers, spaces, hyphens, periods, commas, and apostrophes only',
                    'class': 'jval',
                    'maxlength': '32'
                }),
            'city': forms.TextInput(
                attrs={
                    'placeholder': 'ex. Rochester',
                    'required': 'true',
                    'id': 'city-field',
                    'pattern': '^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$',
                    'title': 'Enter a valid city',
                    'class': 'jval',
                    'maxlength': '32'
                }),
            'state': forms.TextInput(
                attrs={
                    'placeholder': 'ex. NY',
                    'required': 'true',
                    'id': 'state-field',
                    'maxlength': '2',
                    'pattern': '^[a-zA-Z][a-zA-Z]$',
                    'title': 'State must be a two letter state abbreviation',
                    'class': 'jval'
                }),
            'zipcode': forms.TextInput(
                attrs={
                    'placeholder': 'ex. 12345',
                    'required': 'true',
                    'id': 'zipcode-field',
                    'pattern': '^\d{5,6}(?:[-\s]\d{4})?$',
                    'title': 'Enter a valid 5 digit zip code',
                    'class': 'jval',
                    'maxlength': '5'
                }),
            'relation': forms.Select(
                attrs={
                    'required': 'true',
                    'id': 'relation-field'
                }),
        }

    def __init__(self, *args, **kwargs):
        no_self = kwargs.pop('no_self', False)
        super(ContactForm, self).__init__(*args, **kwargs)  # You don't need to call .__init__, you
        NEW_RELATION_CHOICES = (                            # just call the class name with (args)
            ('ga', 'Guardian'),
            ('sp', 'Spouse'),
            ('fa', 'Father'),
            ('mo', 'Mother'),
            ('si', 'Sibling'),
            ('ch', 'Child'),
            ('ot', 'Other'),
        )
        if no_self:
            self.fields['relation'].choices = NEW_RELATION_CHOICES


class NewPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('heightFeet', 'heightInches', 'weight', 'insuranceCompany', 'insuranceId',
                  'hospitalPref')
        labels = {
            'birthDate': 'Date of Birth',
            'heightFeet': 'Height Feet',
            'heightInches': 'Height Inches',
            'weight': 'Weight',
            'insuranceCompany': 'Insurance Company',
            'insuranceId': 'Insurance ID',
            'hospitalPref': 'Preferred Hospital',
        }
        widgets = {
            'heightFeet': forms.NumberInput(
                attrs={
                    'placeholder': 'ex. 5',
                    'required': 'true',
                    'id': 'heightFeet-field',
                    'pattern': '^[0-9]*$',
                    'min': '0',
                    'max': '10',
                    'maxlength': '2',
                    'title': 'Enter a valid height in feet, only numerical characters',
                    'class': 'jval'
                }),
            'heightInches': forms.NumberInput(
                attrs={
                    'placeholder': 'ex. 5',
                    'required': 'true',
                    'id': 'heightInches-field',
                    'pattern': '^[0-9]*$',
                    'min': '0',
                    'max': '11',
                    'maxlength': '2',
                    'title': 'Enter a valid height in inches, only numerical characters allowed',
                    'class': 'jval'
                }),
            'weight': forms.NumberInput(
                attrs={
                    'placeholder': 'ex. 150',
                    'required': 'true',
                    'id': 'weight-field',
                    'pattern': '^[0-9]*$',
                    'min': '0',
                    'max': '3000',
                    'maxlength': '3',
                    'title': 'Enter a valid weight, only numerical characters allowed.',
                    'class': 'jval'
                }),
            'insuranceCompany': forms.TextInput(
                attrs={
                    'placeholder': 'ex. Health-Net Co.',
                    'required': 'true',
                    'id': 'insuranceCompany-field',
                    'pattern': '^[a-zA-Z0-9\s-\'.]*$',
                    'title': 'Enter the company name with letters, numbers, spaces, and - \' . only',
                    'class': 'jval'
                }),
            'insuranceId': forms.TextInput(
                attrs={
                    'placeholder': 'ex. 123-456-789',
                    'required': 'true',
                    'id': 'insuranceId-field',
                    'pattern': '^[a-zA-Z0-9-]*$',
                    'title': 'Enter your ID with letters, numbers, and hyphens only',
                    'class': 'jval'
                }),
        }


class UserContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('firstName', 'middleInitial', 'lastName', 'phoneNumber', 'street', 'city', 'state', 'zipcode')
        labels = {
            'firstName': 'First Name',
            'middleInitial': 'M.I.',
            'lastName': 'Last Name',
            'phoneNumber': 'Phone Number',
            'street': 'Street Address',
            'city': 'City',
            'state': 'State',
            'zipcode': 'Zip Code',
        }
        widgets = {
            'firstName': forms.TextInput(
                attrs={
                    'placeholder': 'ex. John',
                    'required': 'true',
                    'id': 'firstName-field',
                    'pattern': '^[a-zA-Z\s-]*$',
                    'title': 'Name can only be letters',
                    'class': 'jval'
                }),
            'middleInitial': forms.TextInput(
                attrs={
                    'placeholder': 'ex. J',
                    'id': 'middleInitial-field',
                    'pattern': '[A-Za-z-\.]{1,2}',
                    'title': 'Initial must be a single letter',
                    'class': 'jval'
                }),
            'lastName': forms.TextInput(
                attrs={
                    'placeholder': 'ex. Doe',
                    'required': 'true',
                    'id': 'lastName-field',
                    'pattern': '^[a-zA-Z\s-]*$',
                    'title': 'Name can only be letters',
                    'class': 'jval'
                }),
            'phoneNumber': forms.TextInput(
                attrs={
                    'placeholder': 'ex. (123) 456-7890',
                    'required': 'true',
                    'id': 'phoneNumber-field',
                    'pattern': '^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)'
                               '|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9]'
                               '[02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)'
                               '\s*(\d+))?$',
                    'maxlength': '14',
                    'title': 'Enter a valid phone number',
                    'class': 'jval'
                }),
            'street': forms.TextInput(
                attrs={
                    'placeholder': 'ex. 123 Health st. Apt. 1',
                    'required': 'true',
                    'id': 'street-field',
                    'pattern': '^[0-9a-zA-Z\s-.\',]*$',
                    'title': 'Street address must contain letters, numbers, spaces, hyphens, periods, commas, and apostrophes only',
                    'class': 'jval'
                }),
            'city': forms.TextInput(
                attrs={
                    'placeholder': 'ex. Rochester',
                    'required': 'true',
                    'id': 'city-field',
                    'pattern': '^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$',
                    'title': 'Enter a valid city',
                    'class': 'jval'
                }),
            'state': forms.TextInput(
                attrs={
                    'placeholder': 'ex. NY',
                    'required': 'true',
                    'id': 'state-field',
                    'maxlength': '2',
                    'pattern': '^[a-zA-Z][a-zA-Z]$',
                    'title': 'State must be a two letter state abbreviation',
                    'class': 'jval'
                }),
            'zipcode': forms.TextInput(
                attrs={
                    'placeholder': 'ex. 12345',
                    'required': 'true',
                    'id': 'zipcode-field',
                    'pattern': '^\d{5,6}(?:[-\s]\d{4})?$',
                    'title': 'Enter a valid 5 digit zip code',
                    'class': 'jval'
                }),
        }


class EditPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['isNew', 'accountType', 'prescriptions', 'user', 'birthDate']
        labels = {
            'heightFeet': 'Height Feet',
            'heightInches': 'Height Inches',
            'weight': 'Weight',
            'insuranceCompany': 'Insurance Company',
            'insuranceId': 'Insurance ID',
            'hospitalPref': 'Preferred Hospital',
        }
        widgets = {
            'heightFeet': forms.NumberInput(
                attrs={
                    'placeholder': 'ex. 5',
                    'required': 'true',
                    'id': 'heightFeet-field',
                    'pattern': '^[0-9]*$',
                    'min': '0',
                    'max': '10',
                    'maxlength': '2',
                    'title': 'Enter a valid height in feet, only numerical characters',
                    'class': 'jval'
                }),
            'heightInches': forms.NumberInput(
                attrs={
                    'placeholder': 'ex. 5',
                    'required': 'true',
                    'id': 'heightInches-field',
                    'pattern': '^[0-9]*$',
                    'min': '0',
                    'max': '11',
                    'maxlength': '2',
                    'title': 'Enter a valid height in inches, only numerical characters allowed',
                    'class': 'jval'
                }),
            'weight': forms.NumberInput(
                attrs={
                    'placeholder': 'ex. 150',
                    'required': 'true',
                    'id': 'weight-field',
                    'pattern': '^[0-9]*$',
                    'min': '0',
                    'max': '3000',
                    'maxlength': '3',
                    'title': 'Enter a valid weight, only numerical characters allowed.',
                    'class': 'jval'
                }),
            'insuranceCompany': forms.TextInput(
                attrs={
                    'placeholder': 'ex. Health-Net Co.',
                    'required': 'true',
                    'id': 'insuranceCompany-field',
                    'pattern': '^[a-zA-Z0-9\s-\'.]*$',
                    'title': 'Enter the company name with letters, numbers, spaces, and - \' . only',
                    'class': 'jval'
                }),
            'insuranceId': forms.TextInput(
                attrs={
                    'placeholder': 'ex. 123-456-789',
                    'required': 'true',
                    'id': 'insuranceId-field',
                    'pattern': '^[a-zA-Z0-9-]*$',
                    'title': 'Enter your ID with letters, numbers, and hyphens only',
                    'class': 'jval'
                }),
        }


class ImageUploadForm(forms.Form):
    image = forms.ImageField(widget=forms.FileInput(attrs={
    'required': 'true',
    'accept': '.png, .jpg, .gif, .bmp, .tif',
    'id': 'profile-picture-input'
    }))

class FileUploadForm(forms.Form):
    theFile = forms.FileField()
