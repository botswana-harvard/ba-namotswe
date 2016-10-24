from .crf_model import CrfModel


class ArvHistory(CrfModel):

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'ARV History'
