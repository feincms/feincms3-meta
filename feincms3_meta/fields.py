from django.conf import settings


class StructuredDataProperty:
    def __init__(self, property, value=None, keyword=None, coerce=None):
        self.property = property
        self.value = value
        self.keyword = keyword
        self.coerce = coerce

    def to_ld_dict(self, obj):
        data = {}
        value = self.value(obj) if callable(self.value) else self.value
        value = self.coerce(obj, value) if self.coerce else value
        if not value:
            return data

        if self.keyword:
            data[self.property] = {self.keyword: value}
        else:
            data[self.property] = value

        return data


DEFAULT_PROPERTIES = getattr(
    settings,
    "DEFAULT_STRUCTURED_DATA_PROPERTIES",
    [
        StructuredDataProperty("@context", "https://schema.org/"),
        StructuredDataProperty("@type", "WebPageElement"),
    ],
)


class StructuredDataField(StructuredDataProperty):
    def __init__(self, field, property, *args, **kwargs):
        self.field = field
        super().__init__(property, *args, **kwargs)

    def contribute_to_class(self, cls, name):
        self.field.contribute_to_class(cls, name)
        self.value = lambda obj: getattr(obj, name)

        cls.structured_data_properties.append(self)
