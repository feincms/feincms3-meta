=============
feincms3-meta
=============

Helpers and mixins for making meta and `open graph`_ tags less annoying.

Usage
=====

1. Inherit ``feincms3_meta.MetaMixin``
2. Use the dictionary returned by ``feincms3_meta.meta_tags`` or even the
   HTML fragment returned by ``feincms3_meta.meta_tags_html`` in your
   project::

    return render(request, ..., {
        ...
        'meta_tags': meta_tags_html(
            [object],
            request=request,
        ),
    })

.. _open graph: http://ogp.me/