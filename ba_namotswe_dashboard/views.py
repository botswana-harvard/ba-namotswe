from collections import OrderedDict

from django.views.generic import TemplateView
from django.urls.base import reverse

from edc_base.view_mixins import EdcBaseViewMixin

from ba_namotswe.models import RequisitionMetadata, CrfMetadata, Enrollment, Appointment, SubjectVisit
from ba_namotswe.models.entry_to_care import EntryToCare
from edc_metadata.constants import REQUIRED
from edc_constants.constants import OTHER
from edc_base.utils.age import formatted_age
from django.utils import timezone
from ba_namotswe.models.death import Death
from ba_namotswe.models.lost_to_followup import LostToFollowup
# from ba_namotswe.comment_form import CommentForm


class SubjectDashboardView(EdcBaseViewMixin, TemplateView):

    template_name = 'ba_namotswe/subject_dashboard.html'
    enrollment_model = Enrollment
    dashboard_url_name = 'subject_dashboard_url'

    def __init__(self, **kwargs):
        super(SubjectDashboardView, self).__init__(**kwargs)
        self._appointments = None
        self._crfs = None
        self._selected_appointment = None
        self._subject_visit = None

    def get_context_data(self, **kwargs):
        self.context = super(SubjectDashboardView, self).get_context_data(**kwargs)
        enrollment = self.enrollment_model.objects.get(subject_identifier=self.subject_identifier)
        try:
            death = Death.objects.get(subject_identifier=self.subject_identifier)
        except Death.DoesNotExist:
            death = Death()
        try:
            lost_to_followup = LostToFollowup.objects.get(subject_identifier=self.subject_identifier)
        except LostToFollowup.DoesNotExist:
            lost_to_followup = LostToFollowup()
        self.context.update({
            'requisitions': self.requisitions,
            'crfs': self.crfs,
            'appointments': self.appointments,
            'selected_appointment': self.selected_appointment,
            'selected_crf': self.kwargs.get('selected_crf'),
            'subject_visit': self.subject_visit,
            'dashboard_url': self.dashboard_url,
            'subject_identifier': self.subject_identifier,
            'demographics': self.demographics,
            'enrollment_model_name': self.enrollment_model._meta.verbose_name,
            'enrollment': enrollment,
            'death': death,
            'lost_to_followup': lost_to_followup,
        })
        return self.context

    @property
    def crfs(self):
        if not self._crfs:
            if self.selected_appointment:
                self._crfs = []
                crfs = CrfMetadata.objects.filter(
                    subject_identifier=self.subject_identifier,
                    visit_code=self.selected_appointment.visit_code).order_by('show_order')
                for crf in crfs:
                    try:
                        obj = crf.model_class.objects.get(subject_visit=self.subject_visit)
                    except crf.model_class.DoesNotExist:
                        if crf.entry_status == REQUIRED:
                            obj = crf.model_class.objects.create(subject_visit=self.subject_visit)
                            obj.edited = False
                            obj.save(update_fields=['edited'])
                        else:
                            obj = None
                            crf.url = None
                            crf.instance = None
                    if obj:
                        if self.kwargs.get('selected_crf') == crf.model:
                            if self.kwargs.get('toggle_status') == 'flagged':
                                obj.flagged = False if obj.flagged else True
                                obj.flagged_datetime = timezone.now()
                                obj.save(update_fields=['flagged', 'flagged_datetime'])
                            elif self.kwargs.get('toggle_status') == 'reviewed':
                                obj.reviewed = False if obj.reviewed else True
                                obj.reviewed_datetime = timezone.now()
                                obj.save(update_fields=['reviewed', 'reviewed_datetime'])
                            elif self.kwargs.get('toggle_status') == 'no_report':
                                obj.no_report = False if obj.no_report else True
                                obj.no_report_datetime = timezone.now()
                                obj.edited = True
                                obj.save(update_fields=['no_report', 'no_report_datetime', 'edited'])
                        crf.url = obj.get_absolute_url()
                        crf.changelist_url = reverse('{}:{}_{}_changelist'.format(
                            crf.model_class.ADMIN_SITE_NAME, *crf.model_class._meta.label_lower.split('.')))
                        crf.instance = obj
                    crf.title = crf.model_class()._meta.verbose_name
                    self._crfs.append(crf)
        return self._crfs

    @property
    def requisitions(self):
        requisitions = None
        if self.selected_appointment:
            requisitions = RequisitionMetadata.objects.filter(
                subject_identifier=self.subject_identifier, visit_code=self.selected_appointment.visit_code, )
        return requisitions

    @property
    def dashboard_url(self):
        try:
            dashboard_url = reverse(
                self.dashboard_url_name,
                kwargs={
                    'subject_identifier': self.subject_identifier,
                    'appointment_pk': self.selected_appointment.pk})
        except AttributeError:
            dashboard_url = None
        return dashboard_url

    @property
    def subject_identifier(self):
        return self.kwargs.get('subject_identifier')

    @property
    def enrollment(self):
        try:
            enrollment = Enrollment.objects.get(subject_identifier=self.subject_identifier)
        except Enrollment.DoesNotExist:
            enrollment = None
        return enrollment

    @property
    def demographics(self):
        if self.enrollment.caregiver_relation == OTHER:
            caregiver = self.enrollment.get_caregiver_relation_other
        else:
            caregiver = self.enrollment.get_caregiver_relation_display()
        demographics = OrderedDict()
        demographics.update({'initials': self.enrollment.initials})
        demographics.update({'gender': self.enrollment.get_gender_display()})
        demographics.update({'age': self.enrollment.age})
        demographics.update({'born': self.enrollment.dob.strftime('%Y-%m-%d')})
        demographics.update({'caregiver': caregiver})
        try:
            demographics.update({'height': self.entry_to_care.height})
            demographics.update({'weight': self.entry_to_care.weight})
            try:
                demographics.update({
                    'Entry-to-care':
                        (self.entry_to_care.entry_date.strftime('%Y-%m-%d') + '/' +
                         formatted_age(self.enrollment.dob, self.entry_to_care.entry_date))})
            except AttributeError:
                pass
            try:
                demographics.update({
                    'HIV Dx':
                        (self.entry_to_care.hiv_dx_date.strftime('%Y-%m-%d') + '/' +
                         formatted_age(self.enrollment.dob, self.entry_to_care.hiv_dx_date))})
            except AttributeError:
                pass
            try:
                demographics.update({
                    'ART init':
                        (self.entry_to_care.art_init_date.strftime('%Y-%m-%d') + '/' +
                         formatted_age(self.enrollment.dob, self.entry_to_care.art_init_date))})

            except AttributeError:
                pass
        except AttributeError:
            pass
        return demographics

    @property
    def subject_visit(self):
        if not self._subject_visit:
            try:
                self._subject_visit = SubjectVisit.objects.get(appointment=self.selected_appointment)
            except SubjectVisit.DoesNotExist:
                self._subject_visit = None
        return self._subject_visit

    @property
    def entry_appointment(self):
        return Appointment.objects.filter(subject_identifier=self.subject_identifier).first()

    @property
    def entry_subject_visit(self):
        if not self._entry_subject_visit:
            try:
                self._entry_subject_visit = SubjectVisit.objects.get(appointment=self.entry_appointment)
            except SubjectVisit.DoesNotExist:
                self._entry_subject_visit = None
        return self._entry_subject_visit

    @property
    def selected_appointment(self):
        if not self._selected_appointment:
            try:
                self._selected_appointment = Appointment.objects.get(pk=self.kwargs.get('appointment_pk'))
            except Appointment.DoesNotExist:
                self._selected_appointment = None
        return self._selected_appointment

    @property
    def appointments(self):
        if not self._appointments:
            try:
                self._appointments = [Appointment.objects.get(pk=self.kwargs.get('appointment_pk'))]
            except Appointment.DoesNotExist:
                self._appointments = Appointment.objects.filter(
                    subject_identifier=self.subject_identifier).order_by('visit_code')
        return self._appointments

    @property
    def entry_to_care(self):
        try:
            entry_to_care = EntryToCare.objects.get(subject_visit=self.subject_visit)
        except EntryToCare.DoesNotExist:
            entry_to_care = None
        return entry_to_care
