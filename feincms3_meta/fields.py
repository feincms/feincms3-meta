class StructuredDataProperty:
    def __init__(self, attribute, property, keyword="@value"):
        self.attribute = attribute
        self.property = property
        self.keyword = keyword


class StructuredDataField(StructuredDataProperty):
    def __init__(self, field, *args, fallback="", **kwargs):
        self.field = field
        self.fallback = fallback
        super().__init__(field, *args, **kwargs)

    def contribute_to_class(self, cls, name):
        self.field.contribute_to_class(cls, name)
        self.attribute = lambda obj: (
            getattr(obj, name)
            or (
                getattr(obj, self.fallback)
                if self.fallback and hasattr(obj, self.fallback)
                else None
            )
        )

        if not hasattr(cls, "structured_data_properties"):
            cls.structured_data_properties = []

        cls.structured_data_properties.append(self)
