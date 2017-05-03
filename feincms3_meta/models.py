from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class MetaMixin(models.Model):
    meta_title = models.CharField(
        _('title'),
        max_length=200,
        blank=True,
        help_text=_('Used for Open Graph and other meta tags.'),
    )
    meta_description = models.TextField(
        _('description'),
        blank=True,
        help_text=_('Override the description for this page.'),
    )
    meta_image = models.ImageField(
        _('image'),
        blank=True,
        upload_to='meta/%Y/%m',
        help_text=_('Set the Open Graph image.'),
    )
    meta_canonical = models.URLField(
        _('canonical URL'),
        blank=True,
        help_text=_('If you need this you probably know.'),
    )

    class Meta:
        abstract = True

    @classmethod
    def admin_fieldset(cls, **kwargs):
        cfg = {
            'fields': (
                'meta_title', 'meta_description', 'meta_image',
                'meta_canonical',
            ),
            'classes': ('tabbed',),
        }
        cfg.update(kwargs)
        return (_('Meta tags'), cfg)
