"""
HealthNet Appointments Views
"""
import json

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import *
from .models import *
from profiles.models import *
from log.views import createLogEvent


# The create appointment view determines what type of account is requesting
# to create an appointment, then sends the proper form and renders the proper
# template so the user can schedule a new appointment.
def createAppointment(request, username):
    if request.user.is_authenticated():
        hnuser = User.objects.get(username=request.user.username).healthnetuser

        if request.user.username == username:
            if request.method == 'POST':
                appointment = Appointment()

                appointment.title = request.POST['title']
                appointment.startDate = request.POST['startDate']
                appointment.startTime = request.POST['startTime']
                appointment.endDate = request.POST['startDate']
                appointment.endTime = request.POST['startTime']
                appointment.hospital = Hospital.objects.get(pk=request.POST['hospital'])
                appointment.room = request.POST['room']
                appointment.reason = request.POST['reason']

                appointments = None

                if hnuser.accountType == 'P':
                    appointment.patient = hnuser.patient
                    appointment.doctor = Staff.objects.get(pk=request.POST['doctor'])
                    hnuser = hnuser.patient
                    appointments = Appointment.objects.filter(patient=hnuser)

                elif hnuser.accountType == 'D':
                    appointment.patient = Patient.objects.get(pk=request.POST['patient'])
                    appointment.doctor = hnuser.staff

                    casePost = request.POST['case']
                    if casePost != "":
                        case = MedicalCase.objects.get(pk=casePost)
                        if case is not None:
                            appointment.case = case

                    hnuser = hnuser.staff
                    appointments = Appointment.objects.filter(doctor=hnuser)

                elif hnuser.accountType == 'N':
                    appointment.patient = Patient.objects.get(pk=request.POST['patient'])
                    appointment.doctor = Staff.objects.get(pk=request.POST['doctor'])
                    appointment.case = MedicalCase.objects.get(pk=request.POST['case'])
                    hnuser = hnuser.staff
                    appointments = Appointment.objects.filter(hospital=hnuser.hospital)

                appointment.save()
                createLogEvent(request.user.username, username, 15, "User created appointment")

                json_ar = calendarArraySetup(appointments)

                format = 'json'
                mimetype = 'application/json'
                maincal = render_to_string('appointments/ajax_maincalendar.html', {'hnuser': hnuser, 'json_ar': json_ar})
                daycal = render_to_string('appointments/ajax_daycalendar.html', {'hnuser': hnuser, 'json_ar': json_ar})
                res = {'maincal': maincal, 'daycal': daycal}
                return HttpResponse(json.dumps(res), mimetype)
            else:
                if hnuser.accountType == 'P':
                    template = 'appointments/ajax_createappointment_patient.html'
                    form = PatientAppointmentForm()
                    hnuser = hnuser.patient
                    doctors = Contact.objects.filter(type='d')
                    hospitals = Hospital.objects.all()

                    format = 'json'
                    mimetype = 'application/json'
                    html = render_to_string(template, {'form': form, 'username': username,
                                                      'hnuser': hnuser, 'doctors': doctors, 'hospitals': hospitals})
                    res = {'html': html}
                    return HttpResponse(json.dumps(res), mimetype)

                if hnuser.accountType == 'D':
                    template = 'appointments/ajax_createappointment_staff.html'
                    form = StaffAppointmentForm()
                    hnuser = hnuser.staff
                    doctors = Contact.objects.filter(type='d')
                    patients = Contact.objects.filter(type='p')
                    hospitals = Hospital.objects.all()
                    docContact = Contact.objects.get(user=hnuser)

                    format = 'json'
                    mimetype = 'application/json'
                    html = render_to_string(template, {'form': form, 'username': username,
                                                      'hnuser': hnuser, 'doctors': doctors, 'hospitals': hospitals,
                                                      'patients': patients, 'docContact': docContact})
                    res = {'html': html}
                    return HttpResponse(json.dumps(res), mimetype)

                if hnuser.accountType == 'N':
                    template = 'appointments/ajax_createappointment_staff.html'
                    form = StaffAppointmentForm()
                    hnuser = hnuser.staff
                    doctors = Contact.objects.filter(type='d')
                    patients = Contact.objects.filter(type='p')
                    hospitals = Hospital.objects.all()
                    docContact = Contact.objects.get(user=hnuser)

                    format = 'json'
                    mimetype = 'application/json'
                    html = render_to_string(template, {'form': form, 'username': username,
                                                      'hnuser': hnuser, 'doctors': doctors, 'hospitals': hospitals,
                                                      'patients': patients, 'docContact': docContact})
                    res = {'html': html}
                    return HttpResponse(json.dumps(res), mimetype)
        else:
            message = "You do not have permission to view the requested page."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 13,
                           "User attempted to create an appointment without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 13, "Someone attempted to create an appointment without being logged in")
        return HttpResponseRedirect("/")


