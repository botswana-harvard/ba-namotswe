from django.db import models
from django.utils import timezone

from simple_history.models import HistoricalRecords

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_consent.field_mixins import PersonalFieldsMixin
from edc_consent.managers import ConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_identifier.subject.classes import SubjectIdentifier
from edc_registration.model_mixins import RegistrationMixin


class AlreadyAllocatedError(Exception):
    pass


class SubjectConsent(ConsentModelMixin, RegistrationMixin, PersonalFieldsMixin, BaseUuidModel):

    """This is a dummy consent added for schema completeness."""

    history = HistoricalRecords()

    consent = ConsentManager()

    objects = models.Manager()

    def __str__(self):
        return '{}'.format(self.subject_identifier)

    def natural_key(self):
        return (self.subject_identifier, )

    def save(self, *args, **kwargs):
        if not self.id:
            self.subject_identifier = SubjectIdentifier(
                site_code=self.study_site).get_identifier()
            self.consent_datetime = timezone.now()
        super(SubjectConsent, self).save(*args, **kwargs)

    class Meta(ConsentModelMixin.Meta):
        app_label = 'ba_namotswe'
        get_latest_by = 'consent_datetime'
        ordering = ('created', )
