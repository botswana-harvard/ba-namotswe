from django.db.models.signals import pre_save
from django.dispatch import receiver

from ba_namotswe.models.enrollment import Enrollment


@receiver(pre_save, sender=Enrollment, weak=False, dispatch_uid="create_dummy_consent_on_pre_save")
def create_dummy_consent_on_pre_save(sender, instance, raw, using, **kwargs):
    if not raw and not kwargs.get('update_fields'):
        try:
            instance.create_dummy_consent(instance.subject_identifier)
        except AttributeError as e:
            if 'create_dummy_consent' not in str(e):
                raise AttributeError(str(e))
