from django.db.models.signals import post_save
from django.dispatch import receiver

from .enrollment import Enrollment


@receiver(post_save, sender=Enrollment, weak=False, dispatch_uid="create_dummy_consent_on_post_save")
def create_dummy_consent_on_post_save(sender, instance, raw, using, **kwargs):
    if not raw and not kwargs.get('update_fields'):
        try:
            if instance.is_eligible and not instance.subject_identifier:
                instance.subject_identifier = instance.subject_consent.subject_identifier
                instance.save(update_fields=['subject_identifier'])
        except AttributeError as e:
            if 'subject_consent' not in str(e):
                raise AttributeError(str(e))
