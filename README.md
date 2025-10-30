# Skystore - Интернет-магазин на Django

Веб-приложение интернет-магазина, построенное на Django с Bootstrap.

## 🚀 Функциональность

- Главная страница - информационный лендинг
- Страница контактов - контактная информация
- Адаптивный дизайн - работа на всех устройствах
- Навигация - меню между страницами
- 🆕 Каталог товаров - модели Product и Category
- 🆕 Админ-панель - управление товарами и категориями
- 🆕 PostgreSQL - профессиональная база данных
- 🆕 Загрузка изображений - для товаров через Pillow
- 🆕 Миграции БД - система управления схемой базы данных

## 🛠 Технологии

- Backend: Django 5.2+
- Frontend: Bootstrap 5.3
- Язык: Python 3.11+
- 🆕 База данных: PostgreSQL (ранее SQLite)
- 🆕 Pillow** - обработка изображений
- 🆕 psycopg2** - драйвер PostgreSQL
- 🆕 python-dotenv - управление переменными окружения

## 📁 Структура проекта


Django/
├── catalog/                 # Основное приложение
│   ├── management/commands/
│   │   └── fill_products.py # 🆕 Кастомная команда
│   ├── fixtures/           # 🆕 Фикстуры данных
│   │   ├── category.json
│   │   └── product.json
│   ├── migrations/         # 🆕 Файлы миграций
│   ├── templates/catalog/
│   │   ├── home.html
│   │   └── contacts.html
│   ├── admin.py           # 🆕 Настройки админки
│   ├── models.py          # 🆕 Модели данных
│   ├── views.py
│   └── urls.py
├── config/                 # Настройки проекта
│   ├── settings.py        # 🆕 Настройки PostgreSQL
│   ├── urls.py            # 🆕 Маршруты для медиафайлов
│   └── ...
├── media/                 # 🆕 Папка для загружаемых файлов
├── .env                   # 🆕 Переменные окружения
├── requirements.txt       # 🆕 Зависимости проекта
└── manage.py

## 🆕 Модели данных

### Category
- `name` - название категории
- `description` - описание категории

### Product  
- `name` - название товара
- `description` - описание товара
- `image` - изображение товара
- `category` - связь с категорией (ForeignKey)
- `price` - цена товара
- `created_at` - дата создания
- `updated_at` - дата обновления

## ⚡️ Быстрый старт

```bash
# Установка
git clone <repository-url>
cd Django
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 🆕 Установка зависимостей
pip install -r requirements.txt

# 🆕 Настройка базы данных PostgreSQL
# Создайте БД и настройте .env файл

# Миграции и запуск
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Откройте в браузере:

· http://127.0.0.1:8000/ - Главная страница
· http://127.0.0.1:8000/contacts/ - Контакты
· 🆕 http://127.0.0.1:8000/admin/ - Админ-панель

🆕 Команды управления
# Заполнение тестовыми данными
python manage.py fill_products

# Создание фикстур
python manage.py dumpdata catalog.Category --indent 2

# Загрузка фикстур
python manage.py loaddata category.json product.json

# Работа с shell
python manage.py shell

🎯 Маршруты

URL Описание
/ Главная страница
/contacts/ Страница контактов
🆕 /admin/ Админ-панель
🆕 /media/ Медиафайлы

🛡 Безопасность

· 🆕 Чувствительные данные в .env файле
· 🆕 PostgreSQL вместо SQLite для продакшена
· 🆕 Переменные окружения для настроек БД

👨‍💻 Разработка

Абрамов Александр

· GitHub: @1Abramov1

🙏 Благодарности

· Команда Bootstrap за отличный фреймворк
· Сообщество Python за документацию и примеры
· 🆕 Команда PostgreSQL за надежную СУБД
· Все контрибьюторы проекта

---

⭐️ Не забудьте поставить звезду, если проект был полезен!