from collections import OrderedDict

from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin

from ba_namotswe.models import RequisitionMetadata, CrfMetadata, Enrollment, Appointment


class SubjectDashboardView(EdcBaseViewMixin, TemplateView):

    template_name = 'ba_namotswe/subject_dashboard.html'

    def __init__(self, **kwargs):
        super(SubjectDashboardView, self).__init__(**kwargs)
        self._selected_appointment = None
        self._appointments = None
        self.show = None

    def get_context_data(self, **kwargs):
        self.context = super(SubjectDashboardView, self).get_context_data(**kwargs)
        self.context.update({
            'requisitions': self.requisitions,
            'crfs': self.crfs,
            'appointments': self.appointments,
            'selected_appointment': self.selected_appointment,
            'subject_identifier': self.subject_identifier,
            'demographics': self.demographics,
        })
        return self.context

    def get(self, request, *args, **kwargs):
        self.request = request
        context = self.get_context_data(**kwargs)
        self.show = request.GET.get('show', None)
        context.update({'show': self.show})
        return self.render_to_response(context)

    @property
    def crfs(self):
        crfs = None
        if self.selected_appointment:
            crfs = CrfMetadata.objects.filter(
                subject_identifier=self.subject_identifier, visit_code=self.selected_appointment.visit_code)
        return crfs

    @property
    def requisitions(self):
        requisitions = None
        if self.selected_appointment:
            requisitions = RequisitionMetadata.objects.filter(
                subject_identifier=self.subject_identifier, visit_code=self.selected_appointment.visit_code, )
        return requisitions

#     @property
#     def show_forms(self):
#         show = self.request.GET.get('show', None)
#         return True if show == 'forms' else False

    @property
    def subject_identifier(self):
        return self.context.get('subject_identifier')

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
