==========
Change log
==========

`Next version`_
~~~~~~~~~~~~~~~

- Make all fields nullable.
- Switched to a declarative setup.
- Switched from Travis CI to GitHub actions.
- Changed the HTML generation to preserve single quotes etc. in Open Graph tags
  when it is safe to do so.


`3.0`_ (2019-06-21)
~~~~~~~~~~~~~~~~~~~

- Reinstated the support for ``og:site_name`` which was lost in the
  rework leading to 2.0.
- Added a `django-imagefield
  <https://github.com/matthiask/django-imagefield>`__ dependency which
  allows us to provide OpenGraph images in the best format.


`2.0`_ (2019-01-15)
~~~~~~~~~~~~~~~~~~~

- Reworked the internals of the utils module and made the API surface
  smaller.
- Added back support for the ``og:image:width`` and ``og:image:height``
  tags.


`1.5`_ (2019-01-12)
~~~~~~~~~~~~~~~~~~~

- Changed the meta tags dictionary to also build absolute URIs when
  calling ``update()`` after the ``meta_tags`` helper returns.
- Changed ``meta_tags`` to no longer produce a ``<meta
  name="description" content="">`` tag if the description is empty.
- Switched the preferred quote to ``"`` and started using `black
  <https://pypi.org/project/black/>`_ to automatically format Python
  code.
- Removed the deprecated ``meta_tags_html`` function.
- Added new fields for overriding the author and robots meta tags.


`1.4`_ (2018-05-01)
~~~~~~~~~~~~~~~~~~~

- Added the possibility to override values from ``META_TAGS`` using an
  additional ``defaults`` argument to ``meta_tags``.
- Converted the tests to the same structure the other feincms3 packages
  use, added a tox-based test and style checks while doing that.
- Increased test coverage.


`1.3`_ (2018-03-07)
~~~~~~~~~~~~~~~~~~~

- Made the return value of ``meta_tags`` a subclass of ``dict`` which
  renders meta tags as HTML.
- Added a deprecation warning to ``meta_tags_html``.


`1.2`_ (2018-02-09)
~~~~~~~~~~~~~~~~~~~

- Added support for OpenGraph tags with colons (e.g. ``image:width``
  and ``image:height``).
- Modified ``meta_tags`` (and by extension also ``meta_tags_html``) to
  handle keyword arguments differently: Falsy values are discarded,
  ``None`` causes the complete removal of the tag from the dictionary
  respectively from the HTML output.
- Separated the HTML rendering into ``format_meta_tags`` to make it
  reusable.


`1.1`_ (2017-05-03)
~~~~~~~~~~~~~~~~~~~

- Added more steps to the usage instructions.
- Converted the thing into a real package so that we can bundle
  translations etc. This also means that import paths have changed. The
  ``MetaMixin`` has to be imported from ``feincms3_meta.models``,
  ``meta_tags`` and ``meta_tags_html`` from ``feincms3_meta.utils``.


`1.0`_ (2017-03-28)
~~~~~~~~~~~~~~~~~~~

- Initial release!

.. _1.0: https://github.com/matthiask/feincms3-meta/commit/e50451b5661
.. _1.1: https://github.com/matthiask/feincms3-meta/compare/1.0...1.1
.. _1.2: https://github.com/matthiask/feincms3-meta/compare/1.1...1.2
.. _1.3: https://github.com/matthiask/feincms3-meta/compare/1.2...1.3
.. _1.4: https://github.com/matthiask/feincms3-meta/compare/1.3...1.4
.. _1.5: https://github.com/matthiask/feincms3-meta/compare/1.4...1.5
.. _2.0: https://github.com/matthiask/feincms3-meta/compare/1.5...2.0
.. _3.0: https://github.com/matthiask/feincms3-meta/compare/2.0...3.0
.. _Next version: https://github.com/matthiask/feincms3-meta/compare/3.0...master
