from .crf_model import CrfModel


class PregnancyHistory(CrfModel):

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'Pregnancy History'
        verbose_name_plural = 'Pregnancy History'
