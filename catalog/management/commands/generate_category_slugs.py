from django.core.management.base import BaseCommand
from django.utils.text import slugify
from catalog.models import Category


class Command(BaseCommand):
    help = 'Генерирует slug для существующих категорий'

    def handle(self, *args, **options):
        categories = Category.objects.all()
        count = 0

        for category in categories:
            if not category.slug:
                original_name = category.name
                # Генерируем slug
                category.slug = slugify(category.name)

                # Проверяем уникальность
                base_slug = category.slug
                counter = 1
                while Category.objects.filter(slug=category.slug).exclude(id=category.id).exists():
                    category.slug = f"{base_slug}-{counter}"
                    counter += 1

                category.save()
                count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Сгенерирован slug для: {original_name} -> {category.slug}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'✅ Всего обработано категорий: {count}')
        )