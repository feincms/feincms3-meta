from __future__ import unicode_literals

import warnings

from django.conf import settings
from django.utils.html import format_html, html_safe, mark_safe


@html_safe
class MetaTags(dict):
    def __str__(self):
        return format_meta_tags(self)


def meta_tags(
        objects=(),
        *,
        request,
        url_keys=('canonical', 'image', 'url'),
        **kwargs):
    """
    Return a dictionary containing meta tag information: Keys include
    (but are not limited to):

    - ``title``
    - ``description``
    - ``image`` (Full URL)
    - ``canonical`` (Full URL)
    - ``url`` (Full URL, overridden using ``canonical``)

    Data is taken in order from the following sources:

    - Any keyword arguments to this function (items with a value of ``None``
      are discarded)
    - Any ``MetaMixin`` instances passed as an iterable
    - The ``META_TAGS`` setting, if available

    URLs (all keys in ``url_keys``) are passed through
    ``request.build_absolute_uri``.

    The recommended set of keys for ``META_TAGS`` is ``site_name``,
    ``title``, ``description`` and ``image``. See
    `The Open Graph protocol <http://ogp.me/>`_ for additional details.
    """
    meta = MetaTags(type='website')
    meta.update(getattr(settings, 'META_TAGS', {}))

    for object in reversed(objects):
        meta['title'] = object.meta_title or object.title
        if object.meta_description:
            meta['description'] = object.meta_description
        if object.meta_image:
            meta['image'] = object.meta_image.url
        elif getattr(object, 'image', None):
            meta['image'] = object.image.url
        if object.meta_canonical:
            meta['canonical'] = object.meta_canonical
            meta['url'] = object.meta_canonical
        else:
            meta['url'] = request.get_full_path()

    for key, value in kwargs.items():
        if value:
            meta[key] = value
        elif value is None and key in meta:
            del meta[key]

    for key in url_keys:
        if meta.get(key):
            meta[key] = request.build_absolute_uri(meta[key])

    return meta


def format_meta_tags(meta):
    """
    Return a safe HTML representation of the meta tag dictionary
    """
    html = [
        format_html('<meta property="og:{}" content="{}">', key, value)
        for key, value in sorted(meta.items())
        if key not in ('canonical',) and value is not None
    ]
    html.append(
        format_html(
            '<meta name="description" content="{}">',
            meta.get('description', ''),
        )
    )
    if meta.get('canonical'):
        html.append(
            format_html(
                '<link rel="canonical" href="{}">',
                meta['canonical'],
            )
        )

    return mark_safe('\n  '.join(html))


def meta_tags_html(*args, **kwargs):
    """
    Return meta tags

    This function has the same signature as ``meta_tags`` above.
    """
    warnings.warn(
        'Use meta_tags instead of meta_tags_html; its return value is also'
        ' directly usable to render all meta tags at once.',
        DeprecationWarning,
        stacklevel=1,
    )
    return meta_tags(*args, **kwargs)
