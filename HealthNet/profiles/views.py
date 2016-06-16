"""
HealthNet Profile Views
"""
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.context_processors import csrf
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from .validate import *
from .forms import *
from .models import *
from log.views import createLogEvent
from appointments.models import *
import json
import operator
from io import StringIO
import os, mimetypes, urllib
from django_downloadview import ObjectDownloadView

from messaging.forms import *

from profiles.helpers import randomFileName

# The index view simply renders the index.html template with a blank login form.
def index(request):
    form = IndexForm()

    if request.method == 'POST':
        message = request.POST['error_message']
        return render(request, 'profiles/index.html', {'form': form, 'error_message': message})
    else:
        return render(request, 'profiles/index.html', {'form': form})


def register(request):
    if request.method == 'POST':
        authUser = User()

        try:
            authUser.username = validateUser(request.POST['username'])
        except InvalidInput as ii:
            messages.add_message(request, messages.INFO, ii.args[0])
            createLogEvent("n/a", "view: register", 1, "Tried to register with an existing username")
            return HttpResponseRedirect("/")

        try:
            authUser.email = validateEmail(request.POST['email'])
        except InvalidInput as ii:
            messages.add_message(request, messages.INFO, ii.args[0])
            createLogEvent("n/a", "view: register", 1, "Given email failed validation")
            return HttpResponseRedirect("/")

        try:
            authUser.set_password(validatePass(request.POST['password']))
        except InvalidInput as ii:
            messages.add_message(request, messages.INFO, ii.args[0])
            createLogEvent("n/a", "view: register", 1, "Given password failed validation")
            return HttpResponseRedirect("/")

        authUser.first_name = ""
        authUser.last_name = ""
        authUser.is_active = True
        authUser.is_staff = False
        authUser.is_superuser = False
        authUser.save()

        newUser = Patient()
        newUser.user = authUser
        newUser.isNew = True
        newUser.accountType = 'P'
        newUser.birthDate = "1993-08-21"
        newUser.heightFeet = 5
        newUser.heightInches = 11
        newUser.weight = 150
        newUser.insuranceCompany = ""
        newUser.insuranceId = ""
        newUser.hospitalPref = None

        newUser.hospital = None
        newUser.numVisits = 0
        newUser.save()

        createLogEvent(request.POST['username'], "view: register", 0, "Successful registration")

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        auth_login(request, user)

        patientForm = NewPatientForm()
        contactForm = UserContactForm()
        hospitals = Hospital.objects.all()
        return render(request, 'profiles/newpatient.html', {'username': request.POST['username'],
        'patientForm': patientForm, 'contactForm': contactForm, 'hospitals': hospitals})


# The login view takes the form data from the index view and uses it to authenticate
# and log in a user.
def login(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        # The password verified for the user
        if user.check_password(request.POST['password']):
            if user.is_active:
                auth_login(request, user)

                createLogEvent(request.POST['username'], "view: login", 2, "Successful login")

                user = User.objects.get(username=request.user.username).healthnetuser
                if user.accountType == 'P':
                    if user.isNew:
                        patientForm = NewPatientForm()
                        contactForm = UserContactForm()
                        hospitals = Hospital.objects.all()
                        return render(request, 'profiles/newpatient.html',
                                      {'username': request.POST['username'], 'patientForm': patientForm,
                                       'contactForm': contactForm, 'hospitals': hospitals})
                    else:
                        return HttpResponseRedirect("/profiles/" + request.POST['username'])
                else:
                    return HttpResponseRedirect("/profiles/" + request.POST['username'])
            else:
                message = "This account has been disabled."
                messages.add_message(request, messages.INFO, message)
                createLogEvent(request.POST['username'], "view: login", 3,
                               "The account trying to be accessed has been disabled")
                return HttpResponseRedirect("/")
        else:
            message = "Incorrect password..."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.POST['username'], "view: login", 3, "Input wrong password for the given account")
            return HttpResponseRedirect("/")
    else:
        # The authentication system was unable to verify the username and password
        message = "Username and/or password not recognized!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent(request.POST['username'], "view: login", 3, "Given credentials not recognized by system")
        return HttpResponseRedirect("/")


