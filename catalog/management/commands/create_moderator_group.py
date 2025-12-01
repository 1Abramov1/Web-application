from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу модераторов продуктов с необходимыми правами'

    def handle(self, *args, **options):
        # Получаем ContentType для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Получаем необходимые разрешения
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=[
                'can_unpublish_product',
                'can_change_publish_status',
                'delete_product'
            ]
        )

        # Создаем или получаем группу
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Добавляем разрешения в группу
        group.permissions.set(permissions)

        if created:
            self.stdout.write(
                self.style.SUCCESS('✅ Группа "Модератор продуктов" создана успешно!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('ℹ️ Группа "Модератор продуктов" уже существует, обновлены разрешения')
            )

        self.stdout.write(
            self.style.SUCCESS(f'✅ Добавлено {permissions.count()} разрешений в группу:')
        )
        for perm in permissions:
            self.stdout.write(f'   - {perm.name}')