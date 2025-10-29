from django.core.management.base import BaseCommand
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми продуктами (очищает существующие данные)'

    def handle(self, *args, **options):

        # Удаляем все существующие продукты и категории
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('Все существующие данные удалены')

        # Создаем категории
        categories = [
            {'name': 'Электроника', 'description': 'Смартфоны, ноутбуки, планшеты'},
            {'name': 'Одежда', 'description': 'Мужская и женская одежда'},
            {'name': 'Книги', 'description': 'Художественная и учебная литература'},
            {'name': 'Спорт', 'description': 'Спортивный инвентарь и одежда'},
            {'name': 'Дом и сад', 'description': 'Товары для дома и садоводства'},
        ]

        created_categories = {}
        for cat_data in categories:
            category = Category.objects.create(
                name=cat_data['name'],
                description=cat_data['description']
            )
            created_categories[cat_data['name']] = category
            self.stdout.write(f'Создана категория: {category.name}')

        # Создаем продукты
        products = [
            {
                'name': 'iPhone 15 Pro',
                'description': 'Флагманский смартфон Apple с процессором A17 Pro',
                'category': 'Электроника',
                'price': 1299.99
            },
            {
                'name': 'Samsung Galaxy S24',
                'description': 'Смартфон Samsung с искусственным интеллектом',
                'category': 'Электроника',
                'price': 899.99
            },
            {
                'name': 'Футболка хлопковая',
                'description': 'Удобная хлопковая футболка унисекс',
                'category': 'Одежда',
                'price': 24.99
            },
            {
                'name': 'Джинсы классические',
                'description': 'Синие джинсы прямого кроя',
                'category': 'Одежда',
                'price': 79.99
            },
            {
                'name': 'Python для начинающих',
                'description': 'Подробный учебник по программированию на Python',
                'category': 'Книги',
                'price': 49.99
            },
            {
                'name': 'Игра престолов',
                'description': 'Фэнтези роман Джорджа Мартина',
                'category': 'Книги',
                'price': 34.99
            },
            {
                'name': 'Футбольный мяч',
                'description': 'Профессиональный футбольный мяч',
                'category': 'Спорт',
                'price': 45.99
            },
            {
                'name': 'Гантели 5кг',
                'description': 'Резиновые гантели для домашних тренировок',
                'category': 'Спорт',
                'price': 29.99
            },
            {
                'name': 'Горшок для цветов',
                'description': 'Керамический горшок с дренажом',
                'category': 'Дом и сад',
                'price': 19.99
            },
            {
                'name': 'Набор садовых инструментов',
                'description': 'Лопата, грабли и перчатки в наборе',
                'category': 'Дом и сад',
                'price': 59.99
            },
        ]

        for product_data in products:
            product = Product.objects.create(
                name=product_data['name'],
                description=product_data['description'],
                category=created_categories[product_data['category']],
                price=product_data['price']
            )
            self.stdout.write(
                self.style.SUCCESS(f'Создан продукт: {product.name} - {product.price} руб.')
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно создано {len(created_categories)} категорий и {len(products)} продуктов!'
            )
        )