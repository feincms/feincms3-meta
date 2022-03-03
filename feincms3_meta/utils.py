import re

from django.conf import settings
from django.utils.html import escape, html_safe, mark_safe


TEMPLATES = {
    "opengraph": '<meta property="{name}" content="{content}">',
    "meta": '<meta name="{name}" content="{content}">',
    "link": '<link rel="{name}" href="{content}">',
}
TAGS = [
    ("opengraph", "og:description", "description"),
    ("opengraph", "og:image", "image"),
    ("opengraph", "og:image:width", "image:width"),
    ("opengraph", "og:image:height", "image:height"),
    ("opengraph", "og:image:alt", "image:alt"),
    ("opengraph", "og:site_name", "site_name"),
    ("opengraph", "og:title", "title"),
    ("opengraph", "og:type", "type"),
    ("opengraph", "og:url", "url"),
    ("meta", "description", "description"),
    ("meta", "author", "author"),
    ("meta", "robots", "robots"),
    ("link", "canonical", "canonical"),
]
URLS = {"canonical", "image", "url"}


_attribute_escapes = {
    ord("<"): "&lt;",
    ord(">"): "&gt;",
    ord("&"): "&amp;",
}


def escape_attribute(s):
    """
    Preserve single quotes etc. in attribute values if it is safe. Some user
    agents do not seem to interpret HTML entities in Open Graph values
    correctly.
    """
    if re.match(r"^[-\w\s_'&:;.,/()]+$", s, re.I | re.U):
        return s.translate(_attribute_escapes)
    return escape(s)


@html_safe
class MetaTags(dict):
    def __str__(self):
        """
        Return a safe HTML representation of the meta tag dictionary
        """
        uri = self.get("build_absolute_uri", lambda x: x)
        return mark_safe(
            "".join(
                TEMPLATES[template].format(
                    name=name,
                    content=escape_attribute(
                        uri(str(self[key])) if key in URLS else str(self[key])
                    ),
                )
                for template, name, key in TAGS
                if self.get(key)
            )
        )

    def update(self, other):
        if other:
            for key, value in other.items():
                if value is None:
                    self.pop(key, None)
                elif value:
                    self[key] = value
        return self

    def add(self, *dicts_or_meta_mixins, **kwargs):
        for thing in dicts_or_meta_mixins:
            self.update(thing.meta_dict() if hasattr(thing, "meta_dict") else thing)
        self.update(kwargs)
        return self


def meta_tags(objects=(), *, request, defaults=None, **kwargs):
    """
    Return a dictionary containing meta tag information. Keys include
    (but are not limited to):

    - ``title``
    - ``description``
    - ``image`` (Full URL)
    - ``canonical`` (Full URL)
    - ``url`` (Full URL, overridden using ``canonical``)
    - ``author``
    - ``robots``

    Data is taken in order from the following sources:

    - Any keyword arguments to this function (items with a value of ``None``
      are discarded)
    - Any ``MetaMixin`` instances passed as an iterable
    - The ``defaults`` argument, if given
    - The ``META_TAGS`` setting, if available

    The recommended set of keys for ``META_TAGS`` is ``site_name``,
    ``title``, ``description`` and ``image``. See
    `The Open Graph protocol <http://ogp.me/>`_ for additional details.
    """
    return MetaTags(
        build_absolute_uri=request.build_absolute_uri,
        type="website",
        url=request.get_full_path(),
    ).add(getattr(settings, "META_TAGS", None), defaults, *reversed(objects), **kwargs)