def editAppointment(request, username, pk):
    if request.user.is_authenticated():
        hnuser = User.objects.get(username=username).healthnetuser
        appointment = Appointment.objects.get(pk=pk)

        if request.user.username == username:
            if hnuser.accountType == 'P':
                if appointment.patient == hnuser.patient:
                    if request.method == 'POST':
                        appointment.title = request.POST['title']
                        appointment.startDate = request.POST['startDate']
                        appointment.startTime = request.POST['startTime']
                        appointment.endDate = request.POST['startDate']
                        appointment.endTime = request.POST['startTime']
                        appointment.hospital = Hospital.objects.get(pk=request.POST['hospital'])
                        appointment.room = request.POST['room']
                        appointment.reason = request.POST['reason']
                        appointment.patient = hnuser.patient
                        appointment.doctor = Staff.objects.get(pk=request.POST['doctor'])

                        appointment.save()
                        createLogEvent(request.user.username, username, 16, "User edited appointment")

                        hnuser = hnuser.patient

                        appointments = Appointment.objects.filter(patient=hnuser)
                        json_ar = calendarArraySetup(appointments)

                        format = 'json'
                        mimetype = 'application/json'
                        maincal = render_to_string('appointments/ajax_maincalendar.html', {'hnuser': hnuser, 'json_ar': json_ar})
                        daycal = render_to_string('appointments/ajax_daycalendar.html', {'hnuser': hnuser, 'json_ar': json_ar})
                        res = {'maincal': maincal, 'daycal': daycal}
                        return HttpResponse(json.dumps(res), mimetype)

                    else:
                        startDate = appointment.startDate
                        startTime = appointment.startTime
                        endDate = appointment.endDate
                        endTime = appointment.endTime
                        template = 'appointments/ajax_editappointment_patient.html'
                        form = PatientAppointmentForm(instance=appointment)
                        hnuser = hnuser.patient
                        doctors = Contact.objects.filter(type='d')
                        hospitals = Hospital.objects.all()

                        format = 'json'
                        mimetype = 'application/json'
                        html = render_to_string(template, {'form': form, 'appointment': appointment, 'startDate': startDate,
                         'startTime': startTime, 'endDate': endDate, 'endTime': endTime,
                         'username': username, 'pk': pk, 'hnuser': hnuser, 'doctors': doctors,
                         'hospitals': hospitals})
                        res = {'html': html}
                        return HttpResponse(json.dumps(res), mimetype)

            elif hnuser.accountType == 'D':
                if appointment.doctor == hnuser.staff:
                    if request.method == 'POST':
                        appointment.title = request.POST['title']
                        appointment.startDate = request.POST['startDate']
                        appointment.startTime = request.POST['startTime']
                        appointment.endDate = request.POST['startDate']
                        appointment.endTime = request.POST['startTime']
                        appointment.hospital = Hospital.objects.get(pk=request.POST['hospital'])
                        appointment.room = request.POST['room']
                        appointment.reason = request.POST['reason']
                        appointment.patient = Patient.objects.get(pk=request.POST['patient'])
                        appointment.doctor = hnuser.staff

                        appointment.save()
                        createLogEvent(request.user.username, username, 16, "User edited appointment")

                        hnuser = hnuser.staff

                        appointments = Appointment.objects.filter(doctor=hnuser)
                        json_ar = calendarArraySetup(appointments)

                        format = 'json'
                        mimetype = 'application/json'
                        maincal = render_to_string('appointments/ajax_maincalendar.html', {'hnuser': hnuser, 'json_ar': json_ar})
                        daycal = render_to_string('appointments/ajax_daycalendar.html', {'hnuser': hnuser, 'json_ar': json_ar})
                        res = {'maincal': maincal, 'daycal': daycal}
                        return HttpResponse(json.dumps(res), mimetype)

                    else:
                        startDate = appointment.startDate
                        startTime = appointment.startTime
                        endDate = appointment.endDate
                        endTime = appointment.endTime

                        template = 'appointments/ajax_editappointment_staff.html'
                        form = StaffAppointmentForm(instance=appointment)
                        hnuser = hnuser.staff
                        doctors = Contact.objects.filter(type='d')
                        patients = Contact.objects.filter(type='p')
                        hospitals = Hospital.objects.all()

                        format = 'json'
                        mimetype = 'application/json'
                        html = render_to_string(template, {'form': form, 'appointment': appointment, 'startDate': startDate,
                         'startTime': startTime, 'endDate': endDate, 'endTime': endTime,
                         'username': username, 'pk': pk, 'hnuser': hnuser, 'doctors': doctors,
                         'patients': patients, 'hospitals': hospitals})
                        res = {'html': html}
                        return HttpResponse(json.dumps(res), mimetype)

                elif hnuser.accountType == 'N':
                    if appointment.doctor == hnuser.staff:
                        if request.method == 'POST':
                            appointment.title = request.POST['title']
                            appointment.startDate = request.POST['startDate']
                            appointment.startTime = request.POST['startTime']
                            appointment.endDate = request.POST['startDate']
                            appointment.endTime = request.POST['startTime']
                            appointment.hospital = Hospital.objects.get(pk=request.POST['hospital'])
                            appointment.room = request.POST['room']
                            appointment.reason = request.POST['reason']
                            appointment.patient = Patient.objects.get(pk=request.POST['patient'])
                            appointment.doctor = Patient.objects.get(pk=request.POST['doctor'])

                            appointment.save()
                            createLogEvent(request.user.username, username, 16, "User edited appointment")

                            hnuser = hnuser.staff

                            appointments = Appointment.objects.filter(doctor=hnuser)
                            json_ar = calendarArraySetup(appointments)

                            format = 'json'
                            mimetype = 'application/json'
                            maincal = render_to_string('appointments/ajax_maincalendar.html', {'hnuser': hnuser, 'json_ar': json_ar})
                            daycal = render_to_string('appointments/ajax_daycalendar.html', {'hnuser': hnuser, 'json_ar': json_ar})
                            res = {'maincal': maincal, 'daycal': daycal}
                            return HttpResponse(json.dumps(res), mimetype)

                        else:
                            startDate = appointment.startDate
                            startTime = appointment.startTime
                            endDate = appointment.endDate
                            endTime = appointment.endTime

                            template = 'appointments/ajax_editappointment_staff.html'
                            form = StaffAppointmentForm(instance=appointment)
                            hnuser = hnuser.staff
                            doctors = Contact.objects.filter(type='d')
                            patients = Contact.objects.filter(type='p')
                            hospitals = Hospital.objects.all()

                            format = 'json'
                            mimetype = 'application/json'
                            html = render_to_string(template, {'form': form, 'appointment': appointment, 'startDate': startDate,
                             'startTime': startTime, 'endDate': endDate, 'endTime': endTime,
                             'username': username, 'pk': pk, 'hnuser': hnuser, 'doctors': doctors,
                             'patients': patients, 'hospitals': hospitals})
                            res = {'html': html}
                            return HttpResponse(json.dumps(res), mimetype)
        else:
            message = "You do not have permission to view the requested page."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 12,
                           "User attempted to edit an appointment without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 12, "Someone attempted to edit an appointment without being logged in")
        return HttpResponseRedirect("/")


