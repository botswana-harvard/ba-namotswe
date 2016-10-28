from django.views.generic.base import TemplateView
from django.db.models import Q
from edc_base.view_mixins import EdcBaseViewMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

from ba_namotswe.search_form import SearchForm
from ba_namotswe.models.enrollment import Enrollment


class HomeView(EdcBaseViewMixin, TemplateView, FormView):

    template_name = 'ba_namotswe/home.html'
    form_class = SearchForm
    dashboard_url_name = 'subject_dashboard_url'

    def __init__(self, **kwargs):
        self.enrollments = Enrollment.objects.all().order_by('-report_datetime')[0:15]
        super(HomeView, self).__init__(**kwargs)

    def get_initial(self):
        initial = super(HomeView, self).get_initial()
        initial['search_term'] = self.kwargs.get('search_term') or self.kwargs.get('subject_identifier')
        return initial

    def form_valid(self, form):
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            try:
                self.enrollments = [Enrollment.objects.get(subject_identifier=search_term)]
            except Enrollment.DoesNotExist:
                self.enrollments = Enrollment.objects.filter(
                    Q(subject_identifier__icontains=search_term) |
                    Q(slh_identifier__icontains=search_term) |
                    Q(cm_identifier__icontains=search_term)).order_by('-report_datetime')
            if not self.enrollments:
                form.add_error('search_term', 'No matching records found.')
            context = self.get_context_data(form=form)
            context.update({
                'enrollments': self.enrollments})
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({'dashboard_url_name': self.dashboard_url_name})
        context.update({'enrollments': self.enrollments})
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)
