from django.contrib import admin

from edc_base.modeladmin.mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin, ModelAdminFormAutoNumberMixin,
    ModelAdminAuditFieldsMixin, TabularInlineMixin, StackedInlineMixin)
from edc_visit_tracking.admin import VisitAdminMixin

from .admin_site import ba_namotswe_admin
from .forms import (
    SubjectVisitForm, TBRecordForm, EnrollmentForm, ArtRecordForm, LabRecordForm, LabTestForm,
    AdherenceCounsellingForm, DeathForm, PregnancyHistoryForm, WhoStagingForm, WhoDiagnosisForm,
    TransferRecordForm, OiRecordForm, EntryToCareForm, InCareForm, LostToFollowupForm,
    ArtRegimenForm, OiForm, TransferForm, TbForm)
from .list_filters import VisitCodeListFilter, PendingFieldsListFilter
from .models import (
    SubjectConsent, SubjectVisit, Enrollment, OiRecord, Oi, EntryToCare,
    Appointment, TbRecord, Tb, AdherenceCounselling, ArtRecord, ArtRegimen, Death, PregnancyHistory, Pregnancy,
    TransferRecord, Transfer, LabRecord, LabTest, WhoStaging, WhoDiagnosis, LostToFollowup, InCare)


class BaseModelAdmin(ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
                     ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin, admin.ModelAdmin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'

    def redirect_url(self, request, obj, post_url_continue=None):
        return request.GET.get('next')


class BaseCrfModelAdmin(BaseModelAdmin):

    list_display = (
        'dashboard', 'subject_identifier', 'visit_code', 'edited', 'pending_fields',
        'flagged', 'no_report', 'reviewed')
    list_display_links = ('dashboard', )
    search_fields = ['pending_fields']
    instructions = (
        'Please complete the questions below. Required questions are in bold. '
        'When all required questions are complete click SAVE. Based on your responses, additional questions may be '
        'required or some answers may need to be corrected.')

    def get_list_filter(self, request):
        list_filter = super(BaseCrfModelAdmin, self).get_list_filter(request)
        list_filter = list(list_filter)
        list_filter.insert(0, 'no_report')
        list_filter.insert(0, 'edited')
        list_filter.insert(0, 'flagged')
        list_filter.insert(0, 'reviewed')
        list_filter.insert(0, PendingFieldsListFilter)
        list_filter.insert(0, VisitCodeListFilter)
        return list_filter

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'subject_visit' and request.GET.get('subject_visit'):
            kwargs["queryset"] = SubjectVisit.objects.filter(pk=request.GET.get('subject_visit', 0))
        return super(BaseCrfModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class BaseTabularInlineCrfModelAdmin(TabularInlineMixin, admin.TabularInline):
    pass


class BaseStackedInlineCrfModelAdmin(StackedInlineMixin, admin.StackedInline):
    pass


@admin.register(Enrollment, site=ba_namotswe_admin)
class EnrollmentAdmin(BaseModelAdmin):
    form = EnrollmentForm
    radio_fields = {
        'gender': admin.VERTICAL,
        'caregiver_relation': admin.VERTICAL}

    list_display = ('subject_identifier', 'report_datetime', 'age', 'dashboard', 'slh_identifier', 'cm_identifier')
    list_filter = ('report_datetime', )


@admin.register(Appointment, site=ba_namotswe_admin)
class AppointmentAdmin(BaseModelAdmin):
    list_filter = ('best_appt_datetime', )
    list_display = ('subject_identifier', 'appt_datetime', 'visit_code')


@admin.register(SubjectVisit, site=ba_namotswe_admin)
class SubjectVisitAdmin(VisitAdminMixin, BaseModelAdmin):

    form = SubjectVisitForm
    list_filter = ('subject_identifier', 'visit_datetime', 'visit_code')


@admin.register(Death, site=ba_namotswe_admin)
class DeathAdmin(BaseModelAdmin):
    form = DeathForm


@admin.register(LostToFollowup, site=ba_namotswe_admin)
class LostToFollowupAdmin(BaseModelAdmin):
    form = LostToFollowupForm


@admin.register(EntryToCare, site=ba_namotswe_admin)
class EntryToCareAdmin(BaseCrfModelAdmin):
    form = EntryToCareForm
    radio_fields = {
        'weight_measured': admin.VERTICAL,
        'height_measured': admin.VERTICAL,
        'phiv': admin.VERTICAL,
        'art_preg': admin.VERTICAL,
        'art_preg_type': admin.VERTICAL,
        'infant_ppx': admin.VERTICAL,
        'infant_ppx_type': admin.VERTICAL,
    }


@admin.register(InCare, site=ba_namotswe_admin)
class InCareAdmin(BaseCrfModelAdmin):
    form = InCareForm
    search_fields = ['pending_fields']
    radio_fields = {
        'attended': admin.VERTICAL,
        'weight_measured': admin.VERTICAL,
        'height_measured': admin.VERTICAL,
        'hospital': admin.VERTICAL,
        'disclosure_to_patient': admin.VERTICAL,
        'disclosure_to_others': admin.VERTICAL,
        'disclosure_by_caregiver': admin.VERTICAL,
    }


class LabTestInlineAdmin(BaseTabularInlineCrfModelAdmin):
    model = LabTest
    form = LabTestForm
    extra = 1


@admin.register(LabRecord, site=ba_namotswe_admin)
class LabRecordAdmin(BaseCrfModelAdmin):
    form = LabRecordForm
    inlines = [LabTestInlineAdmin]


class TransferInlineAdmin(BaseStackedInlineCrfModelAdmin):
    model = Transfer
    form = TransferForm
    extra = 0


@admin.register(TransferRecord, site=ba_namotswe_admin)
class TransferRecordAdmin(BaseCrfModelAdmin):
    form = TransferRecordForm
    inlines = [TransferInlineAdmin]


class PregnancyInlineAdmin(BaseTabularInlineCrfModelAdmin):
    model = Pregnancy
    extra = 1


@admin.register(PregnancyHistory, site=ba_namotswe_admin)
class PregnancyHistoryAdmin(BaseCrfModelAdmin):
    form = PregnancyHistoryForm
    inlines = [PregnancyInlineAdmin]


@admin.register(AdherenceCounselling, site=ba_namotswe_admin)
class AdherenceCounsellingAdmin(BaseCrfModelAdmin):
    form = AdherenceCounsellingForm
    radio_fields = {
        'relation': admin.VERTICAL,
    }


class OiInlineAdmin(BaseTabularInlineCrfModelAdmin):
    model = Oi
    form = OiForm
    extra = 1


@admin.register(OiRecord, site=ba_namotswe_admin)
class OiHistoryAdmin(BaseCrfModelAdmin):
    form = OiRecordForm
    inlines = [OiInlineAdmin]


class TbInlineAdmin(BaseTabularInlineCrfModelAdmin):
    model = Tb
    form = TbForm
    extra = 1


@admin.register(TbRecord, site=ba_namotswe_admin)
class TbRecordAdmin(BaseCrfModelAdmin):
    form = TBRecordForm
    inlines = [TbInlineAdmin]


class ArtRegimenInlineAdmin(BaseTabularInlineCrfModelAdmin):
    model = ArtRegimen
    form = ArtRegimenForm
    extra = 0


@admin.register(ArtRecord, site=ba_namotswe_admin)
class ArtRecordAdmin(BaseCrfModelAdmin):
    form = ArtRecordForm
    inlines = [ArtRegimenInlineAdmin]


@admin.register(SubjectConsent, site=ba_namotswe_admin)
class SubjectConsentAdmin(BaseModelAdmin):

    dashboard_type = 'subject'


class WhoDiagnosisInlineAdmin(BaseTabularInlineCrfModelAdmin):
    model = WhoDiagnosis
    form = WhoDiagnosisForm
    extra = 1


@admin.register(WhoStaging, site=ba_namotswe_admin)
class WhoStagingAdmin(BaseCrfModelAdmin):
    form = WhoStagingForm
    inlines = [WhoDiagnosisInlineAdmin]
    radio_fields = {
        'who_stage': admin.VERTICAL,
    }


@admin.register(WhoDiagnosis, site=ba_namotswe_admin)
class WhoDiagnosisAdmin(BaseCrfModelAdmin):
    form = WhoDiagnosisForm
