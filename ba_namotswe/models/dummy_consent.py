from django.db import models
from edc_base.model.models.base_uuid_model import BaseUuidModel

from edc_consent.managers import ConsentManager

from simple_history.models import HistoricalRecords

from edc_consent.model_mixins import ConsentModelMixin
from django.utils import timezone


class AlreadyAllocatedError(Exception):
    pass


class DummyConsent(ConsentModelMixin, BaseUuidModel):

    history = HistoricalRecords()

    consent = ConsentManager()

    objects = models.Manager()

    def __str__(self):
        return '{}'.format(self.subject_identifier)

    def natural_key(self):
        return (self.subject_identifier, )

    def save(self, *args, **kwargs):
        self.consent_datetime = timezone.now()
        super(DummyConsent, self).save(*args, **kwargs)

    class Meta:
        app_label = 'ba_namotswe'
        get_latest_by = 'consent_datetime'
        ordering = ('created', )
