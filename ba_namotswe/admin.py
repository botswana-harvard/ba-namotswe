from django.contrib import admin

from edc_base.modeladmin.mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
    ModelAdminAuditFieldsMixin)

from .admin_site import ba_namotswe_admin
from .models import SubjectVisit, Enrollment, Oi, Abstraction, Treatment, ARTRegimen, Appointment
from ba_namotswe.forms.enrollment_form import EnrollmentForm
from ba_namotswe.forms.treatment_form import TreatmentForm
from ba_namotswe.models.collected_data import CollectedData
from ba_namotswe.models.tb_history import TBHistory
from ba_namotswe.forms.tb_history_form import TBHistoryForm
from ba_namotswe.models import SubjectIdentifier


@admin.register(SubjectIdentifier, site=ba_namotswe_admin)
class SubjectIdentifierAdmin(admin.ModelAdmin):
    pass


class MembershipBaseModelAdmin(ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
                               ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin, admin.ModelAdmin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'

    def redirect_url(self, request, obj, post_url_continue=None):
        return request.GET.get('next')


@admin.register(Enrollment, site=ba_namotswe_admin)
class EnrollmentAdmin(MembershipBaseModelAdmin):
    form = EnrollmentForm
    radio_fields = {
        'caregiver_relation': admin.VERTICAL,
        'weight_measured': admin.VERTICAL,
        'height_measured': admin.VERTICAL}

    list_display = ('dashboard', 'initial_visit_date', 'hiv_diagnosis_date', 'art_initiation_date', )


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


@admin.register(CollectedData, site=ba_namotswe_admin)
class CollectedDataAdmin(admin.ModelAdmin):
    list_filter = ('arv_changes', 'tb_diagnosis', )
    radio_fields = {
        'arv_changes': admin.VERTICAL,
        'tb_diagnosis': admin.VERTICAL,
        'oi_diagnosis': admin.VERTICAL,
        'preg_diagnosis': admin.VERTICAL,
        'counselling_adhere': admin.VERTICAL,
        'transfer': admin.VERTICAL,
        'death': admin.VERTICAL}


@admin.register(TBHistory, site=ba_namotswe_admin)
class TBHistoryAdmin(admin.ModelAdmin):
    form = TBHistoryForm
    radio_fields = {
        'tb_type': admin.VERTICAL,
        'tb_test': admin.VERTICAL}
