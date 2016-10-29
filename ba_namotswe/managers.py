from django.db import models
from edc_constants.constants import UNKNOWN


class CrfInlineManager(models.Manager):

    def get_pending_fields(self):
        pending_fields = []
        for key, value in self.__dict__.items():
            if value == UNKNOWN:
                pending_fields.append(key)
        pending_fields.sort()
        return pending_fields