def logout(request):
    createLogEvent(request.user.username, "view: logout", 4, "User logged out")
    auth_logout(request)
    message = "Successfully logged out!"
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect("/")


# The viewProfile view obtains the user by userName and displays that user's information.
def viewProfile(request, username):
    if request.user.is_authenticated():
        if request.user.username == username:
            hnuser = User.objects.get(username=username).healthnetuser

            if hnuser.accountType == 'P':
                hnuser = hnuser.patient

                appointments = Appointment.objects.filter(patient=hnuser)
                json_ar = calendarArraySetup(appointments)

                if request.method == 'POST':

                    contact = Contact()
                    contact.street = request.POST['street']
                    contact.city = request.POST['city']
                    contact.state = request.POST['state']
                    contact.zipcode = request.POST['zipcode']
                    contact.firstName = request.POST['firstName']
                    contact.lastName = request.POST['lastName']
                    contact.middleInitial = request.POST['middleInitial']
                    contact.phoneNumber = request.POST['phoneNumber']
                    contact.relation = 'se'
                    contact.healthnetuser = hnuser
                    contact.user_id = hnuser.pk
                    contact.type = 'p'

                    hnuser.birthDate = request.POST['birthDate']
                    hnuser.heightFeet = request.POST['heightFeet']
                    hnuser.heightInches = request.POST['heightInches']
                    hnuser.weight = request.POST['weight']
                    hnuser.insuranceCompany = request.POST['insuranceCompany']
                    hnuser.insuranceId = request.POST['insuranceId']
                    hnuser.hospitalPref = Hospital.objects.get(pk=int(request.POST["hospitalPref"]))
                    hnuser.isNew = False

                    contact.save()
                    hnuser.save()

                    createLogEvent(request.user.username, username, 10, "User profile information was edited")

                    return HttpResponseRedirect("/profiles/" + username)
                else:
                    createLogEvent(request.user.username, username, 5, "User viewed a profile")
                    try:
                        contacts = Contact.objects.filter(user_id=hnuser.id).exclude(relation='se')
                        thiscontact = Contact.objects.get(relation='se', user_id=hnuser.id)

                    except (KeyError, Contact.DoesNotExist):
                        message = "Account not created properly.  Create a new account."
                        messages.add_message(request, messages.INFO, message)
                        return HttpResponseRedirect("/")
                    else:
                        # TODO: Edit this spagetti... It needs some meat sauce.
                        received_messages = hnuser.receiver.all()
                        received_messages = sorted(received_messages, key=lambda m:  m.send_date_time)
                        received_messages.reverse()
                        profilePicForm = ImageUploadForm()
                        prescriptions = Prescription.objects.filter(patient=hnuser)
                        cases = MedicalCase.objects.filter(patient=hnuser)
                        return render(request, 'profiles/profile_patient.html',
                                      {'hnuser': hnuser, 'contacts': contacts, 'json_ar': json_ar,
                                       'thiscontact': thiscontact, 'profilePicForm': profilePicForm,
                                       'received_messages': received_messages, 'prescriptions': prescriptions,
                                       'cases': cases})
            elif hnuser.accountType == 'D':
                hnuser = hnuser.staff

                appointments = Appointment.objects.filter(doctor=hnuser)
                json_ar = calendarArraySetup(appointments)

                createLogEvent(request.user.username, username, 5, "User viewed a profile")
                try:
                    contacts = Contact.objects.filter(user_id=hnuser.id).exclude(relation='se')
                    thiscontact = Contact.objects.get(relation='se', user_id=hnuser.id)

                except (KeyError, Contact.DoesNotExist):
                    message = "Account not created properly.  Create a new account."
                    messages.add_message(request, messages.INFO, message)
                    return HttpResponseRedirect("/")
                else:
                    received_messages = hnuser.receiver.all()
                    received_messages = sorted(received_messages, key=lambda m:  m.send_date_time)
                    received_messages.reverse()
                    profilePicForm = ImageUploadForm()
                    return render(request, 'profiles/profile_doctor.html',
                                  {'hnuser': hnuser, 'contacts': contacts, 'json_ar': json_ar,
                                   'thiscontact': thiscontact, 'profilePicForm': profilePicForm,
                                   'received_messages': received_messages})
            elif (hnuser.accountType == 'N'):
                hnuser = hnuser.staff

                appointments = Appointment.objects.filter(doctor=hnuser)
                json_ar = calendarArraySetup(appointments)

                createLogEvent(request.user.username, username, 5, "User viewed a profile")
                try:
                    contacts = Contact.objects.filter(user_id=hnuser.id).exclude(relation='se')
                    thiscontact = Contact.objects.get(relation='se', user_id=hnuser.id)

                except (KeyError, Contact.DoesNotExist):
                    message = "Account not created properly.  Create a new account."
                    messages.add_message(request, messages.INFO, message)
                    return HttpResponseRedirect("/")
                else:
                    received_messages = hnuser.receiver.all()
                    received_messages = sorted(received_messages, key=lambda m:  m.send_date_time)
                    received_messages.reverse()
                    profilePicForm = ImageUploadForm()
                    return render(request, 'profiles/profile_nurse.html',
                                  {'hnuser': hnuser, 'contacts': contacts, 'json_ar': json_ar,
                                   'thiscontact': thiscontact, 'profilePicForm': profilePicForm,
                                   'received_messages': received_messages})
            elif (hnuser.accountType == 'A'):
                createLogEvent(request.user.username, username, 5, "User viewed a profile")
                try:
                    contacts = Contact.objects.filter(user_id=hnuser.id).exclude(relation='se')
                    thiscontact = Contact.objects.get(relation='se', user_id=hnuser.id)
                except (KeyError, Contact.DoesNotExist):
                    message = "Account not created properly.  Create a new account."
                    messages.add_message(request, messages.INFO, message)
                    return HttpResponseRedirect("/")
                else:
                    return render(request, 'profiles/profile_admin.html',
                                  {'hnuser': hnuser, 'contacts': contacts,
                                   'thiscontact': thiscontact})
        else:
            message = "You do not have permission to view the requested page."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 11, "User attempted to view a profile without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 11, "Someone attempted to view a profile without being logged in")
        return HttpResponseRedirect("/")


