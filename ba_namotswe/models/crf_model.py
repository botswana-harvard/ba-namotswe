from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_visit_tracking.model_mixins import CrfModelMixin

from .subject_visit import SubjectVisit


class CrfModel(CrfModelMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`MaternalVisit`). """

    visit_model_attr = 'subject_visit'

    subject_visit = models.OneToOneField(SubjectVisit)

    class Meta:
        consent_model = 'ba_namotswe.subjectconsent'
        abstract = True
