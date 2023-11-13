from django.conf import settings


class StructuredDataProperty:
    def __init__(self, property, value=None, keyword=None):
        self.property = property
        self.value = value
        self.keyword = keyword


DEFAULT_PROPERTIES = getattr(
    settings,
    "DEFAULT_STRUCTURED_DATA_PROPERTIES",
    [
        StructuredDataProperty("@context", "https://schema.org/"),
        StructuredDataProperty("@type", "WebPageElement"),
    ],
)


class StructuredDataField(StructuredDataProperty):
    def __init__(self, field, property, *args, fallback="", **kwargs):
        self.field = field
        self.fallback = fallback
        super().__init__(property, *args, **kwargs)

    def contribute_to_class(self, cls, name):
        self.field.contribute_to_class(cls, name)
        self.value = lambda obj: (
            getattr(obj, name)
            or (
                getattr(obj, self.fallback)
                if self.fallback and hasattr(obj, self.fallback)
                else None
            )
        )

        cls.structured_data_properties.append(self)