def endTut(request, username):
    if request.user.is_authenticated():
        if request.user.username == username:
            hnuser = User.objects.get(username=username).healthnetuser
            hnuser.shownTutorial = True
            hnuser.save()

            return HttpResponse("User is no longer new");
        else:
            message = "You do not have permission to view the requested page."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 20,
                           "Someone attempted to end the tutorial on someone else\'s profile without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 11, "Someone attempted to view a profile without being logged in")
        return HttpResponseRedirect("/")

def fileUpload(request, username):
    if request.user.is_authenticated():
        if (request.user.username == username or request.user.healthnetuser.accountType != 'P'):
            user = User.objects.get(username=username).healthnetuser

            if request.method == 'POST':
                pFile = PatientFile()
                pFile.name = request.POST['filename']
                pFile.file = request.FILES['file']
                pFile.patient = user.patient
                pFile.save()

                files = PatientFile.objects.filter(patient=user)

                mimetype = 'application/json'
                html = render_to_string('profiles/ajax_patientfiles.html', {'hnuser': user.patient, 'files': files})
                res = {'html': html}
                return HttpResponse(json.dumps(res), mimetype)
        else:
            message = "You do not have permission to view the requested page."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 20,
            "Someone attempted to upload a picture to someone else\'s profile without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 11, "Someone attempted to view a profile without being logged in")
        return HttpResponseRedirect("/")

default_file_view = ObjectDownloadView.as_view(model=PatientFile, basename_field='name')

