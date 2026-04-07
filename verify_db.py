from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.dal.models import Specialization, Course, Week, Instructor, Review
from src.core.config import Config

def verify_database():
    engine = create_engine(Config.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    print("🔍 --- ВЕРИФІКАЦІЯ БАЗИ ДАНИХ (Coursera) --- 🔍\n")

    try:
        stats = [
            ("Спеціалізації", session.query(Specialization).count()),
            ("Курси", session.query(Course).count()),
            ("Тижні (Weeks)", session.query(Week).count()),
            ("Інструктори", session.query(Instructor).count()),
            ("Відгуки", session.query(Review).count()),
        ]

        print(f"{'Сутність':<25} | {'Кількість':<10}")
        print("-" * 40)
        for name, count in stats:
            status = "✅ OK" if count > 0 else "❌ EMPTY"
            print(f"{name:<25} | {count:<10} {status}")

        print("\n📊 --- ПЕРЕВІРКА ЗВ'ЯЗКІВ (Relationships) ---")
        
        orphan_courses = session.query(Course).filter(Course.specialization_id == None).count()
        if orphan_courses == 0:
            print("✅ Всі курси коректно прив'язані до спеціалізацій.")
        else:
            print(f"⚠️ Знайдено {orphan_courses} курсів без спеціалізації!")
            
        orphan_weeks = session.query(Week).filter(Week.course_id == None).count()
        if orphan_weeks == 0:
            print("✅ Всі тижні коректно прив'язані до курсів.")
            
    except Exception as e:
        print(f"❌ Помилка під час верифікації: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    verify_database()