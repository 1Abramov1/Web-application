from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category


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
        fields = ['name', 'description', 'image', 'category', 'price', 'is_published']
        # 🆕 Поле owner НЕ включаем - оно устанавливается автоматически
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название товара'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опишите товар подробно'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Название товара',
            'description': 'Описание товара',
            'image': 'Изображение товара',
            'category': 'Категория',
            'price': 'Цена (руб.)',
            'is_published': 'Опубликовать товар',
        }
        help_texts = {
            'name': 'Не используйте запрещенные слова в названии',
            'description': 'Подробно опишите характеристики товара',
            'price': 'Введите цену в рублях',
            'is_published': 'Товар будет виден в каталоге только после публикации',
        }

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы с дополнительной стилизацией.
        """
        super().__init__(*args, **kwargs)

        # Стилизация всех полей
        for field_name, field in self.fields.items():
            # Для чекбокса добавляем особый класс
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            # Для остальных полей добавляем стандартные классы
            elif field_name != 'is_published':
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'

                # Добавляем дополнительные атрибуты в зависимости от типа поля
                if field_name == 'name':
                    field.widget.attrs['placeholder'] = 'Введите название товара'
                elif field_name == 'description':
                    field.widget.attrs['placeholder'] = 'Опишите товар подробно'
                    field.widget.attrs['rows'] = 4
                elif field_name == 'price':
                    field.widget.attrs['placeholder'] = '0.00'
                    field.widget.attrs['step'] = '0.01'
                elif field_name == 'category':
                    # Оптимизируем запрос для категорий
                    field.queryset = Category.objects.all()

            # Добавляем обязательную маркировку
            if field.required:
                field.widget.attrs['required'] = 'required'

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

        return self.cleaned_data['description']  # 🆕 Исправлено - добавлен return

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
