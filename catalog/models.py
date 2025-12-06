from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import uuid  # Добавляем импорт для генерации уникальных идентификаторов

# Получаем модель пользователя
User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Наименование',
        unique=True,  # Добавляем уникальность названия
        help_text='Уникальное название категории'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name='URL-идентификатор',
        help_text='Автоматически генерируется из названия'
    )
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):  # ✅ Исправлено: должно быть два подчеркивания __str__
        return self.name

    def save(self, *args, **kwargs):
        """Автоматически генерируем уникальный slug из названия"""
        # Если slug не задан или название изменилось
        if not self.slug or self._name_changed():
            # Генерируем базовый slug
            base_slug = slugify(self.name, allow_unicode=False)

            # Если slugify вернул пустую строку (например, для кириллицы без транслита)
            if not base_slug:
                base_slug = f"category-{uuid.uuid4().hex[:8]}"  # Уникальный идентификатор

            # Делаем slug уникальным
            self.slug = self._make_unique_slug(base_slug)

        super().save(*args, **kwargs)

    def _make_unique_slug(self, base_slug):
        """Создает уникальный slug"""
        slug = base_slug[:255]  # Ограничиваем длину
        counter = 1

        while True:
            # Проверяем, существует ли уже такой slug
            exists_query = Category.objects.filter(slug=slug)

            # Если это обновление существующей записи, исключаем ее из проверки
            if self.pk:
                exists_query = exists_query.exclude(pk=self.pk)

            # Если slug уникален - возвращаем
            if not exists_query.exists():
                return slug

            # Если не уникален - добавляем номер
            slug = f"{base_slug[:240]}-{counter}"  # Оставляем место для номера
            counter += 1

    def _name_changed(self):
        """Проверяет, изменилось ли имя у существующей записи"""
        if not self.pk:  # Новая запись
            return False

        try:
            # Получаем оригинальную запись из БД
            original = Category.objects.get(pk=self.pk)
            return original.name != self.name
        except Category.DoesNotExist:
            return False

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']  # Сортировка по умолчанию


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Наименование',
        help_text='Название продукта'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Подробное описание продукта'
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Изображение',
        help_text='Рекомендуемый размер: 800x600px'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='products',  # category.products - все продукты категории
        help_text='Выберите категорию'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена за покупку',
        help_text='Цена в рублях'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего изменения'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Отображается ли продукт на сайте'
    )

    # Поле владельца продукта
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Владелец',
        related_name='products',
        help_text='Пользователь, создавший продукт'
    )

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"

    def get_absolute_url(self):
        """Получение абсолютного URL продукта"""
        from django.urls import reverse
        return reverse('catalog:product_detail', kwargs={'pk': self.pk})

    def is_owner(self, user):
        """Проверяет, является ли пользователь владельцем продукта"""
        return self.owner == user

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at', 'name']  # сначала новые
        indexes = [
            models.Index(fields=['name']),  # Индекс для поиска по имени
            models.Index(fields=['category', 'is_published']),  # Индекс для фильтрации
            models.Index(fields=['price']),  # Индекс для сортировки по цене
        ]
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
            ("can_change_publish_status", "Может изменять статус публикации"),
            ("can_view_statistics", "Может просматривать статистику"),
        ]
