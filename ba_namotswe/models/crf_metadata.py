from django.apps import apps
from django.urls.base import reverse

from edc_base.model.models.base_uuid_model import BaseUuidModel

from edc_metadata.model_mixins import CrfMetadataModelMixin


class CrfMetadata(CrfMetadataModelMixin, BaseUuidModel):

    class Meta(CrfMetadataModelMixin.Meta):
        app_label = 'ba_namotswe'

    @property
    def crf_model_add_or_update(self):
        app_label, model_name = self.model.split('.')
        model = apps.get_app_config('ba_namotswe').get_model(model_name)
        obj = None
        try:
            obj = model.objects.get(subject_visit__appointment__subject_identifier=self.subject_identifier)
            admin_model_url_label = model._meta.verbose_name
            admin_model_change_url = obj.get_absolute_url()
            print(admin_model_url_label, admin_model_change_url)
            return (admin_model_url_label, admin_model_change_url)
        except model.DoesNotExist:
            admin_model_url_label = model._meta.verbose_name
            admin_model_add_url = reverse('admin:{}_{}_add'.format(app_label, model_name))
            print(admin_model_url_label, admin_model_add_url)
            return (admin_model_url_label, admin_model_add_url)
