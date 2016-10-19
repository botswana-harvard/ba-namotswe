from edc_lab.aliquot.aliquot_type import AliquotType


class AliquotType(AliquotType):

    class Meta:
        app_label = 'ba_namotswe_lab'
        ordering = ["name"]
