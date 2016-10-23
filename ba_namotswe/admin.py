from django.contrib import admin

from edc_base.modeladmin.mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
    ModelAdminAuditFieldsMixin)
from edc_visit_tracking.admin import VisitAdminMixin

from .forms import (
    SubjectConsentForm, SubjectVisitForm, TBHistoryForm, TreatmentForm, EnrollmentForm, AbstractionForm,
    AdherenceCounsellingForm, ArvHistoryForm, AssessmentHistoryForm, DeathForm, PregnancyHistoryForm,
    TransferHistoryForm, OiForm, ArtRegimenForm, CollectedDataForm)
from .models import (
    SubjectConsent, SubjectVisit, CollectedData, Enrollment, Oi, Abstraction, Treatment, ArtRegimen,
    Appointment, TbHistory, AdherenceCounselling, ArvHistory, AssessmentHistory, Death, PregnancyHistory,
    TransferHistory)


class BaseModelAdmin(ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
                     ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin, admin.ModelAdmin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'

    def redirect_url(self, request, obj, post_url_continue=None):
        return request.GET.get('next')


@admin.register(Enrollment)
class EnrollmentAdmin(BaseModelAdmin):
    form = EnrollmentForm
    radio_fields = {
        'caregiver_relation': admin.VERTICAL,
        'gender': admin.VERTICAL,
        'weight_measured': admin.VERTICAL,
        'height_measured': admin.VERTICAL}

    list_display = ('dashboard', 'initial_visit_date', 'hiv_diagnosis_date', 'art_initiation_date', )


@admin.register(Appointment)
class AppointmentAdmin(BaseModelAdmin):
    list_filter = ('best_appt_datetime', )


@admin.register(SubjectVisit)
class SubjectVisitAdmin(VisitAdminMixin, BaseModelAdmin):

    form = SubjectVisitForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'appointment' and request.GET.get('appointment'):
            kwargs["queryset"] = Appointment.objects.filter(pk=request.GET.get('appointment', 0))
        return super(VisitAdminMixin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Abstraction)
class AbstractionAdmin(BaseModelAdmin):
    list_filter = ('subject_visit', )
    form = AbstractionForm
    # fields = ()
    readonly_fields = ('subject_visit', )
    filter_horizontal = ('art_history', 'io_history')
    radio_fields = {
        'height_measured': admin.VERTICAL,
        'weight_measured': admin.VERTICAL,
        'hospitalized': admin.VERTICAL,
        'tb': admin.VERTICAL,
        'tb_type': admin.VERTICAL,
        'tb_method': admin.VERTICAL,
        'io': admin.VERTICAL,
        'ctx': admin.VERTICAL,
        'ctx_table': admin.VERTICAL,
        'pregnant_and_rx': admin.VERTICAL,
        'hiv_status_aware': admin.VERTICAL,
        'hiv_disclosed_others': admin.VERTICAL,
        'hiv_caregiver_disclosed_others': admin.VERTICAL,
        'transferred': admin.VERTICAL,
        'transferred_to': admin.VERTICAL,
        'deceased': admin.VERTICAL,
    }


@admin.register(PregnancyHistory)
class PregnancyHistoryAdmin(BaseModelAdmin):
    list_filter = ('subject_visit', )
    form = PregnancyHistoryForm


@admin.register(TransferHistory)
class TransferHistoryAdmin(BaseModelAdmin):
    list_filter = ('subject_visit', )
    form = TransferHistoryForm


@admin.register(Death)
class DeathAdmin(BaseModelAdmin):
    list_filter = ('subject_visit', )
    form = DeathForm


@admin.register(AssessmentHistory)
class AssessmentHistoryAdmin(BaseModelAdmin):
    list_filter = ('subject_visit', )
    form = AssessmentHistoryForm


@admin.register(ArvHistory)
class ArvHistoryAdmin(BaseModelAdmin):
    list_filter = ('subject_visit', )
    form = ArvHistoryForm


@admin.register(AdherenceCounselling)
class AdherenceCounsellingAdmin(BaseModelAdmin):
    list_filter = ('subject_visit', )
    form = AdherenceCounsellingForm


@admin.register(Treatment)
class TreatmentAdmin(BaseModelAdmin):
    list_filter = ('perinatal_infection', )
    form = TreatmentForm


@admin.register(Oi)
class OiAdmin(BaseModelAdmin):
    list_filter = ('oi_type', )
    radio_fields = {
        'oi_type': admin.VERTICAL}
    form = OiForm


@admin.register(ArtRegimen)
class ARTRegimenAdmin(BaseModelAdmin):
    list_filter = ('name', )
    form = ArtRegimenForm


@admin.register(CollectedData)
class CollectedDataAdmin(BaseModelAdmin):
    list_filter = ('arv_changes', 'tb_diagnosis', )
    radio_fields = {
        'arv_changes': admin.VERTICAL,
        'tb_diagnosis': admin.VERTICAL,
        'oi_diagnosis': admin.VERTICAL,
        'preg_diagnosis': admin.VERTICAL,
        'counselling_adhere': admin.VERTICAL,
        'transfer': admin.VERTICAL,
        'death': admin.VERTICAL}
    form = CollectedDataForm


@admin.register(TbHistory)
class TBHistoryAdmin(BaseModelAdmin):
    form = TBHistoryForm
    radio_fields = {
        'tb_type': admin.VERTICAL,
        'tb_test': admin.VERTICAL}


@admin.register(SubjectConsent)
class SubjectConsentAdmin(BaseModelAdmin):

    dashboard_type = 'subject'
    form = SubjectConsentForm
