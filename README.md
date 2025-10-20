# Skystore - Интернет-магазин на Django

Веб-приложение интернет-магазина, построенное на Django с Bootstrap.

## 🚀 Функциональность

- **Главная страница** - информационный лендинг
- **Страница контактов** - контактная информация
- **Адаптивный дизайн** - работа на всех устройствах
- **Навигация** - меню между страницами

## 🛠 Технологии

- **Backend**: Django 4.2+
- **Frontend**: Bootstrap 5.3
- **Язык**: Python 3.8+
- **База данных**: SQLite

## 📁 Структура проекта


Django/
├── catalog/                 # Основное приложение
│   ├── templates/catalog/
│   │   ├── home.html
│   │   └── contacts.html
│   ├── views.py
│   ├── urls.py
│   └── ...
├── config/                 # Настройки проекта
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── manage.py

## ⚡️ Быстрый старт

```bash
# Установка
git clone <repository-url>
cd Django
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Зависимости и запуск
pip install django
python manage.py migrate
python manage.py runserver

Откройте в браузере:

· http://127.0.0.1:8000/ - Главная страница
· http://127.0.0.1:8000/contacts/ - Контакты

🎯 Маршруты

URL Описание
/ Главная страница
/contacts/ Страница контактов

👨‍💻 Разработка

Абрамов Алекcандр

· GitHub: @1Abramov1

🙏 Благодарности

· Команда Bootstrap за отличный фреймворк
· Сообщество Python за документацию и примеры
· Все контрибьюторы проекта

---

⭐️ Не забудьте поставить звезду, если проект был полезен!