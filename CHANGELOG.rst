==========
Change log
==========

`Next version`_
~~~~~~~~~~~~~~~

- Added support for OpenGraph tags with colons (e.g. ``image:width``
  and ``image:height``).
- Discard keyword arguments to ``meta_tags`` and ``meta_tags_html`` with
  a value of ``None``


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
.. _Next version: https://github.com/matthiask/feincms3-meta/compare/1.1...master
