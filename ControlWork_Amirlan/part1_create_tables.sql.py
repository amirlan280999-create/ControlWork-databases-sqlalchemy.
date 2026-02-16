# -- ЧАСТЬ 1: Создание таблиц и функции
# -- Автор: [Amirlan]
# -- Дата: 16.02.2026

 Создание таблицы platforms
CREATE TABLE IF NOT EXISTS platforms (
    id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL UNIQUE
);

 Создание таблицы games
CREATE TABLE IF NOT EXISTS games (
    id SERIAL PRIMARY KEY,
title VARCHAR(200) NOT NULL,
price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
platform_id INTEGER REFERENCES platforms(id) ON DELETE CASCADE
);

 Очистка таблиц от возможных дубликатов
TRUNCATE TABLE games RESTART IDENTITY CASCADE;
TRUNCATE TABLE platforms RESTART IDENTITY CASCADE;

 Добавление платформ
INSERT INTO platforms (name) VALUES
('Sega'),
('Dendy');

 Добавление игр
INSERT INTO games (title, price, stock, platform_id)
SELECT title, price, stock, p.id
FROM (VALUES
      -- Игры для Sega
('Golden Axe', 24.99, 10, 'Sega'),
('Sonic the Hedgehog', 29.99, 15, 'Sega'),

 Игры для Dendy
('Super Mario Bros', 34.99, 20, 'Dendy'),
('Contra', 19.99, 25, 'Dendy')
) AS g(title, price, stock, platform_name)
JOIN platforms p ON p.name = g.platform_name;

 Хранимая процедура для скидок
CREATE OR REPLACE FUNCTION apply_discount(p_platform_id INT, p_discount_percent INT)
RETURNS VOID AS $$
BEGIN
IF p_discount_percent < 0 OR p_discount_percent > 100 THEN
RAISE EXCEPTION 'Процент скидки должен быть от 0 до 100';
END IF;

UPDATE games
SET price = price * (1 - p_discount_percent::DECIMAL / 100)
WHERE platform_id = p_platform_id;

RAISE NOTICE 'Скидка % применена к платформе с ID %', p_discount_percent, p_platform_id;
END;
$$ LANGUAGE plpgsql;

 Проверка данных
SELECT
p.name as "Платформа",
g.title as "Игра",
g.price as "Цена",
g.stock as "Остаток"
FROM games g
JOIN platforms p ON g.platform_id = p.id
ORDER BY p.name, g.title;