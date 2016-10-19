from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView

from edc_base.views import EdcBaseViewMixin

from .appointment_visit_crf_view_mixin import AppointmentSubjectVisitCRFViewMixin
from .locator_results_actions_view_mixin import LocatorResultsActionsViewMixin
from .marquee_view_mixin import MarqueeViewMixin


class SubjectDashboardView(
        AppointmentSubjectVisitCRFViewMixin,
        MarqueeViewMixin, LocatorResultsActionsViewMixin, EdcBaseViewMixin, TemplateView):

    def __init__(self, **kwargs):
        super(SubjectDashboardView, self).__init__(**kwargs)
        self.request = None
        self.context = {}
        self.show = None
        self.template_name = 'ba_namotswe/subject_dashboard.html'

    def get_context_data(self, **kwargs):
        self.context = super().get_context_data(**kwargs)
        self.context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE,
            site_header=admin.site.site_header,
        )
        self.context.update({
            'markey_data': {},
            'markey_next_row': {},
            'requisitions_meta_data': self.requisitions_meta_data,
            'scheduled_forms': self.scheduled_forms,
            'appointments': self.appointments,
            'subject_identifier': self.subject_identifier,
        })
        return self.context

    def get(self, request, *args, **kwargs):
        self.request = request
        context = self.get_context_data(**kwargs)
        self.show = request.GET.get('show', None)
        context.update({'show': self.show})
        return self.render_to_response(context)

    @property
    def scheduled_forms(self):
        return {}

    @property
    def requisitions_meta_data(self):
        return {}

    @property
    def show_forms(self):
        show = self.request.GET.get('show', None)
        return True if show == 'forms' else False

    @property
    def subject_identifier(self):
        return self.context.get('subject_identifier')
