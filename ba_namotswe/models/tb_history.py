from .crf_model import CrfModel


class TbHistory(CrfModel):

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'Tuberculosis Infection History'
        verbose_name_plural = 'Tuberculosis Infection History'
