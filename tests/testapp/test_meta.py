from django import test
from django.utils.functional import lazy

from feincms3_meta.utils import meta_tags

from .models import Model


class MetaTest(test.TestCase):
    def test_meta(self):
        request = test.RequestFactory().get("/")
        self.assertEqual(
            str(meta_tags(request=request)),
            """\
<meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/">""",
        )

        lazy_url = lazy(lambda: "/", str)()
        self.assertEqual(
            str(meta_tags(url=lazy_url, request=request)),
            """\
<meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/">""",
        )

        self.assertEqual(
            str(meta_tags(request=request, defaults={"title": "stuff"}, title=None)),
            """\
<meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/">""",
        )

    def test_model(self):
        m = Model()
        request = test.RequestFactory().get("/stuff/")
        self.assertEqual(
            str(meta_tags([m], request=request)),
            """\
<meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/stuff/">""",
        )

        m.meta_canonical = "/bla/"
        self.assertEqual(
            str(meta_tags([m], request=request)),
            """\
<meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/bla/">
  <link rel="canonical" href="http://testserver/bla/">""",
        )

        # meta_title not set, falling back to title
        m.title = "test"
        self.assertEqual(
            str(meta_tags([m], request=request)),
            """\
<meta property="og:title" content="test">
  <meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/bla/">
  <link rel="canonical" href="http://testserver/bla/">""",
        )

        m = Model()
        m.meta_title = "title-test"
        # Generate both name="description" and property="og:description"
        m.meta_description = "description-test"
        self.assertEqual(
            str(meta_tags([m], request=request)),
            """\
<meta property="og:description" content="description-test">
  <meta property="og:title" content="title-test">
  <meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/stuff/">
  <meta name="description" content="description-test">""",
        )

        # print(str(meta_tags([m], request=request)))
