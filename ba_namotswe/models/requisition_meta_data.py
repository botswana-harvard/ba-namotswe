from django.db import models

from ba_namotswe.models import Appointment

from edc_base.model.models.base_uuid_model import BaseUuidModel

from edc_metadata.model_mixins import (
    CrfMetadataModelMixin, RequisitionMetadataModelMixin)
from ba_namotswe.models.subject_requisition import SubjectRequisition


class RequisitionMetadata(RequisitionMetadataModelMixin, BaseUuidModel):

    appointment = models.ForeignKey(Appointment, related_name='+')

    class Meta(RequisitionMetadataModelMixin.Meta):
        app_label = 'ba_namotswe'

    @property
    def subject_requisition(self):
        subject_requisition = None
        try:
            subject_requisition = SubjectRequisition.objects.get(subject_visit__appointment=self.appointment, panel_name=self.panel_name)
        except SubjectRequisition.DoesNotExist:
            pass
        return subject_requisition


class CrfMetadata(CrfMetadataModelMixin, BaseUuidModel):

    appointment = models.ForeignKey(Appointment, related_name='+')

    class Meta(CrfMetadataModelMixin.Meta):
        app_label = 'ba_namotswe'
