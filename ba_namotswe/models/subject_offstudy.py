from django.db import models

from edc_offstudy.model_mixins import OffstudyModelMixin
from edc_base.model.models import BaseUuidModel, HistoricalRecords


class SubjectOffstudy(OffstudyModelMixin, BaseUuidModel):

    objects = models.Manager()

    history = HistoricalRecords()

    class Meta:
        app_label = 'ba_namotswe'
        visit_schedule_name = 'subject_visit_schedule'
        consent_model = 'ba_namotswe.subjectconsent'
