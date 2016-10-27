from django.views.generic.base import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

from ba_namotswe.search_form import SearchForm
from ba_namotswe.models.enrollment import Enrollment


class HomeView(EdcBaseViewMixin, TemplateView, FormView):

    template_name = 'ba_namotswe/home.html'
    form_class = SearchForm

    def __init__(self, **kwargs):
        self.enrollment = None
        super(HomeView, self).__init__(**kwargs)

    def get_initial(self):
        initial = super(HomeView, self).get_initial()
        initial['subject_identifier'] = self.kwargs.get('subject_identifier')
        return initial

    def form_valid(self, form):
        if form.is_valid():
            subject_identifier = form.cleaned_data['subject_identifier']
            try:
                self.enrollment = Enrollment.objects.get(subject_identifier=subject_identifier)
            except Enrollment.DoesNotExist:
                form.add_error('subject_identifier', 'Enrollment not found. Please search again or add a new patient.')
            context = self.get_context_data(form=form)
            context.update({
                'enrollment': self.enrollment})
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({'enrollment': self.enrollment})
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)