def uploadPic(request, username):
    if request.user.is_authenticated():
        if (request.user.username == username or request.user.healthnetuser.accountType != 'P'):
            user = User.objects.get(username=username).healthnetuser

            if request.method == 'POST':
                form = ImageUploadForm(request.POST, request.FILES)
                if form.is_valid():
                    user.photo = request.FILES['image']
                    user.save()
                    return HttpResponseRedirect('/profiles/' + request.user.username)
            else:
                form = ImageUploadForm()
                return render(request, 'profiles/uploadpicture.html',
                              {'form': form, 'username': username, 'hnuser': user})
        else:
            message = "You do not have permission to view the requested page."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 20,
            "Someone attempted to upload a picture to someone else\'s profile without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 11, "Someone attempted to view a profile without being logged in")
        return HttpResponseRedirect("/")

def ajaxUploadPic(request, username):
    if request.user.is_authenticated():
        if (request.user.username == username or request.user.healthnetuser.accountType != 'P'):
            user = User.objects.get(username=username).healthnetuser

            if request.method == 'POST':
                form = ImageUploadForm(request.POST, request.FILES)
                if form.is_valid():
                    user.photo = request.FILES['image']
                    user.save()

                    mimetype = 'application/json'
                    html = render_to_string('profiles/ajax_profilepicture.html', {'hnuser': user})
                    res = {'html': html}
                    return HttpResponse(json.dumps(res), mimetype)
        else:
            message = "You do not have permission to view the requested page."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 20,
            "Someone attempted to upload a picture to someone else\'s profile without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 11, "Someone attempted to view a profile without being logged in")
        return HttpResponseRedirect("/")


def peekView(request, username):
    if request.user.is_authenticated():
        hnuser = User.objects.get(username=username).healthnetuser
        currentUser = User.objects.get(username=request.user.username).healthnetuser

        format = 'json'
        mimetype = 'application/json'
        html = None

        thiscontact = Contact.objects.get(pk=request.POST["pk"])
        hnuser = thiscontact.user

        if (hnuser.accountType == 'P'):
            hnuser = hnuser.patient
            profilePicForm = ImageUploadForm()
            contacts = Contact.objects.filter(user_id=hnuser.id).exclude(relation='se')
            files = PatientFile.objects.filter(patient=hnuser)
            prescriptions = Prescription.objects.filter(patient=hnuser).order_by('-startDate')
            cases = MedicalCase.objects.filter(patient=hnuser).order_by('-date')

            html = render_to_string('profiles/peek_patient.html', {'hnuser': hnuser,
            'thiscontact': thiscontact, 'profilePicForm': profilePicForm,
            'contacts': contacts, 'files': files, 'prescriptions': prescriptions,
            'cases': cases, 'currentUser': currentUser})
        elif (hnuser.accountType == 'D'):
            hnuser = hnuser.staff
            html = render_to_string('profiles/peek_doctor.html', {'hnuser': hnuser,
            'thiscontact': thiscontact, 'currentUser': currentUser})
        elif (hnuser.accountType == 'N'):
            hnuser = hnuser.staff
            html = render_to_string('profiles/peek_nurse.html', {'hnuser': hnuser,
            'thiscontact': thiscontact, 'currentUser': currentUser})

        res = {'html': html}
        return HttpResponse(json.dumps(res), mimetype)
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 11, "Someone attempted to peek a profile without being logged in")
        return HttpResponseRedirect("/")

def searchView(request, username):
    if request.user.is_authenticated():
        if request.user.username == username:
            if request.method == 'POST':
                format = 'json'
                mimetype = 'application/json'

                hnuser = User.objects.get(username=username).healthnetuser
                if (hnuser.accountType == 'P'):
                    results = Contact.objects.filter(
                        Q(firstName__icontains=request.POST["text"], relation='se') |
                        Q(lastName__icontains=request.POST["text"], relation='se'))
                    results = results.exclude(type='p')

                elif ((hnuser.accountType == 'D') or (hnuser.accountType == 'N')):

                    results = Contact.objects.filter(
                        Q(firstName__icontains=request.POST["text"], relation='se') |
                        Q(lastName__icontains=request.POST["text"], relation='se'))

                html = render_to_string('profiles/ajax_searchresults.html', {'results': results})
                res = {'html': html}
                return HttpResponse(json.dumps(res), mimetype)
        else:
            message = "You do not have permission to view the requested page."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 20,
            "Someone attempted to search on behalf of another profile without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 11, "Someone attempted to search without being logged in")
        return HttpResponseRedirect("/")

