from collections import OrderedDict

from django.views.generic import TemplateView
from django.urls.base import reverse

from edc_base.view_mixins import EdcBaseViewMixin

from ba_namotswe.models import RequisitionMetadata, CrfMetadata, Enrollment, Appointment, SubjectVisit
from ba_namotswe.models.entry_to_care import EntryToCare
from edc_metadata.constants import REQUIRED
from ba_namotswe.comment_form import CommentForm


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
            'enrollment_model': self.enrollment_model._meta.verbose_name,
            'comment_form': CommentForm()
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
                                obj.save(update_fields=['flagged'])
                            elif self.kwargs.get('toggle_status') == 'reviewed':
                                obj.reviewed = False if obj.reviewed else True
                                obj.save(update_fields=['reviewed'])
                        crf.url = obj.get_absolute_url()
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
        demographics = OrderedDict()
        demographics.update({'initials': self.enrollment.initials})
        demographics.update({'gender': self.enrollment.get_gender_display()})
        demographics.update({'age': self.enrollment.age_at_entry})
        demographics.update({'born': self.enrollment.dob.strftime('%Y-%m-%d')})
        try:
            demographics.update({'height': self.entry_to_care.entry_height})
            demographics.update({'weight': self.entry_to_care.entry_weight})
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
            entry_to_care = EntryToCare.objects.get(subject_visit=self.entry_subject_visit)
        except EntryToCare.DoesNotExist:
            entry_to_care = None
        return entry_to_care
