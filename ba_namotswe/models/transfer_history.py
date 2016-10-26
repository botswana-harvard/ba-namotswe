from .crf_model import CrfModel


class TransferHistory(CrfModel):

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'Transfer History'
        verbose_name_plural = 'Transfer History'