def editBasicInfo(request, username):
    if request.user.is_authenticated():
        if (request.user.username == username or request.user.healthnetuser.accountType != 'P'):
            if request.method == 'POST':
                format = 'json'
                mimetype = 'application/json'

                hnuser = User.objects.get(username=username).healthnetuser
                user = hnuser.patient
                contact = Contact.objects.get(user=hnuser, relation='se')

                userForm = NewPatientForm(instance=user)
                contactForm = UserContactForm(instance=contact)

                html = render_to_string('profiles/ajax_basicinfoforms.html', {'userForm': userForm, 'contactForm': contactForm})
                res = {'html': html}
                return HttpResponse(json.dumps(res), mimetype)
        else:
            message = "You do not have permission to view the requested page."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 12,
            "User attempted to edit a patient's basic info without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 12, "Someone attempted to edit a patient's information without being logged in")
        return HttpResponseRedirect("/")

def saveBasicInfo(request, username):
    if request.user.is_authenticated():
        if request.user.username == username or request.user.healthnetuser.accountType != 'P':
            if request.method == 'POST':
                format = 'json'
                mimetype = 'application/json'

                hnuser = User.objects.get(username=username).healthnetuser
                user = hnuser.patient
                contact = Contact.objects.get(user=hnuser, relation='se')

                user.heightFeet = request.POST["heightFeet"]
                user.heightInches = request.POST["heightInches"]
                user.weight = request.POST["weight"]

                contact.phoneNumber = request.POST["phoneNumber"]
                contact.street = request.POST["street"]
                contact.city = request.POST["city"]
                contact.state = request.POST["state"]
                contact.zipcode = request.POST["zipcode"]

                user.save()
                contact.save()

                html = render_to_string('profiles/ajax_basicinfo.html', {'hnuser': user, 'thiscontact': contact})
                res = {'html': html}
                return HttpResponse(json.dumps(res), mimetype)
        else:
            message = "You do not have permission to view the requested page."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 12,
            "Someone attempted to edit a patient's basic info without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 12, "Someone attempted to edit a patient's information without being logged in")
        return HttpResponseRedirect("/")

def editMedicalInfo(request, username):
    if request.user.is_authenticated():
        if request.user.username == username or request.user.healthnetuser.accountType != 'P':
            if request.method == 'POST':
                format = 'json'
                mimetype = 'application/json'

                hnuser = User.objects.get(username=username).healthnetuser
                user = hnuser.patient

                userForm = NewPatientForm(instance=user)
                hospitals = Hospital.objects.all()

                html = render_to_string('profiles/ajax_medicalinfoforms.html', {'userForm': userForm,
                'hospitals': hospitals, 'hnuser': user})
                res = {'html': html}
                return HttpResponse(json.dumps(res), mimetype)
        else:
            message = "You do not have permission to view the requested page."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 12,
            "Someone attempted to edit a patient's medical info without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 12, "Someone attempted to edit a patient's information without being logged in")
        return HttpResponseRedirect("/")

def saveMedicalInfo(request, username):
    if request.user.is_authenticated():
        if request.user.username == username or request.user.healthnetuser.accountType != 'P':
            if request.method == 'POST':
                format = 'json'
                mimetype = 'application/json'

                hnuser = User.objects.get(username=username).healthnetuser
                user = hnuser.patient

                user.insuranceCompany = request.POST["insuranceCompany"]
                user.insuranceId = request.POST["insuranceId"]
                user.hospitalPref = Hospital.objects.get(pk=int(request.POST["hospitalPref"]))

                user.save()

                html = render_to_string('profiles/ajax_medicalinfo.html', {'hnuser': user})
                res = {'html': html}
                return HttpResponse(json.dumps(res), mimetype)
        else:
            message = "You do not have permission to view the requested page."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 12,
            "Someone attempted to edit a patient's medical info without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 12, "Someone attempted to edit a patient's information without being logged in")
        return HttpResponseRedirect("/")

