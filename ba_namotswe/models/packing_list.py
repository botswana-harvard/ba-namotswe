from edc_base.model.models import BaseUuidModel
from edc_lab.packing.model_mixins import PackingListModelMixin


class PackingList(PackingListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'ba_namotswe'
        verbose_name = 'Packing List'
