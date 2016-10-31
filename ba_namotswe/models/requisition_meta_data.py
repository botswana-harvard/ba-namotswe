from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_metadata.model_mixins import RequisitionMetadataModelMixin

from .subject_requisition import SubjectRequisition


class RequisitionMetadata(RequisitionMetadataModelMixin, BaseUuidModel):

    class Meta(RequisitionMetadataModelMixin.Meta):
        app_label = 'ba_namotswe'

    @property
    def subject_requisition(self):
        subject_requisition = None
        try:
            subject_requisition = SubjectRequisition.objects.get(subject_visit__appointment__visit_code=self.visit_code, panel_name=self.panel_name)
        except SubjectRequisition.DoesNotExist:
            pass
        return subject_requisition