# The addContact view presents a form to fill in that adds a new contact to the user.
def addContact(request, username):
    if request.user.is_authenticated():
        if request.user.username == username:
            if request.method == 'POST':
                format = 'json'
                mimetype = 'application/json'

                hnuser = User.objects.get(username=request.user.username).healthnetuser

                contact = Contact()
                contact.street = request.POST['street']
                contact.city = request.POST['city']
                contact.state = request.POST['state']
                contact.zipcode = request.POST['zipcode']
                contact.firstName = request.POST['firstName']
                contact.lastName = request.POST['lastName']
                contact.middleInitial = request.POST['middleInitial']
                contact.phoneNumber = request.POST['phoneNumber']
                contact.relation = request.POST['relation']
                contact.healthnetuser = hnuser
                contact.user_id = hnuser.pk
                contact.type = 'e'
                contact.save()

                user = None;
                contacts = None;

                if (hnuser.accountType == 'P'):
                    user = User.objects.get(username=request.user.username).healthnetuser.patient
                    contacts = Contact.objects.filter(user_id=user.id).exclude(relation='se')

                if (hnuser.accountType == 'D'):
                    user = User.objects.get(username=request.user.username).healthnetuser.staff
                    contacts = Contact.objects.filter(user_id=user.id).exclude(relation='se')

                createLogEvent(request.user.username, request.user.username, 7, "User added a new contact")
                html = render_to_string('profiles/ajax_contactlist.html', {'contacts': contacts, 'hnuser': user})
                res = {'html': html}
                return HttpResponse(json.dumps(res), mimetype)
            else:
                format = 'json'
                mimetype = 'application/json'

                form = ContactForm(no_self=True)

                html = render_to_string('profiles/ajax_addcontact.html', {'form': form})
                res = {'html': html}
                return HttpResponse(json.dumps(res), mimetype)
        else:
            message = "You do not have permission to view the requested page."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 13,
            "Someone attempted to create a user contact without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent(request.user.username, username, 13, "Someone attempted to create a user contact without being logged in")
        return HttpResponseRedirect("/")

def editContact(request, username, pk):
    if request.user.is_authenticated():
        if request.user.username == username:
            hnuser = User.objects.get(username=request.user.username).healthnetuser
            contact = Contact.objects.get(pk=pk)
            if contact.user_id == User.objects.get(username=request.user.username).healthnetuser.pk:
                if request.method == 'POST':
                    format = 'json'
                    mimetype = 'application/json'

                    contact.street = request.POST['street']
                    contact.city = request.POST['city']
                    contact.state = request.POST['state']
                    contact.zipcode = request.POST['zipcode']
                    contact.firstName = request.POST['firstName']
                    contact.lastName = request.POST['lastName']
                    contact.middleInitial = request.POST['middleInitial']
                    contact.phoneNumber = request.POST['phoneNumber']
                    contact.relation = request.POST['relation']
                    contact.save()

                    user = None;
                    contacts = None;

                    if (hnuser.accountType == 'P'):
                        user = User.objects.get(username=request.user.username).healthnetuser.patient
                        contacts = Contact.objects.filter(user_id=user.id).exclude(relation='se')

                    if (hnuser.accountType == 'D'):
                        user = User.objects.get(username=request.user.username).healthnetuser.staff
                        contacts = Contact.objects.filter(user_id=user.id).exclude(relation='se')

                    createLogEvent(request.user.username, username, 8, "User edited a contact")
                    html = render_to_string('profiles/ajax_contactlist.html', {'contacts': contacts, 'hnuser': user})
                    res = {'html': html}
                    return HttpResponse(json.dumps(res), mimetype)
                else:
                    data = {
                        'street': contact.street,
                        'city': contact.city,
                        'state': contact.state,
                        'zipcode': contact.zipcode,
                        'firstName': contact.firstName,
                        'lastName': contact.lastName,
                        'middleInitial': contact.middleInitial,
                        'phoneNumber': contact.phoneNumber,
                        'relation': contact.relation,
                    }
                    form = ContactForm(data, no_self=True)

                    format = 'json'
                    mimetype = 'application/json'

                    html = render_to_string('profiles/ajax_editcontact.html', {'form': form})
                    res = {'html': html}
                    return HttpResponse(json.dumps(res), mimetype)
            else:
                message = "You do not have permission to view the requested page."
                messages.add_message(request, messages.INFO, message)
                createLogEvent(request.user.username, username, 12,
                               "User attempted to edit a user contact without permission")
                return HttpResponseRedirect("/")

        else:
            message = "You do not have permission to view the requested page."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 12,
                           "User attempted to edit a user contact without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 12, "Someone attempted to edit a user contact without being logged in")
        return HttpResponseRedirect("/")

