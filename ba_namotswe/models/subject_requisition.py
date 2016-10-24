from django.core.urlresolvers import reverse
from django.db import models

from edc_lab.requisition.managers import RequisitionManager
from edc_lab.requisition.model_mixins import RequisitionModelMixin
from edc_visit_tracking.managers import CrfModelManager

from .crf_model import CrfModel
from .packing_list import PackingList


class SubjectRequisitionManager(CrfModelManager):

    def get_by_natural_key(self, requisition_identifier):
        return self.get(requisition_identifier=requisition_identifier)


class SubjectRequisition(RequisitionModelMixin, CrfModel):

    packing_list = models.ForeignKey(PackingList, null=True, blank=True)

    objects = RequisitionManager()

    def subject(self):
        return None

    def dashboard(self):
        """Returns a hyperink for the Admin page."""
        url = reverse(
            'subject_dashboard_url',
            kwargs={
                'subject_identifier': self.subject_visit.appointment.subject_identifier
            })
        ret = """<a href="{url}" >dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

    def get_visit(self):
        return self.subject_visit

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'Subject Requisition'
        verbose_name_plural = 'Subject Laboratory Requisition'
