class BootstrapFormMixin:
    widget_attrs = {"class": "form-control", "id": "floatingText"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(self.widget_attrs)
