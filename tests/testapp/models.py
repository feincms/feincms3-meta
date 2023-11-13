from django.db import models

# from django.utils.translation import gettext_lazy as _
from feincms3_meta.fields import StructuredDataField, StructuredDataProperty
from feincms3_meta.models import MetaMixin, StructuredDataMixin


class Model(MetaMixin):
    pass


class NaiveStructuredDataModel(StructuredDataMixin):
    name = StructuredDataField(
        models.CharField(max_length=50), "https://schema.org/name"
    )


class StructuredDataModel(StructuredDataMixin):
    name = StructuredDataField(models.CharField(max_length=50), "name")

    def get_absolute_url(self):
        return "/slug/"

    structured_data_properties = [
        StructuredDataProperty("@context", "https://schema.org/"),
        StructuredDataProperty("@type", "WebPageElement"),
        StructuredDataProperty("url", get_absolute_url, "@id"),
    ]
