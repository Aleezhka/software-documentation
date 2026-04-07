import os
from src.core.config import Config
from src.dal.repository import SqlAlchemyRepository
from src.bll.services import CourseraService

def main():
    print("🚀 Ініціалізація додатку Coursera (Варіант 23)...\n")

    # Перевірка наявності файлу
    if not os.path.exists(Config.CSV_DATA_PATH):
        print(f"⚠️ Файл {Config.CSV_DATA_PATH} не знайдено.")
        print("💡 Спочатку запустіть: python src/generator/cli_gen.py --count 1050")
        return

    # Inversion of Control / Dependency Injection
    repository = SqlAlchemyRepository(Config.DATABASE_URL)
    
    # Очищуємо базу перед імпортом для чистоти експерименту
    repository.clear_database()

    # Інжектимо DAL у BLL
    service = CourseraService(repository)

    # Виконання бізнес-логіки
    service.import_data_from_csv(Config.CSV_DATA_PATH)
    
    print("\n✅ Система готова. Можна запускати verify_db.py для перевірки.")

if __name__ == "__main__":
    main()