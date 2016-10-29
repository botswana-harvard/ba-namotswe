from django.db import models

from .crf_model import CrfModelMixin, CrfInlineModelMixin


class PregnancyHistory(CrfModelMixin):

    class Meta(CrfModelMixin.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'Pregnancy History'
        verbose_name_plural = 'Pregnancy History'


class Pregnancy(CrfInlineModelMixin, models.Model):

    pregnancy_history = models.ForeignKey(PregnancyHistory)

    pregnancy_date = models.DateField(
        verbose_name='Date of first clinical documentation of pregnancy',
        null=True,
        blank=True)

    delivery_date = models.DateField(
        null=True,
        blank=True)

    def get_pending_fields(self):
        pending_fields = super(Pregnancy, self).get_pending_fields()
        if not self.pregnancy_date:
            pending_fields.append('pregnancy_date')
        if not self.delivery_date:
            pending_fields.append('delivery_date')
        pending_fields.sort()
        return pending_fields

    class Meta(CrfInlineModelMixin.Meta):
        app_label = 'ba_namotswe'
        verbose_name = 'Pregnancy'
        crf_inline_parent = 'pregnancy_history'
