from django.utils.functional import lazy

from feincms3_meta.utils import meta_tags


def test_meta(rf):
    request = rf.get('/')
    assert str(meta_tags(request=request)) == '''\
<meta property="og:type" content="website">
  <meta name="description" content="">'''

    lazy_url = lazy(lambda: '/', str)()
    assert str(meta_tags(url=lazy_url, request=request)) == '''\
<meta property="og:type" content="website">
  <meta property="og:url" content="http://testserver/">
  <meta name="description" content="">'''
