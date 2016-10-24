from edc_base.model.models.base_uuid_model import BaseUuidModel

from edc_metadata.model_mixins import CrfMetadataModelMixin


class CrfMetadata(CrfMetadataModelMixin, BaseUuidModel):

    class Meta(CrfMetadataModelMixin.Meta):
        app_label = 'ba_namotswe'
