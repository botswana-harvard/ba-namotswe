from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.db.models.aggregates import Count
from edc_constants.constants import YES, NO


class VisitCodeListFilter(admin.SimpleListFilter):
    title = _('Visit code')

    parameter_name = 'visit_code'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request).values(
            'subject_visit__appointment__visit_code').annotate(
                Count('subject_visit__appointment__visit_code'))
        return [(item['subject_visit__appointment__visit_code'],
                 item['subject_visit__appointment__visit_code']) for item in qs]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(subject_visit__appointment__visit_code=self.value())
        return queryset


class PendingFieldsListFilter(admin.SimpleListFilter):
    title = _('Pending')

    parameter_name = 'pending_fields'

    def lookups(self, request, model_admin):
        return (
            (YES, 'Yes'),
            (NO, 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == YES:
            return queryset.filter(pending_fields__isnull=False)
        elif self.value() == NO:
            return queryset.filter(pending_fields__isnull=True)
        else:
            return queryset
