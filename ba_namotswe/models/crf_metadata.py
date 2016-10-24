from django.apps.registry import apps
from django.urls.base import reverse

from edc_base.model.models.base_uuid_model import BaseUuidModel

from edc_metadata.model_mixins import CrfMetadataModelMixin


class CrfMetadata(CrfMetadataModelMixin, BaseUuidModel):

    class Meta(CrfMetadataModelMixin.Meta):
        app_label = 'ba_namotswe'

    def get_absolute_url(self):
        app_label, model_name = self.model.split('.')
        model = apps.get_app_config(app_label).get_model(model_name)
        obj = None
        try:
            obj = model.objects.get(subject_visit__appointment__visit_code=self.visit_code, subject_visit__appointment__subject_identifier=self.subject_identifier)
            if obj.id:
                return reverse(
                    'ba_namotswe_admin:{}_{}_change'.format(app_label, model_name), args=[str(obj.id)])
        except model.DoesNotExist:
            return reverse('ba_namotswe_admin:{}_{}_add'.format(app_label, model_name))