def viewAppointment(request, username, pk):
    if request.user.is_authenticated():
        hnuser = User.objects.get(username=request.user.username).healthnetuser
        appointment = Appointment.objects.get(pk=pk)
        patientContact = Contact.objects.get(relation='se', user=appointment.patient)
        doctorContact = Contact.objects.get(relation='se', user=appointment.doctor)

        if request.user.username == username:
            if hnuser.accountType == 'P':
                if appointment.patient == hnuser.patient:
                    createLogEvent(request.user.username, username, 19, "User viewed an appointment")

                    hnuser = hnuser.patient

                    format = 'json'
                    mimetype = 'application/json'

                    html = render_to_string('appointments/ajax_viewappointment.html', {'appointment': appointment,
                                                                                  'hnuser': hnuser,
                                                                                  'patientContact': patientContact,
                                                                                  'doctorContact': doctorContact})
                    res = {'html': html}
                    return HttpResponse(json.dumps(res), mimetype)

            elif hnuser.accountType == 'D':
                if appointment.doctor == hnuser.staff:
                    createLogEvent(request.user.username, username, 19, "User viewed an appointment")

                    hnuser = hnuser.staff

                    format = 'json'
                    mimetype = 'application/json'

                    html = render_to_string('appointments/ajax_viewappointment.html', {'appointment': appointment,
                                                                                  'hnuser': hnuser,
                                                                                  'patientContact': patientContact,
                                                                                  'doctorContact': doctorContact})
                    res = {'html': html}
                    return HttpResponse(json.dumps(res), mimetype)

            elif hnuser.accountType == 'N':
                if appointment.doctor == hnuser.staff:
                    createLogEvent(request.user.username, username, 19, "User viewed an appointment")

                    hnuser = hnuser.staff

                    format = 'json'
                    mimetype = 'application/json'

                    html = render_to_string('appointments/ajax_viewappointment.html', {'appointment': appointment,
                                                                                  'hnuser': hnuser,
                                                                                  'patientContact': patientContact,
                                                                                  'doctorContact': doctorContact})
                    res = {'html': html}
                    return HttpResponse(json.dumps(res), mimetype)

        else:
            message = "You do not have permission to view the requested page."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 11,
                           "User attempted to view an appointment without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 11, "Someone attempted to view an appointment without being logged in")
        return HttpResponseRedirect("/")


