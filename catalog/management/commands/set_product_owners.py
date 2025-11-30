from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from catalog.models import Product

User = get_user_model()


class Command(BaseCommand):
    help = 'Устанавливает владельца для существующих продуктов'

    def handle(self, *args, **options):
        """ Находим первого суперпользователя как владельца по умолчанию"""

        admin_user = User.objects.filter(is_superuser=True).first()

        if not admin_user:
            self.stdout.write(
                self.style.ERROR('❌ Не найден суперпользователь!')
            )
            return

        # Устанавливаем владельца для продуктов без владельца
        products_without_owner = Product.objects.filter(owner__isnull=True)
        count = products_without_owner.count()

        for product in products_without_owner:
            product.owner = admin_user
            product.save()

        self.stdout.write(
            self.style.SUCCESS(f'✅ Установлен владелец для {count} продуктов')
        )