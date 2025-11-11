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
- 🆕 Детальные страницы товаров
- 🆕 Динамическое отображение каталога
- 🆕 Блог с CRUD операциями - полное управление записями
- 🆕 Счетчик просмотров - автоматический учет просмотров статей
- 🆕 Фильтрация записей - показ только опубликованных статей
- 🆕 Умные перенаправления - после редактирования на просмотр статьи

## 🛠 Технологии

- Backend: Django 5.2+
- Frontend: Bootstrap 5.3
- Язык: Python 3.11+
- 🆕 База данных: PostgreSQL
- 🆕 Pillow - обработка изображений
- 🆕 psycopg2 - драйвер PostgreSQL
- 🆕 python-dotenv - управление переменными окружения
- 🆕 Class-Based Views (CBV) - для блога и каталога

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
│   │   ├── base.html       # 🆕 Базовый шаблон
│   │   ├── includes/
│   │   │   └── header.html # 🆕 Подшаблон меню
│   │   ├── home.html
│   │   ├── contacts.html
│   │   └── product_detail.html # 🆕 Страница товара
│   ├── admin.py           # 🆕 Настройки админки
│   ├── models.py          # 🆕 Модели данных
│   ├── views.py           # 🆕 CBV контроллеры
│   └── urls.py
├── blog/                   # 🆕 Приложение блога
│   ├── migrations/
│   ├── templates/blog/
│   │   ├── blogpost_list.html
│   │   ├── blogpost_detail.html
│   │   ├── blogpost_form.html
│   │   └── blogpost_confirm_delete.html
│   ├── admin.py
│   ├── models.py          # 🆕 Модель BlogPost
│   ├── views.py           # 🆕 CBV с кастомной логикой
│   └── urls.py
├── config/                 # Настройки проекта
│   ├── settings.py        # 🆕 Настройки PostgreSQL
│   ├── urls.py            # 🆕 Маршруты для медиафайлов и блога
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

### 🆕 BlogPost
- `title` - заголовок статьи
- `content` - содержимое статьи
- `preview` - превью изображение
- `created_at` - дата создания
- `is_published` - признак публикации
- `views_count` - количество просмотров

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
· 🆕 http://127.0.0.1:8000/product/1/ - Страница товара
· 🆕 http://127.0.0.1:8000/blog/ - Блог

🆕 Команды управления
# Заполнение тестовыми данными
python manage.py fill_products

# Создание фикстур
python manage.py dumpdata catalog.

Александр antik, [12.11.2025 0:44]
Category --indent 2

# Загрузка фикстур
python manage.py loaddata category.json product.json

# Работа с shell
python manage.py shell

# 🆕 Создание приложения блога
python manage.py startapp blog

🎯 Маршруты

URL Описание
/ Главная страница
/contacts/ Страница контактов
🆕 /admin/ Админ-панель
🆕 /media/ Медиафайлы
🆕 /product/<int:pk>/ Страница товара
🆕 /blog/ Список записей блога
🆕 /blog/post/<int:pk>/ Детальная страница записи
🆕 /blog/post/create/ Создание записи
🆕 /blog/post/<int:pk>/update/ Редактирование записи
🆕 /blog/post/<int:pk>/delete/ Удаление записи

🆕 Особенности блога

· Полный CRUD - создание, чтение, обновление, удаление
· Счетчик просмотров - автоматически увеличивается при каждом просмотре
· Фильтрация - показываются только опубликованные записи
· Умные перенаправления - после редактирования переход на просмотр статьи
· Class-Based Views - чистая архитектура на CBV

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
