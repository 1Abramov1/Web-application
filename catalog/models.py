from django.db import models
from django.contrib.auth import get_user_model

# 🆕 Получаем модель пользователя
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    # 🆕 Поле владельца продукта
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Если пользователь удален, продукт остается
        null=True,
        blank=True,
        verbose_name='Владелец',
        related_name='products'  # user.products - все продукты пользователя
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name', 'category']
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
            ("can_change_publish_status", "Может изменять статус публикации"),
        ]