from django import test
from django.utils.functional import lazy

from feincms3_meta.utils import meta_tags

from .models import Model


class MetaTest(test.TestCase):
    def test_meta(self):
        request = test.RequestFactory().get('/')
        self.assertEqual(
            str(meta_tags(request=request)),
            '''\
<meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/">
  <meta name="description" content="">''')

        lazy_url = lazy(lambda: '/', str)()
        self.assertEqual(
            str(meta_tags(url=lazy_url, request=request)),
            '''\
<meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/">
  <meta name="description" content="">''')

        self.assertEqual(
            str(meta_tags(
                request=request,
                defaults={'title': 'stuff'},
                title=None,
            )),
            '''\
<meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/">
  <meta name="description" content="">''')

    def test_model(self):
        m = Model()
        request = test.RequestFactory().get('/stuff/')
        self.assertEqual(
            str(meta_tags([m], request=request)),
            '''\
<meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/stuff/">
  <meta name="description" content="">''')

        m.meta_canonical = '/bla/'
        self.assertEqual(
            str(meta_tags([m], request=request)),
            '''\
<meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/bla/">
  <meta name="description" content="">
  <link rel="canonical" href="http://testserver/bla/">''')

        # meta_title not set, falling back to title
        m.title = 'test'
        self.assertEqual(
            str(meta_tags([m], request=request)),
            '''\
<meta property="og:title" content="test">
  <meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/bla/">
  <meta name="description" content="">
  <link rel="canonical" href="http://testserver/bla/">''')

        # print(str(meta_tags([m], request=request)))
