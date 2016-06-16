"""
HealthNet Profile URLs
"""
from django.conf.urls import url

from . import views

app_name = 'profiles'  # namespace

urlpatterns = [
    # The root URL links to the index view that displays the login page
    url(r'^$', views.index, name='index'),

    # The register URL links to the register view to create a new user
    url(r'^register/$', views.register, name='register'),

    # The login URL links to the login view which authenticates a user with the given form data
    url(r'^login/$', views.login, name='login'),

    # The logout URL links to the login view which simply logs out the current session
    url(r'^logout/$', views.logout, name='logout'),

    # This URL links to the viewProfile view that displays a user's information
    url(r'^profiles/(?P<username>\w*)$', views.viewProfile, name='viewProfile'),

    # This URL links to the uploadPic view which handles the uploading of profile pictures
    url(r'^profiles/(?P<username>\w+)/uploadpicture$', views.uploadPic, name="uploadPic"),
    url(r'^profiles/(?P<username>\w+)/ajaxpicupload$', views.ajaxUploadPic, name="ajaxUploadPic"),

    # This URL is used to upload patient files
    url(r'^profiles/(?P<username>\w+)/fileupload$', views.fileUpload, name='fileUpload'),
    url(r'^profiles/patient-files/(?P<pk>[a-zA-Z0-9_-]+)/$', views.default_file_view, name='default_file'),

    # This URL is used to update a user's shownTutorial field after the tutorial
    url(r'^profiles/(?P<username>\w+)/endtut$', views.endTut, name="endTut"),

    # This URL is used to show a preview of a user's profile to others
    url(r'^profiles/(?P<username>\w+)/peek$', views.peekView, name='peekView'),

    # This URL is used to receive search terms and return results to the user
    url(r'^profiles/(?P<username>\w+)/search$', views.searchView, name='searchView'),

    # These URLs are used to update basic patient info
    url(r'^profiles/(?P<username>\w+)/editbasicinfo$', views.editBasicInfo, name='editBasicInfo'),
    url(r'^profiles/(?P<username>\w+)/savebasicinfo$', views.saveBasicInfo, name='saveBasicInfo'),

    # These URLs are used to update patient insurance info
    url(r'^profiles/(?P<username>\w+)/editmedicalinfo$', views.editMedicalInfo, name='editMedicalInfo'),
    url(r'^profiles/(?P<username>\w+)/savemedicalinfo$', views.saveMedicalInfo, name='saveMedicalInfo'),

    # These URLs are used to add and edit contacts
    url(r'^profiles/(?P<username>\w+)/addcontact$', views.addContact, name='addContact'),
    url(r'^profiles/(?P<username>\w+)/editcontact/(?P<pk>[0-9]+)$', views.editContact, name='editContact'),

    # This URL links to the deleteContact view which deletes the contact
    url(r'^profiles/(?P<username>\w+)/deletecontact/(?P<pk>[0-9]+)$', views.deleteContact, name='deleteContact'),

    url(r'^profiles/(?P<username>\w+)/newcase$', views.newCase, name='newCase'),
    url(r'^profiles/(?P<username>\w+)/savecasenotes/(?P<pk>[0-9]+)$', views.saveCaseNotes, name='saveCaseNotes'),

    url(r'^profiles/(?P<username>\w+)/peekcontact/(?P<pk>[0-9]+)$', views.addPeekContact, name='addPeekContact'),

    # This is a temporary URL used to test new UI features
    url(r'^ui$', views.uiTest, name="uiTest"),
]
