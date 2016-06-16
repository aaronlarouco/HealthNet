"""
HealthNet Profile Models
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from profiles.helpers import randomFileName, randomPhotoName

'''
Hospital model

model of hospital object for doctors, nurses, and patients to be parented by

instance variables:
    name: name of hospital
    street: street string
    city: city string
    state: 2 character state code
    zipcode: string of zipcode
    phoneNumber: hospital phone number
    numVisits: The number of patient visits to this hospital

'''


class Hospital(models.Model):
    name = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)
    phoneNumber = models.CharField(max_length=10)  # CSIF?
    numVisits = models.IntegerField()

    def __str__(self):
        return self.name


'''
User model

The User model represents the basic information for every Healthnet user.

instance variables:
user: A Django User model for authentication
accountType: THe type of account (patient, doctor, etc.)
isNew: Is this a brand new account that has just been created
shownTutorial: Has the profile tutorial been shown to this user
photo: A profile picture
'''


class HealthNetUser(models.Model):
    ACCOUNT_TYPE_CHOICES = (
        ('P', 'Patient'),
        ('D', 'Doctor'),
        ('A', 'Admin'),
        ('N', 'Nurse'),
    )
    user = models.OneToOneField(User)
    accountType = models.CharField(max_length=1, choices=ACCOUNT_TYPE_CHOICES, default='P')
    isNew = models.BooleanField(default=True)
    shownTutorial = models.BooleanField(default=False)
    photo = models.ImageField(upload_to=randomPhotoName, default="/static/images/profile.png")

    def __str__(self):
        return self.user.username

    @property
    def get_name(self):
        contact = self.contact_set.filter(relation='se')
        return "{0} {1}".format(contact[0].firstName, contact[0].lastName)

    def received_messages(self):
            messages = self.receiver.all()
            return sorted(messages, key=lambda m:  m.send_date_time).reverse()

#
'''
Patient model

The Patient model is a child of User and contains fields specific to a patient.

instance variables:
birthDate: The patient's date of birth
heightFeet: The feet part of a patient's height
heightInches: The inches part of a patient's height
weight: The patient's weight
insuranceCompany: The patient's insurance company
insuranceId: The patient's insurance ID
hospitalPref: The patient's prefered hospital
hospital: The hospital that the patient is currently at (can be null)
numVisits: The number of hospital visits this patient has had
'''

class Patient(HealthNetUser):
    birthDate = models.DateField()
    heightFeet = models.IntegerField()
    heightInches = models.IntegerField()
    weight = models.IntegerField()
    insuranceCompany = models.CharField(max_length=200)
    insuranceId = models.CharField(max_length=200)
    hospitalPref = models.ForeignKey(Hospital, related_name="hospitalPref", null=True, blank=True)
    hospital = models.ForeignKey(Hospital, related_name="hospital", null=True, blank=True)
    numVisits = models.IntegerField(default = 1)


    def __str__(self):
        return self.user.username

fs = FileSystemStorage(location='/media/patient_files')

class PatientFile(models.Model):
    file = models.FileField(upload_to=randomFileName)
    name = models.CharField(max_length=64)
    patient = models.ForeignKey(Patient)

    def __str__(self):
        return self.name


'''
Contact model

The Contact model contains contact information for a person.  Each User has many Contacts.

instance variables:
firstName: A contact's first name
middleInitial: A contact's middle initial
lastName: A contact's last name
phoneNumber: A contact's phone number
street: The street address at which the contact lives
city: The city in which the contact lives
state: The state in which the contact lives
zipcode: The zipcode of the area that the contact lives
relation: The user's relation to this contact
type: The type of contact this is (patient, doctor, emergency, etc.)
user: The user that this contact belongs to
'''


class Contact(models.Model):
    firstName = models.CharField(max_length=32)
    middleInitial = models.CharField(max_length=1, null=True, blank=True)
    lastName = models.CharField(max_length=64)
    phoneNumber = models.CharField(max_length=14)
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)
    RELATION_CHOICES = (
        ('ga', 'Guardian'),
        ('sp', 'Spouse'),
        ('fa', 'Father'),
        ('mo', 'Mother'),
        ('si', 'Sibling'),
        ('ch', 'Child'),
        ('ot', 'Other'),
        ('se', 'Self'),
    )
    relation = models.CharField(max_length=2, choices=RELATION_CHOICES)
    TYPE_CHOICES = (
        ('e', 'Emergency'),
        ('d', 'Doctor'),
        ('n', 'Nurse'),
        ('p', 'Patient'),
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    user = models.ForeignKey(HealthNetUser)

    def __str__(self):
        return self.firstName

'''
Staff model

The Staff model is a child of HealthNetUser.  Any staff using the system
(doctor, nurse, admin) has a staff object associated with them.

instance variables:
hospital: The hospital that the staff member is currently working at
bio: A short biography describing the staff member
'''

class Staff(HealthNetUser):
    hospital = models.ForeignKey(Hospital)
    bio = models.TextField(null=True)

'''
Illness model

The Illness model represents any sickness/disease that a patient can have

instance variables:
name: The common name of the illness
illnessId: The ID of the illness (used for the API) (If its hooked up...)
symptoms: A list of symptoms associated with this illness
'''

class Illness(models.Model):
    name = models.CharField(max_length=128)
    illnessId = models.CharField(max_length=64)
    symptoms = models.TextField()

    def __str__(self):
        return self.name

'''
Drug model

The Drug model represents a drug that can be prescribed by the hospital

instance variables:
name: The common name of the drug
drugId: The ID of the drug (used for the API) (If its hooked up...)
usage: The description of use (ie. 200mg twice a day)
sideEffects: A list of side effects associated with the drug
illnesses: A list of illnesses that this drug treats
'''

class Drug(models.Model):
    name = models.CharField(max_length=128)
    drugId = models.CharField(max_length=64)
    usage = models.TextField()
    sideEffects = models.TextField()
    illnesses = models.ManyToManyField(Illness)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    drug = models.ForeignKey(Drug)
    startDate = models.DateField()
    refills = models.IntegerField()
    dose = models.TextField()
    pharmacy = models.CharField(max_length=64)
    patient = models.ForeignKey(Patient)
    doctor = models.ForeignKey(Staff)

    def __str__(self):
        return self.drug.name

class MedicalCase(models.Model):
    title = models.CharField(max_length=64)
    caseId = models.CharField(max_length=64)
    date = models.DateField()
    notes = models.TextField(null=True, blank=True)
    ongoing = models.BooleanField(default=True)
    patient = models.ForeignKey(Patient)
    illness = models.ForeignKey(Illness)
    prescriptions = models.ManyToManyField(Prescription, blank=True)
    files = models.ManyToManyField(PatientFile, blank=True)

    def __str__(self):
        return self.caseId
