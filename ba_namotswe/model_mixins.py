from django.db import models
from django.urls import reverse
from django.utils.html import format_html

from edc_constants.constants import UNKNOWN


class DashboardModelMixin(models.Model):

    def dashboard(self):
        """Returns a hyperink for the Admin page."""
        options = {'subject_identifier': self.subject_identifier}
        try:
            options.update({'appointment_pk': str(self.appointment.pk)})
        except AttributeError:
            pass
        url = reverse('subject_dashboard_url', kwargs=options)
        ret = """<a href="{url}" role="button" class="btn btn-sm btn-primary">dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

    class Meta:
        abstract = True


class PendingFieldsModelMixin(models.Model):

    pending_fields = models.TextField(verbose_name='Pending', null=True, editable=False)

    def save(self, *args, **kwargs):
        if not kwargs.get('update_fields'):
            self.pending_fields = ', '.join(self.get_pending_fields())
        super(PendingFieldsModelMixin, self).save(*args, **kwargs)

    def get_pending_fields(self):
        pending_fields = []
        for key, value in self.__dict__.items():
            if value == UNKNOWN:
                pending_fields.append(key)
        pending_fields.sort()
        return pending_fields

    class Meta:
        abstract = True


class ReviewFieldsModelMixin(models.Model):

    edited = models.BooleanField(default=False, editable=False)

    flagged = models.BooleanField(default=False, editable=False)

    flagged_datetime = models.DateTimeField(null=True, editable=False)

    reviewed = models.BooleanField(default=False, editable=False)

    reviewed_datetime = models.DateTimeField(null=True, editable=False)

    no_report = models.BooleanField(default=False, editable=False)

    no_report_datetime = models.DateTimeField(null=True, editable=False)

    def save(self, *args, **kwargs):
        if not kwargs.get('update_fields'):
            self.edited = True
            self.reviewed = False
            self.reviewed_datetime = None
            self.no_report = False
            self.no_report_datetime = None
        super(ReviewFieldsModelMixin, self).save(*args, **kwargs)

    @property
    def flag(self):
        if self.flagged:
            return format_html('<span class="fa fa-flag"></span>')
        else:
            return None

    @property
    def NR(self):
        if self.no_report:
            return format_html('<span class="fa fa-minus-square"></span>')
        else:
            return None

    class Meta:
        abstract = True
