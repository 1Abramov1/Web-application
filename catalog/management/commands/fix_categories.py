from django.core.management.base import BaseCommand
from catalog.models import Category


class Command(BaseCommand):
    help = 'Исправляет slug для всех категорий'

    def handle(self, *args, **kwargs):
        self.stdout.write("Исправление категорий...")

        for category in Category.objects.all():
            old_slug = category.slug

            if not category.slug or category.slug.strip() == '':
                category.save()
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Добавлен slug для '{category.name}': {category.slug}")
                )
            else:
                self.stdout.write(f"✓ '{category.name}': {category.slug}")

        self.stdout.write(self.style.SUCCESS(f"\nГотово! Всего категорий: {Category.objects.count()}"))