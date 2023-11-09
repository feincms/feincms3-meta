from types import SimpleNamespace

from django import test
from django.test.utils import override_settings
from django.utils.functional import lazy

from feincms3_meta.utils import MetaTags, meta_tags

from .models import Model, StructuredDataModel


class MetaTest(test.TestCase):
    def test_basic_meta_tags(self):
        request = test.RequestFactory().get("/")
        self.assertEqual(
            str(meta_tags(request=request)),
            """\
<meta property="og:type" content="website">\
<meta property="og:url" content="http://testserver/">""",
        )

        lazy_url = lazy(lambda: "/lazy/", str)()
        self.assertEqual(
            str(meta_tags(url=lazy_url, request=request)),
            """\
<meta property="og:type" content="website">\
<meta property="og:url" content="http://testserver/lazy/">""",
        )

        self.assertEqual(
            str(meta_tags(request=request, defaults={"title": "stuff"}, title="")),
            """\
<meta property="og:title" content="stuff">\
<meta property="og:type" content="website">\
<meta property="og:url" content="http://testserver/">""",
        )

        self.assertEqual(
            str(meta_tags(request=request, defaults={"title": "stuff"}, title=None)),
            """\
<meta property="og:type" content="website">\
<meta property="og:url" content="http://testserver/">""",
        )

    def test_model(self):
        m = Model()
        request = test.RequestFactory().get("/stuff/")
        self.assertEqual(
            str(meta_tags([m], request=request)),
            """\
<meta property="og:type" content="website">\
<meta property="og:url" content="http://testserver/stuff/">""",
        )

        m.meta_canonical = "/bla/"
        self.assertEqual(
            str(meta_tags([m], request=request)),
            """\
<meta property="og:type" content="website">\
<meta property="og:url" content="http://testserver/bla/">\
<link rel="canonical" href="http://testserver/bla/">""",
        )

        # meta_title not set, falling back to title
        m.title = "test"
        self.assertEqual(
            str(meta_tags([m], request=request)),
            """\
<meta property="og:title" content="test">\
<meta property="og:type" content="website">\
<meta property="og:url" content="http://testserver/bla/">\
<link rel="canonical" href="http://testserver/bla/">""",
        )

        m = Model()
        m.meta_title = "title-test"
        # Generate both name="description" and property="og:description"
        m.meta_description = "description-test"
        self.assertEqual(
            str(meta_tags([m], request=request)),
            """\
<meta property="og:description" content="description-test">\
<meta property="og:title" content="title-test">\
<meta property="og:type" content="website">\
<meta property="og:url" content="http://testserver/stuff/">\
<meta name="description" content="description-test">""",
        )

        # print(str(meta_tags([m], request=request)))

    def test_model_images(self):
        m = SimpleNamespace(
            meta_image=SimpleNamespace(opengraph="hello/world.jpg"),
            meta_image_alternative_text="",
        )
        self.assertEqual(
            Model.meta_images_dict(m),
            {
                "image": "hello/world.jpg",
                "image:width": 1200,
                "image:height": 630,
                "image:alt": "",
            },
        )

        m = SimpleNamespace(
            meta_image=None,
            image=SimpleNamespace(url="hello/world.jpg"),
        )
        self.assertEqual(
            Model.meta_images_dict(m),
            {"image": "hello/world.jpg"},
        )

        m = SimpleNamespace(meta_image=None)
        self.assertEqual(
            Model.meta_images_dict(m),
            {"image": ""},
        )

    def test_unknown_attribute_rendered(self):
        request = test.RequestFactory().get("/")
        self.assertEqual(
            str(meta_tags([], request=request, unknown="Stuff")),
            """\
<meta property="og:type" content="website">\
<meta property="og:url" content="http://testserver/">\
<meta name="unknown" content="Stuff">""",
        )

    @override_settings(
        META_TAGS={
            "site_name": "site",
            "title": "t",
            "description": "desc",
            "image": "/logo.png",
            "image:width": 1200,
            "image:height": 630,
            "image:alt": "Alternative text",
            "robots": "noindex",
        }
    )
    def test_setting(self):
        request = test.RequestFactory().get("/")
        self.assertEqual(
            str(meta_tags([], request=request)),
            """\
<meta property="og:description" content="desc">\
<meta property="og:image" content="http://testserver/logo.png">\
<meta property="og:image:width" content="1200">\
<meta property="og:image:height" content="630">\
<meta property="og:image:alt" content="Alternative text">\
<meta property="og:site_name" content="site">\
<meta property="og:title" content="t">\
<meta property="og:type" content="website">\
<meta property="og:url" content="http://testserver/">\
<meta name="description" content="desc">\
<meta name="robots" content="noindex">""",
        )

    @override_settings(META_TAGS=None)
    def test_setting_none(self):
        request = test.RequestFactory().get("/")
        self.assertEqual(
            str(meta_tags([], request=request)),
            """\
<meta property="og:type" content="website">\
<meta property="og:url" content="http://testserver/">""",
        )

    def test_as_dict(self):
        mt = MetaTags()
        self.assertEqual(str(mt), "")

        mt["url"] = "test"
        self.assertEqual(str(mt), '<meta property="og:url" content="test">')

    def test_no_quoting_of_safe_values(self):
        request = test.RequestFactory().get("/")
        self.assertEqual(
            str(meta_tags(request=request, defaults={"title": "stu'ff"}, title="")),
            """\
<meta property="og:title" content="stu'ff">\
<meta property="og:type" content="website">\
<meta property="og:url" content="http://testserver/">""",
        )
        self.assertEqual(
            str(meta_tags(request=request, defaults={"title": 'stu"ff'}, title="")),
            """\
<meta property="og:title" content="stu&quot;ff">\
<meta property="og:type" content="website">\
<meta property="og:url" content="http://testserver/">""",
        )

    def test_twitter_cards(self):
        request = test.RequestFactory().get("/")
        self.assertEqual(
            str(
                meta_tags(
                    [
                        {
                            "twitter:card": "summary",
                            "twitter:site": "@example",
                            "twitter:creator": "@example",
                            "_ignored_because_of_underscore": "yes",
                            "ignored_because_of_falsiness": "",
                        }
                    ],
                    request=request,
                )
            ),
            """\
<meta property="og:type" content="website">\
<meta property="og:url" content="http://testserver/">\
<meta name="twitter:card" content="summary">\
<meta name="twitter:site" content="@example">\
<meta name="twitter:creator" content="@example">\
""",
        )

    @override_settings(
        IMAGEFIELD_FORMATS={"testapp.model.meta_image": {"blub": ["default"]}}
    )
    def test_opengraph_format_check(self):
        errors = Model.check()
        self.assertEqual(
            [error.id for error in errors],
            ["feincms3_meta.E001"],
        )

    def test_expanded_json_ld_from_meta_model(self):
        m = Model()
        m.meta_title = "title-test"
        m.meta_description = "description-test"
        self.assertEqual(
            str(m.structured_data()),
            """\
<script type="application/ld+json">{"https://schema.org/title": {"@value": "title-test"}, "https://schema.org/description": {"@value": "description-test"}}</script>""",
        )

    def test_expanded_json_ld_fallback_test(self):
        m = Model()
        m.title = "fallback-title-test"
        self.assertEqual(
            str(m.structured_data()),
            """\
<script type="application/ld+json">{"https://schema.org/title": {"@value": "fallback-title-test"}}</script>""",
        )

    def test_expanded_json_ld_from_custom_model(self):
        m = StructuredDataModel()
        m.name = "name"
        self.assertEqual(
            str(m.structured_data()),
            """\
<script type="application/ld+json">{"https://schema.org/url": {"@id": "/slug/"}, "https://schema.org/name": {"@value": "name"}}</script>""",
        )
