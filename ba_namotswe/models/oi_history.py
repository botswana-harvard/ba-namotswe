from .crf_model import CrfModel


class OiHistory(CrfModel):

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'Opportunistic Infection History'
