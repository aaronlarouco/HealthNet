from django.contrib import admin

from .models import *


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


class StaffInline(admin.TabularInline):
    model = Staff
    extra = 0

class FilesInline(admin.TabularInline):
    model = PatientFile
    extra = 0

class PrescriptionsInline(admin.TabularInline):
    model = Prescription
    extra = 0

class CasesInline(admin.TabularInline):
    model = MedicalCase
    extra = 0

class PatientAdmin(admin.ModelAdmin):
    inlines = [ContactInline, CasesInline, PrescriptionsInline, FilesInline]


class StaffAdmin(admin.ModelAdmin):
    inlines = [ContactInline]


class HospitalAdmin(admin.ModelAdmin):
    inlines = [StaffInline]


admin.site.register(Patient, PatientAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Drug)
admin.site.register(Illness)
