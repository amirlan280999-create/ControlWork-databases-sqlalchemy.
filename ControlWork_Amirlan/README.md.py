# Control work: Базы данных + Python SQLAlchemy
# [Amirlan]
# Дата: 16.02.2026

#Содержание работы

#Часть 1: SQL (pgAdmin/DBeaver)
- Созданы таблицы `platforms` и `games`
- Добавлены 2 платформы: Sega, Dendy
- Добавлены 4 игры:
  - Sega: Golden Axe, Sonic the Hedgehog
  - Dendy: Super Mario Bros, Contra
- Создана функция `apply_discount()` для применения скидок

#Часть 2: Python + SQLAlchemy
- Настроено подключение к БД через SQLAlchemy
- Созданы ORM модели Platform, Game, Review
- Проведена миграция: создана таблица `reviews`
- Реализованы CRUD операции:
  CREATE: создание отзывов
  READ: чтение отзывов по игре
  UPDATE: обновление текста отзыва
  DELETE: удаление отзыва
- Проведена очистка от дубликатов
- Добавлены уникальные ограничения

#Результаты
Все операции выполнены успешно. Данные в таблицах соответствуют требованиям.

#Используемые технологии
- PostgreSQL
- SQLAlchemy
- Python
- DBeaver/pgAdmin