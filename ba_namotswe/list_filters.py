from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.db.models.aggregates import Count
from edc_constants.constants import YES, NO


class VisitCodeListFilter(admin.SimpleListFilter):
    title = _('Visit code')

    parameter_name = 'visit_code'

    def lookups(self, request, model_admin):
        inline_attr = self.get_inline_attr(model_admin)
        qs = model_admin.get_queryset(request).values(
            '{}subject_visit__appointment__visit_code'.format(inline_attr)).annotate(
                Count('{}subject_visit__appointment__visit_code'.format(inline_attr)))
        return [(item['{}subject_visit__appointment__visit_code'.format(inline_attr)],
                 item['{}subject_visit__appointment__visit_code'.format(inline_attr)]) for item in qs]

    def queryset(self, request, queryset):
        inline_attr = self.get_inline_attr(queryset)
        if self.value():
            return queryset.filter(**{'{}subject_visit__appointment__visit_code'.format(inline_attr): self.value()})
        return queryset

    def get_inline_attr(self, model_admin):
        try:
            return model_admin.model._meta.crf_inline_parent + '__'
        except AttributeError:
            return ''


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
