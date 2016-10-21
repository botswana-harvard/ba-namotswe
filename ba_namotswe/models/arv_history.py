from edc_base.model.models import BaseUuidModel


class ArvHistory(BaseUuidModel):

    class Meta:
        app_label = 'ba_namotswe'
        verbose_name = 'ARV History'