def deleteContact(request, username, pk):
    if request.user.is_authenticated():
        if request.user.username == username:
            hnuser = User.objects.get(username=request.user.username).healthnetuser
            contact = Contact.objects.get(pk=pk)
            if contact.user_id == User.objects.get(username=request.user.username).healthnetuser.pk:
                contactName = contact.firstName
                contact.delete()

                user = None;
                contacts = None;

                if (hnuser.accountType == 'P'):
                    user = User.objects.get(username=request.user.username).healthnetuser.patient
                    contacts = Contact.objects.filter(user_id=user.id).exclude(relation='se')

                if (hnuser.accountType == 'D'):
                    user = User.objects.get(username=request.user.username).healthnetuser.staff
                    contacts = Contact.objects.filter(user_id=user.id).exclude(relation='se')

                createLogEvent(request.user.username, username, 9, "User deleted a contact")
                format = 'json'
                mimetype = 'application/json'
                html = render_to_string('profiles/ajax_contactlist.html', {'contacts': contacts, 'hnuser': user})
                res = {'html': html}
                return HttpResponse(json.dumps(res), mimetype)
            else:
                message = "You do not have permission to do that."
                messages.add_message(request, messages.INFO, message)
                createLogEvent(request.user.username, username, 14,
                               "User attempted to delete a user contact without permission")
                return HttpResponseRedirect("/")
        else:
            message = "You do not have permission to do that."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 14,
                           "User attempted to delete a user contact without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 14, "Someone attempted to delete a user contact without being logged in")
        return HttpResponseRedirect("/")

def newCase(request, username):
    if request.user.is_authenticated():
        if (request.user.username == username or request.user.healthnetuser.accountType != 'P'):

            hnuser = User.objects.get(username=username).healthnetuser
            format = 'json'
            mimetype = 'application/json'

            if request.method == "POST":
                case = MedicalCase()
                case.title = request.POST["title"]
                case.caseId = request.POST["caseId"]
                case.date = timezone.now()
                case.notes = request.POST["notes"]
                case.ongoing = True
                case.patient = hnuser.patient
                case.illness = Illness.objects.get(pk=request.POST["illness"])
                case.save()

                cases = MedicalCase.objects.filter(patient=hnuser.patient)

                html = render_to_string('profiles/ajax_patientcases.html', {'cases': cases})
                res = {'html': html}
                return HttpResponse(json.dumps(res), mimetype)
            else:
                illnesses = Illness.objects.all()

                html = render_to_string('profiles/ajax_newcase.html', {'illnesses': illnesses})
                res = {'html': html}
                return HttpResponse(json.dumps(res), mimetype)
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 11, "Someone attempted to peek a profile without being logged in")
        return HttpResponseRedirect("/")

