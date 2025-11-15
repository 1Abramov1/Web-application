from django import forms
from django.core.exceptions import ValidationError
from .models import Product


class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования продуктов с валидацией запрещенных слов и цены.
    """
    # Запрещенные слова
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def clean_name(self):
        """
        Валидация названия продукта на наличие запрещенных слов.
        """
        name = self.cleaned_data['name'].lower()

        for word in self.FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(
                    f'Название содержит запрещенное слово: "{word}"'
                )

        return self.cleaned_data['name']

    def clean_description(self):
        """
        Валидация описания продукта на наличие запрещенных слов.
        """
        description = self.cleaned_data['description'].lower()

        for word in self.FORBIDDEN_WORDS:
            if word in description:
                raise ValidationError(
                    f'Описание содержит запрещенное слово: "{word}"'
                )

        return self.cleaned_data['description']

    def clean_price(self):
        """
        Валидация цены продукта - проверка, что цена не отрицательная.
        """
        price = self.cleaned_data['price']

        if price < 0:
            raise ValidationError(
                'Цена не может быть отрицательной. Введите положительное значение.'
            )

        if price == 0:
            raise ValidationError(
                'Цена не может быть нулевой. Введите положительное значение.'
            )

        return price