![Python](https://img.shields.io/badge/Python-3.14-blue)
![Django](https://img.shields.io/badge/Django-6.1-green)
[![Django Tests](https://github.com/Anyakin666/fitness_tracker/actions/workflows/test.yml/badge.svg)](https://github.com/Anyakin666/fitness_tracker/actions/workflows/test.yml)

# Fitness Tracker

Приложение, в котором я попыталась объединить самые нужные функции из нескольких разных приложений — записи тренировок, питания и замеров в одном месте. С расчётом КБЖУ по формуле Миффлина-Сан Жеора и проверкой, держитесь ли вы плана.

## Стек

- Python 3.14
- Django 6.1
- Tailwind CSS (через CDN)
- SQLite

## Возможности

- 🔐 Регистрация и вход — данные каждого пользователя видны только ему
- 🏋️ **Тренировки**: тип, длительность, заметки
- 🍎 **Питание**: калории и БЖУ по дням
- 📏 **Замеры тела**: вес и обхваты (талия, бёдра, грудь, бедро, бицепс, икра)
- 👤 **Профиль**: цель, пол, возраст, рост, вес, активность — с автоматическим расчётом цели по калориям
- 📊 **Главная**: последняя тренировка, последний замер, средние калории за 7 дней
- ✅ **Проверка плана**: сравнение средних калорий с целью, прогресс-бар, подбадривающие цитаты
- ✏️ Полный CRUD для всех разделов
- 📱 Адаптивная навигация (бургер-меню на мобильных)

## Запуск

1. Клонируйте репозиторий:
   git clone https://github.com/Anyakin666/fitness-tracker.git
   cd fitness-tracker

2. Создайте и активируйте виртуальное окружение:
   python -m venv venv
   venv\Scripts\activate    (Windows)
   source venv/bin/activate (macOS/Linux)

3. Установите зависимости:
   pip install -r requirements.txt

4. Примените миграции:
   python manage.py migrate

5. (Опционально) Создайте суперпользователя для доступа в админку:
   python manage.py createsuperuser

6. Запустите сервер:
   python manage.py runserver

7. Откройте в браузере: http://127.0.0.1:8000/

## Тесты

python manage.py test tracker

Покрыты: модели, вьюхи (логин, фильтрация), CRUD, безопасность (чужие записи → 404), главная (сводка, отклонение).

## Структура проекта

```
fitness-tracker/
├── fitness_tracker/      # настройки проекта
├── tracker/              # основное приложение
│   ├── models.py         # Workout, NutritionEntry, Measurement, UserProfile
│   ├── views.py          # списки, формы, главная, профиль
│   ├── forms.py          # ModelForm'ы
│   ├── utils.py          # расчёт КБЖУ, цитаты
│   ├── urls.py           # маршруты
│   ├── tests.py          # тесты
│   └── templates/
│       ├── base.html
│       └── tracker/      # шаблоны страниц
├── .github/workflows/    # CI (GitHub Actions)
├── requirements.txt
└── manage.py
```

## Скриншоты

_(добавлю позже)_