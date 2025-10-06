from django import forms
from .models import Product
from django.core.exceptions import ValidationError

FORBIDDEN_WORDS = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "image", "category"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        if any(word in name.lower() for word in FORBIDDEN_WORDS):
            raise ValidationError("Название продукта содержит запрещенные слова.")
        return name

    def clean_description(self):
        description = self.cleaned_data["description"]
        if any(word in description.lower() for word in FORBIDDEN_WORDS):
            raise ValidationError("Описание продукта содержит запрещенные слова.")
        return description

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 0:
            raise ValidationError("Цена продукта не может быть отрицательной.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            if not image.name.endswith((".png", ".jpg", ".jpeg")):
                raise ValidationError("Формат изображения должен быть PNG или JPEG.")

            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Размер изображения не должен превышать 5 МБ.")
        return image

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
