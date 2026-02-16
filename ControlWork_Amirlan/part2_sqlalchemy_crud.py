
# ЧАСТЬ 2: SQLAlchemy + CRUD операции
# Автор: [Amirlan]
# Дата: 16.02.2026
# Игры: Golden Axe, Sonic, Super Mario Bros, Contra


import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, CheckConstraint, Text, DECIMAL, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

# НАСТРОЙКА ПОДКЛЮЧЕНИЯ

DB_HOST = 'localhost'
DB_PORT = '5433'
DB_NAME = 'game_shop'
DB_USER = 'postgres'
DB_PASSWORD = ''

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# МОДЕЛИ

class Platform(Base):
    __tablename__ = 'platforms'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    games = relationship("Game", back_populates="platform", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Platform(id={self.id}, name='{self.name}')"

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    platform_id = Column(Integer, ForeignKey('platforms.id', ondelete='CASCADE'))

    platform = relationship("Platform", back_populates="games")
    reviews = relationship("Review", back_populates="game", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Game(id={self.id}, title='{self.title}', price={self.price})"

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id', ondelete='CASCADE'), nullable=False)
    author_name = Column(String(100), nullable=False)
    rating = Column(Integer, nullable=False)
    text = Column(Text)

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
        UniqueConstraint('author_name', 'game_id', name='unique_author_game')
    )

    game = relationship("Game", back_populates="reviews")

    def __repr__(self):
        return f"Review(id={self.id}, author='{self.author_name}', rating={self.rating})"

# МИГРАЦИЯ

print("\n" + "="*50)
print("СОЗДАНИЕ ТАБЛИЦЫ reviews")
print("="*50)
Base.metadata.create_all(engine)
print("Таблица reviews создана или уже существует")

# CRUD ОПЕРАЦИИ

def create_review(session, game_id: int, author: str, rating: int, text: str) -> Optional[Review]:
    try:
        game = session.query(Game).filter(Game.id == game_id).first()
        if not game:
            print(f"Ошибка: Игра с ID {game_id} не найдена")
            return None

        if rating < 1 or rating > 5:
            print("Ошибка: Рейтинг должен быть от 1 до 5")
            return None

        review = Review(
            game_id=game_id,
            author_name=author,
            rating=rating,
            text=text
        )

        session.add(review)
        session.commit()
        print(f"Отзыв создан: {review}")
        return review

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Ошибка при создании отзыва: {e}")
        return None

def read_game_reviews(session, game_title: str) -> List[Review]:
    try:
        game = session.query(Game).filter(
            Game.title.ilike(f'%{game_title}%')
        ).first()

        if not game:
            print(f"Игра '{game_title}' не найдена")
            return []

        reviews = session.query(Review).filter(Review.game_id == game.id).all()

        print(f"\nОТЗЫВЫ ДЛЯ ИГРЫ: {game.title}")
        print("-" * 40)
        if not reviews:
            print("Отзывов пока нет")
        else:
            for i, review in enumerate(reviews, 1):
                print(f"\n{i}. Автор: {review.author_name}")
                print(f"   Оценка: {review.rating}/5")
                print(f"   Текст: {review.text}")
                print(f"   ID: {review.id}")

        return reviews

    except SQLAlchemyError as e:
        print(f"Ошибка при чтении отзывов: {e}")
        return []

def update_review(session, review_id: int, new_text: str) -> bool:
    try:
        review = session.query(Review).filter(Review.id == review_id).first()

        if not review:
            print(f"Отзыв с ID {review_id} не найден")
            return False

        old_text = review.text
        review.text = new_text
        session.commit()
        print(f"\nОтзыв {review_id} обновлен:")
        print(f"   Было: {old_text}")
        print(f"   Стало: {new_text}")
        return True

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Ошибка при обновлении отзыва: {e}")
        return False

def delete_review(session, review_id: int) -> bool:
    try:
        review = session.query(Review).filter(Review.id == review_id).first()

        if not review:
            print(f"Отзыв с ID {review_id} не найден")
            return False

        session.delete(review)
        session.commit()
        print(f"\nОтзыв {review_id} удален")
        return True

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Ошибка при удалении отзыва: {e}")
        return False

# ДЕМОНСТРАЦИЯ

def demonstrate_crud_operations():
    session = SessionLocal()

    try:
        print("\n" + "="*50)
        print("ДЕМОНСТРАЦИЯ CRUD ОПЕРАЦИЙ")
        print("="*50)

        game = session.query(Game).filter(Game.title == 'Super Mario Bros').first()
        if not game:
            print("Игра Super Mario Bros не найдена!")
            return

        game_id = game.id
        print(f"\nРаботаем с игрой: {game.title} (ID: {game_id})")

        # CREATE
        print("\n" + "-"*40)
        print("1. СОЗДАНИЕ ОТЗЫВОВ")
        print("-"*40)

        reviews_data = [
            (game_id, "Александр", 5, "Отличная игра! Детство вспомнил"),
            (game_id, "Мария", 4, "Хорошая игра, но сложновато"),
            (game_id, "Анна", 5, "Шедевр на все времена!"),
            (game_id, "Иван", 5, "Обязательно куплю!")
        ]

        created_reviews = []
        for data in reviews_data:
            review = create_review(session, *data)
            if review:
                created_reviews.append(review)

        # READ
        print("\n" + "-"*40)
        print("2. ЧТЕНИЕ ОТЗЫВОВ")
        print("-"*40)
        read_game_reviews(session, "Super Mario Bros")

        # UPDATE
        print("\n" + "-"*40)
        print("3. ОБНОВЛЕНИЕ ОТЗЫВА")
        print("-"*40)
        if len(created_reviews) >= 2:
            update_review(session, created_reviews[1].id,
                          "Исправляю оценку - все таки 5 звезд! Прошел уже 10 раз")

        # DELETE
        print("\n" + "-"*40)
        print("4. УДАЛЕНИЕ ОТЗЫВА")
        print("-"*40)
        if len(created_reviews) >= 3:
            delete_review(session, created_reviews[2].id)

        # READ AGAIN
        print("\n" + "-"*40)
        print("5. ПРОВЕРКА ПОСЛЕ ИЗМЕНЕНИЙ")
        print("-"*40)
        read_game_reviews(session, "Super Mario Bros")

        print("\n" + "="*50)
        print("ВСЕ ОПЕРАЦИИ ВЫПОЛНЕНЫ")
        print("="*50)

        # ИТОГОВЫЕ ДАННЫЕ
        print("\n" + "="*50)
        print("ИТОГОВЫЕ ДАННЫЕ В ТАБЛИЦЕ reviews")
        print("="*50)

        result = session.query(
            Review.id,
            Review.author_name,
            Review.rating,
            Review.text,
            Game.title.label('game_name')
        ).join(Game).order_by(Review.id).all()

        for row in result:
            print(f"\nID: {row.id}")
            print(f"Автор: {row.author_name}")
            print(f"Оценка: {row.rating}/5")
            print(f"Игра: {row.game_name}")
            print(f"Текст: {row.text}")
            print("-" * 30)

    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

# ЗАПУСК

if __name__ == "__main__":
    demonstrate_crud_operations()