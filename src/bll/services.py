from typing import List, Optional
from datetime import datetime
from src.dal.interfaces import IDataRepository
from src.dal.models import Specialization, Course, Week, Instructor, Review

class CourseraService:
    def __init__(self, repository: IDataRepository):
        self._repository = repository

    def get_all_specializations(self) -> List[Specialization]:
        return self._repository.get_all_specializations()

    def import_data_from_csv(self, file_path: str):
        raw_rows = self._repository.read_raw_data_from_csv(file_path)
        if not raw_rows:
            return

        # Кеш для всіх сутностей, щоб уникати дублікатів
        specs_cache = {}
        courses_cache = {}
        instructors_cache = {}
        weeks_cache = {}
        entities_to_save = []

        print(f"🔄 Початок обробки {len(raw_rows)} рядків...")

        for row in raw_rows:
            # 1. Specialization
            spec_title = row['spec_title']
            if spec_title not in specs_cache:
                spec = Specialization(title=spec_title, rating=float(row['spec_rating']))
                specs_cache[spec_title] = spec
                entities_to_save.append(spec)
            current_spec = specs_cache[spec_title]

            # 2. Instructor (кешуємо за іменем + спеціалізацією)
            instr_key = f"{spec_title}_{row['instructor_name']}"
            if instr_key not in instructors_cache:
                instructor = Instructor(
                    full_name=row['instructor_name'],
                    expertise=row['instructor_expertise'],
                    specialization=current_spec
                )
                instructors_cache[instr_key] = instructor
                entities_to_save.append(instructor)

            # 3. Course
            course_name = row['course_name']
            course_key = f"{spec_title}_{course_name}"
            if course_key not in courses_cache:
                course = Course(
                    name=course_name,
                    final_deadline=datetime.fromisoformat(row['course_final_deadline']),
                    specialization=current_spec
                )
                courses_cache[course_key] = course
                entities_to_save.append(course)
            current_course = courses_cache[course_key]

            # 4. Week (кешуємо за курсом + номером тижня)
            week_num = int(row['week_number'])
            week_key = f"{course_key}_week_{week_num}"
            if week_key not in weeks_cache:
                week = Week(
                    week_number=week_num,
                    soft_deadline=datetime.fromisoformat(row['week_soft_deadline']),
                    hard_deadline=datetime.fromisoformat(row['week_hard_deadline']),
                    course=current_course
                )
                weeks_cache[week_key] = week
                entities_to_save.append(week)

            # 5. Review (відгуки завжди унікальні, їх не кешуємо)
            review = Review(
                author=row['review_author'],
                rating=int(row['review_rating']),
                text=row['review_text'],
                specialization=current_spec
            )
            entities_to_save.append(review)

        self._repository.save_entities(entities_to_save)
        print("🚀 Бізнес-логіка: Обробка завершена.")