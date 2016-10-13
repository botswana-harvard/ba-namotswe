from django.contrib import admin

from .admin_site import ba_namotswe_admin
from .models import (
    RegisteredSubject, SubjectVisit, Enrollment, Oi, Abstraction, Treatment, ARTRegimen, Appointment)
from ba_namotswe.forms.enrollment_form import EnrollmentForm
from ba_namotswe.forms.registered_subject_form import RegisteredSubjectForm
from ba_namotswe.forms.treatment_form import TreatmentForm


@admin.register(Enrollment, site=ba_namotswe_admin)
class EnrollmentAdmin(admin.ModelAdmin):
    form = EnrollmentForm
    radio_fields = {
        'caregiver_relation': admin.VERTICAL,
        'weight_measured': admin.VERTICAL,
        'height_measured': admin.VERTICAL}


@admin.register(RegisteredSubject, site=ba_namotswe_admin)
class RegisteredSubjectAdmin(admin.ModelAdmin):
    list_filter = ('dob', )
    form = RegisteredSubjectForm


@admin.register(Appointment, site=ba_namotswe_admin)
class AppointmentAdmin(admin.ModelAdmin):
    list_filter = ('best_appt_datetime', )


@admin.register(SubjectVisit, site=ba_namotswe_admin)
class SubjectVisitAdmin(admin.ModelAdmin):
    list_filter = ('report_datetime', )


@admin.register(Abstraction, site=ba_namotswe_admin)
class AbstractionAdmin(admin.ModelAdmin):
    list_filter = ('subject_visit', )


@admin.register(Treatment, site=ba_namotswe_admin)
class TreatmentAdmin(admin.ModelAdmin):
    list_filter = ('perinatal_infection', )
    form = TreatmentForm


@admin.register(Oi, site=ba_namotswe_admin)
class OiAdmin(admin.ModelAdmin):
    list_filter = ('name', )


@admin.register(ARTRegimen, site=ba_namotswe_admin)
class ARTRegimenAdmin(admin.ModelAdmin):
    list_filter = ('name', )