def saveCaseNotes(request, username, pk):
    if request.user.is_authenticated():
        if (request.user.username == username or request.user.healthnetuser.accountType != 'P'):

            hnuser = User.objects.get(username=username).healthnetuser
            format = 'json'
            mimetype = 'application/json'

            if request.method == "POST":
                case = MedicalCase.objects.get(pk=pk)
                case.notes = request.POST["notes"]
                case.save()

                return HttpResponse("Saved")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 11, "Someone attempted to peek a profile without being logged in")
        return HttpResponseRedirect("/")

def addPeekContact(request, username, pk):
    if request.user.is_authenticated():
        if request.user.username == username:
            format = 'json'
            mimetype = 'application/json'

            user = User.objects.get(username=request.user.username).healthnetuser

            contact = Contact.objects.get(pk=pk)
            newContact = Contact()
            newContact.firstName = contact.firstName
            newContact.middleInitial = contact.middleInitial
            newContact.lastName = contact.lastName
            newContact.phoneNumber = contact.phoneNumber
            newContact.street = contact.street
            newContact.city = contact.city
            newContact.state = contact.state
            newContact.zipcode = contact.zipcode
            newContact.relation = 'ot'
            newContact.type = contact.type
            newContact.user = user
            newContact.save()

            return HttpResponse("Added")
        else:
            message = "You do not have permission to view the requested page."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 13,
            "Someone attempted to create a user contact without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent(request.user.username, username, 13, "Someone attempted to create a user contact without being logged in")
        return HttpResponseRedirect("/")

'''
Temporary Views
'''

# The view is temporary.  It is used to test new UI features.
def uiTest(request):
    if (request.method == "POST"):
        format = 'json'
        mimetype = 'application/json'
        hnuser = User.objects.get(username=request.POST["username"]).healthnetuser
        patient = hnuser.patient
        patientContact = Contact.objects.get(user=hnuser, relation='se')
        html = render_to_string('profiles/temp_ajaxtest.html', {'patient': patient, 'patientContact': patientContact})
        res = {'html': html}
        return HttpResponse(json.dumps(res), mimetype)
    else:
        return render(request, 'profiles/uitest.html')

'''
Extra Functions
'''

# Sets up the array to send to the calendars
def calendarArraySetup(appointments):
    ar = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]

    syears = {}
    smonths = {}
    sdays = {}
    shours = {}
    smins = {}
    eyears = {}
    emonths = {}
    edays = {}
    ehours = {}
    emins = {}
    ids = {}
    titles = {}
    descs = {}

    i = 0
    for appointment in appointments:
        syears[i] = appointment.startDate.year
        smonths[i] = appointment.startDate.month
        sdays[i] = appointment.startDate.day
        shours[i] = appointment.startHours()
        smins[i] = appointment.startMinutes()
        eyears[i] = appointment.endDate.year
        emonths[i] = appointment.endDate.month
        edays[i] = appointment.endDate.day
        ehours[i] = appointment.endHours()
        emins[i] = appointment.endMinutes()
        ids[i] = appointment.pk
        titles[i] = appointment.title
        descs[i] = appointment.reason
        i += 1

    ar[0] = syears
    ar[1] = smonths
    ar[2] = sdays
    ar[3] = shours
    ar[4] = smins
    ar[5] = eyears
    ar[6] = emonths
    ar[7] = edays
    ar[8] = ehours
    ar[9] = emins
    ar[10] = ids
    ar[11] = titles
    ar[12] = descs

    return json.dumps(ar)

# AUTHENTICATION TEMPLATE
# if request.user.is_authenticated():
#     if request.user.username == username:
#         # User is successfully authenticated and logged in
#         # Do stuff...
#     else:
#         message = "You do not have permission to view the requested page."
#         messages.add_message(request, messages.INFO, message)
#         createLogEvent(request.user.username, username, 20,
#         "Someone attempted to perform an action on someone else\'s profile without permission")
#         return HttpResponseRedirect("/")
# else:
#     message = "You must login to do that!"
#     messages.add_message(request, messages.INFO, message)
#     createLogEvent("n/a", username, 11, "Someone attempted to view a profile without being logged in")
#     return HttpResponseRedirect("/")
