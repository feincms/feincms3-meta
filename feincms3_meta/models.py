from django.core import checks
from django.db import models
from django.utils.html import format_html, mark_safe
from django.utils.translation import gettext_lazy as _
from imagefield.fields import ImageField

from feincms3_meta.fields import (
    DEFAULT_PROPERTIES,
    StructuredDataField,
    StructuredDataProperty,
)
from feincms3_meta.utils import escape_json


class StructuredDataMixin(models.Model):
    structured_data_properties = DEFAULT_PROPERTIES

    class Meta:
        abstract = True

    def structured_data_json(self, **kwargs):
        data = {}

        for sdp in self.structured_data_properties:
            value = sdp.value(self, **kwargs) if callable(sdp.value) else sdp.value
            if not value:
                continue

            if sdp.keyword:
                data[sdp.property] = {sdp.keyword: value}
            else:
                data[sdp.property] = value

        return escape_json(data)

    def structured_data(self, **kwargs):
        json_str = self.structured_data_json(**kwargs)
        html_template = '<script type="application/ld+json">{}</script>'
        return format_html(html_template, *(mark_safe(json_str),))


class MetaMixin(StructuredDataMixin):
    structured_data_properties = [
        StructuredDataProperty("@context", "https://schema.org/"),
        StructuredDataProperty("@type", "WebPage"),
    ]

    meta_title = StructuredDataField(
        models.CharField(
            _("title"),
            max_length=200,
            blank=True,
            default="",
            help_text=_("Used for Open Graph and other meta tags."),
        ),
        "title",
        fallback="title",
    )
    meta_description = StructuredDataField(
        models.TextField(
            _("description"),
            blank=True,
            default="",
            help_text=_("Override the description for this page."),
        ),
        "description",
    )
    meta_image = ImageField(
        _("image"),
        blank=True,
        default="",
        auto_add_fields=True,
        upload_to="meta/%Y/%m",
        help_text=_("Set the Open Graph image."),
        formats={"opengraph": ("default", ("crop", (1200, 630)))},
    )
    meta_image_alternative_text = models.CharField(
        _("alternative text"),
        blank=True,
        default="",
        help_text=_("Describe the contents, e.g. for screenreaders."),
        max_length=1000,
    )
    meta_canonical = models.URLField(
        _("canonical URL"),
        blank=True,
        default="",
        help_text=_("If you need this you probably know."),
    )
    meta_author = models.CharField(
        _("author"),
        blank=True,
        default="",
        help_text=_("Override the author meta tag."),
        max_length=200,
    )
    meta_robots = models.CharField(
        _("robots"),
        blank=True,
        default="",
        help_text=_("Override the robots meta tag."),
        max_length=200,
    )

    class Meta:
        abstract = True

    @classmethod
    def admin_fieldset(cls, **kwargs):
        cfg = {
            "fields": (
                "meta_title",
                "meta_description",
                "meta_image",
                "meta_image_ppoi",
                "meta_image_alternative_text",
                "meta_canonical",
                "meta_author",
                "meta_robots",
            ),
            "classes": ("tabbed",),
        }
        cfg.update(kwargs)
        return (_("Meta tags"), cfg)

    def meta_dict(self):
        ctx = {
            "title": self.meta_title or getattr(self, "title", ""),
            "description": self.meta_description,
            "canonical": self.meta_canonical,
            # Override URL if canonical is set to a non-empty value (the empty
            # string will be skipped when merging this dictionary)
            "url": self.meta_canonical,
            "author": self.meta_author,
            "robots": self.meta_robots,
        }
        ctx.update(self.meta_images_dict())
        return ctx

    def meta_images_dict(self):
        if self.meta_image:
            return {
                "image": str(self.meta_image.opengraph),
                "image:width": 1200,
                "image:height": 630,
                "image:alt": self.meta_image_alternative_text,
            }

        elif getattr(self, "image", None):
            return {"image": self.image.url}

        return {"image": ""}

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        meta_image = cls._meta.get_field("meta_image")
        if "opengraph" not in meta_image.formats:
            errors.append(
                checks.Error(
                    'The "opengraph" image format doesn\'t exist',
                    obj=cls,
                    id="feincms3_meta.E001",
                    hint=f'Check IMAGEFIELD_FORMATS and possibly remove the "{cls._meta.label_lower}.meta_image" configuration alltogether.',
                )
            )
        return errors
