from collections import OrderedDict

from django.views.generic import TemplateView
from django.urls.base import reverse
from django.apps.registry import apps

from edc_base.view_mixins import EdcBaseViewMixin

from ba_namotswe.models import RequisitionMetadata, CrfMetadata, Enrollment, Appointment, SubjectVisit


class SubjectDashboardView(EdcBaseViewMixin, TemplateView):

    template_name = 'ba_namotswe/subject_dashboard.html'

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
            'subject_visit': self.subject_visit,
            'dashboard_url': self.dashboard_url,
            'subject_identifier': self.subject_identifier,
            'demographics': self.demographics,
        })
        return self.context

    @property
    def crfs(self):
        if not self._crfs:
            if self.selected_appointment:
                self._crfs = []
                crfs = CrfMetadata.objects.filter(
                    subject_identifier=self.subject_identifier,
                    visit_code=self.selected_appointment.visit_code)
                for crf in crfs:
                    app_label, model_name = crf.model.split('.')
                    model = apps.get_app_config(app_label).get_model(model_name)
                    try:
                        obj = model.objects.get(
                            subject_visit__appointment=self.selected_appointment)
                        crf.instance = obj
#                         crf.url = obj.get_absolute_url()
                        crf.title = obj._meta.verbose_name
                    except model.DoesNotExist:
                        crf.instance = None
#                         crf.url = model().get_absolute_url()
                        crf.title = model()._meta.verbose_name
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
                'subject_dashboard_url',
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
        demographics.update({'age': self.enrollment.age_at_visit})
        demographics.update({'born': self.enrollment.dob.strftime('%Y-%m-%d')})
        demographics.update({'height': self.enrollment.height})
        demographics.update({'weight': self.enrollment.weight})
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