def cancelAppointment(request, username, pk):
    if request.user.is_authenticated():
        appointment = Appointment.objects.get(pk=pk)
        hnuser = User.objects.get(username=username).healthnetuser

        if request.user.username == username:
            if hnuser.accountType == 'P':
                if appointment.patient == hnuser.patient:
                    appointment.delete()
                    createLogEvent(request.user.username, username, 17, "User cancelled an appointment")

                    hnuser = hnuser.patient

                    appointments = Appointment.objects.filter(patient=hnuser)
                    json_ar = calendarArraySetup(appointments)

                    format = 'json'
                    mimetype = 'application/json'
                    maincal = render_to_string('appointments/ajax_maincalendar.html', {'hnuser': hnuser, 'json_ar': json_ar})
                    daycal = render_to_string('appointments/ajax_daycalendar.html', {'hnuser': hnuser, 'json_ar': json_ar})
                    res = {'maincal': maincal, 'daycal': daycal}
                    return HttpResponse(json.dumps(res), mimetype)
                else:
                    message = "You do not have permission to do that."
                    messages.add_message(request, messages.INFO, message)
                    createLogEvent(request.user.username, username, 14,
                                   "User attempted to cancel an appointment without permission")
                    return HttpResponseRedirect("/")

            elif hnuser.accountType == 'D':
                appointment.delete()
                createLogEvent(request.user.username, username, 17, "User cancelled an appointment")

                hnuser = hnuser.staff

                appointments = Appointment.objects.filter(doctor=hnuser)
                json_ar = calendarArraySetup(appointments)

                format = 'json'
                mimetype = 'application/json'
                maincal = render_to_string('appointments/ajax_maincalendar.html', {'hnuser': hnuser, 'json_ar': json_ar})
                daycal = render_to_string('appointments/ajax_daycalendar.html', {'hnuser': hnuser, 'json_ar': json_ar})
                res = {'maincal': maincal, 'daycal': daycal}
                return HttpResponse(json.dumps(res), mimetype)

            elif hnuser.accountType == 'N':
                appointment.delete()
                createLogEvent(request.user.username, username, 17, "User cancelled an appointment")

                hnuser = hnuser.staff

                appointments = Appointment.objects.filter(doctor=hnuser)
                json_ar = calendarArraySetup(appointments)

                format = 'json'
                mimetype = 'application/json'
                maincal = render_to_string('appointments/ajax_maincalendar.html', {'hnuser': hnuser, 'json_ar': json_ar})
                daycal = render_to_string('appointments/ajax_daycalendar.html', {'hnuser': hnuser, 'json_ar': json_ar})
                res = {'maincal': maincal, 'daycal': daycal}
                return HttpResponse(json.dumps(res), mimetype)
        else:
            message = "You do not have permission to do that."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 14,
                           "User attempted to cancel an appointment without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 14, "Someone attempted to cancel an appointment without being logged in")
        return HttpResponseRedirect("/")

def updateCases(request, username, pk):
    if request.user.is_authenticated():
        hnuser = User.objects.get(username=username).healthnetuser

        if request.user.username == username:
            patient = Patient.objects.get(pk=pk)
            cases = MedicalCase.objects.filter(patient=patient)

            format = 'json'
            mimetype = 'application/json'
            html = render_to_string('appointments/ajax_cases.html', {'cases': cases})
            res = {'html': html}
            return HttpResponse(json.dumps(res), mimetype)
        else:
            message = "You do not have permission to do that."
            messages.add_message(request, messages.INFO, message)
            createLogEvent(request.user.username, username, 14,
                           "User attempted to cancel an appointment without permission")
            return HttpResponseRedirect("/")
    else:
        message = "You must login to do that!"
        messages.add_message(request, messages.INFO, message)
        createLogEvent("n/a", username, 14, "Someone attempted to cancel an appointment without being logged in")
        return HttpResponseRedirect("/")


# The view is temporary.  It is used to test new UI features.
def uiTest(request):
    return render(request, 'appointments/calendartest.html')

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
