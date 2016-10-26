from .crf_model import CrfModel


class TbHistory(CrfModel):

    class Meta(CrfModel.Meta):
        app_label = 'ba_namotswe'
