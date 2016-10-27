from django.db import models

from edc_constants.choices import YES_NO_UNKNOWN
from edc_constants.constants import UNKNOWN

from .crf_model import CrfModel


class EntryToCareChecklist(CrfModel):

    arv_changes = models.CharField(
        max_length=20,
        verbose_name='Has the patient had an changes to his/her ARV regimen since previous visit?',
        choices=YES_NO_UNKNOWN,
        default=UNKNOWN)
