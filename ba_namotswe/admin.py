from django.contrib import admin

from edc_base.modeladmin.mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
    ModelAdminAuditFieldsMixin)

from edc_visit_tracking.admin import VisitAdminMixin

from .models import SubjectVisit, Enrollment, Oi, Abstraction, Treatment, ArtRegimen, Appointment
from ba_namotswe.forms.enrollment_form import EnrollmentForm
from ba_namotswe.forms.treatment_form import TreatmentForm
from ba_namotswe.models.collected_data import CollectedData
from ba_namotswe.models import TbHistory
from ba_namotswe.forms.tb_history_form import TBHistoryForm
from ba_namotswe.models import SubjectIdentifier
from ba_namotswe.models import DummyConsent
from ba_namotswe.forms import DummyConsentForm
from ba_namotswe.forms import SubjectVisitForm


class SubjectIdentifierAdmin(admin.ModelAdmin):
    pass
admin.site.register(SubjectIdentifier, SubjectIdentifierAdmin)


class MembershipBaseModelAdmin(ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
                               ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin, admin.ModelAdmin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'

    def redirect_url(self, request, obj, post_url_continue=None):
        return request.GET.get('next')


class EnrollmentAdmin(MembershipBaseModelAdmin):
    form = EnrollmentForm
    radio_fields = {
        'caregiver_relation': admin.VERTICAL,
        'gender': admin.VERTICAL,
        'weight_measured': admin.VERTICAL,
        'height_measured': admin.VERTICAL}

    list_display = ('dashboard', 'initial_visit_date', 'hiv_diagnosis_date', 'art_initiation_date', )
admin.site.register(Enrollment, EnrollmentAdmin)


class AppointmentAdmin(MembershipBaseModelAdmin):
    list_filter = ('best_appt_datetime', )
admin.site.register(Appointment, AppointmentAdmin)


class SubjectVisitAdmin(VisitAdminMixin, MembershipBaseModelAdmin):

    form = SubjectVisitForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'appointment' and request.GET.get('appointment'):
            kwargs["queryset"] = Appointment.objects.filter(pk=request.GET.get('appointment', 0))
        return super(VisitAdminMixin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectVisit, SubjectVisitAdmin)


class AbstractionAdmin(MembershipBaseModelAdmin):
    list_filter = ('subject_visit', )
admin.site.register(Abstraction, AbstractionAdmin)


class TreatmentAdmin(MembershipBaseModelAdmin):
    list_filter = ('perinatal_infection', )
    form = TreatmentForm
admin.site.register(Treatment, TreatmentAdmin)


class OiAdmin(MembershipBaseModelAdmin):
    list_filter = ('name', )
admin.site.register(Oi, OiAdmin)


class ARTRegimenAdmin(MembershipBaseModelAdmin):
    list_filter = ('name', )
admin.site.register(ArtRegimen, ARTRegimenAdmin)


class CollectedDataAdmin(MembershipBaseModelAdmin):
    list_filter = ('arv_changes', 'tb_diagnosis', )
    radio_fields = {
        'arv_changes': admin.VERTICAL,
        'tb_diagnosis': admin.VERTICAL,
        'oi_diagnosis': admin.VERTICAL,
        'preg_diagnosis': admin.VERTICAL,
        'counselling_adhere': admin.VERTICAL,
        'transfer': admin.VERTICAL,
        'death': admin.VERTICAL}
admin.site.register(CollectedData, CollectedDataAdmin)


class TBHistoryAdmin(MembershipBaseModelAdmin):
    form = TBHistoryForm
    radio_fields = {
        'tb_type': admin.VERTICAL,
        'tb_test': admin.VERTICAL}
admin.site.register(TbHistory, TBHistoryAdmin)


class DummyConsentAdmin(MembershipBaseModelAdmin):

    dashboard_type = 'subject'
    form = DummyConsentForm

admin.site.register(DummyConsent, DummyConsentAdmin)
