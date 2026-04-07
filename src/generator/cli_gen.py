import csv
import os
import argparse
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

def generate_coursera_data(output_path, num_rows):
    fieldnames = [
        'spec_title', 'spec_rating',
        'instructor_name', 'instructor_expertise',
        'course_name', 'course_final_deadline',
        'week_number', 'week_soft_deadline', 'week_hard_deadline',
        'review_author', 'review_rating', 'review_text'
    ]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    num_specs = 15
    courses_per_spec = 5
    weeks_per_course = 4
    
    # 1. Генеруємо спеціалізації
    specializations = [
        (f"Specialization: {fake.job()}", round(random.uniform(4.0, 5.0), 1)) 
        for _ in range(num_specs)
    ]
    
    # 2. Генеруємо загальний пул інструкторів для кожної спеціалізації (від 6 до 8)
    instructors_per_spec = {}
    for spec_id in range(num_specs):
        num_instructors = random.randint(6, 8)
        instructors_per_spec[spec_id] = [
            {'name': fake.name(), 'expertise': fake.bs().capitalize()}
            for _ in range(num_instructors)
        ]
    
    # 3. Генеруємо курси і призначаємо їм команду з 2-3 інструкторів (з пулу спеціалізації)
    courses = []
    for spec_id in range(num_specs):
        for _ in range(courses_per_spec):
            base_date = fake.date_time_between(start_date='now', end_date='+1y')
            # Вибираємо 2 або 3 унікальних інструкторів для цього курсу
            course_instructors = random.sample(instructors_per_spec[spec_id], random.randint(2, 3))
            
            courses.append({
                'spec_idx': spec_id,
                'name': f"Course: {fake.catch_phrase()}",
                'deadline': (base_date + timedelta(days=60)).isoformat(),
                'base_date': base_date,
                'instructors': course_instructors
            })

    try:
        with open(output_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for _ in range(num_rows):
                # Вибираємо випадковий курс
                course = random.choice(courses)
                spec_idx = course['spec_idx']
                spec_title, spec_rating = specializations[spec_idx]
                
                # Вибираємо випадкового інструктора З КОМАНДИ ЦЬОГО КУРСУ
                instructor = random.choice(course['instructors'])
                
                # Вибираємо випадковий тиждень
                week_num = random.randint(1, weeks_per_course)
                week_soft = course['base_date'] + timedelta(days=7 * week_num)
                week_hard = week_soft + timedelta(days=2)
                
                rating_weights = [5, 4, 3, 2, 1]
                rating_probabilities = [60, 25, 10, 3, 2]
                
                writer.writerow({
                    'spec_title': spec_title,
                    'spec_rating': spec_rating,
                    'instructor_name': instructor['name'],
                    'instructor_expertise': instructor['expertise'],
                    'course_name': course['name'],
                    'course_final_deadline': course['deadline'],
                    'week_number': week_num,
                    'week_soft_deadline': week_soft.isoformat(),
                    'week_hard_deadline': week_hard.isoformat(),
                    'review_author': fake.user_name(),
                    'review_rating': random.choices(rating_weights, weights=rating_probabilities)[0],
                    'review_text': fake.sentence(nb_words=8)
                })

        print(f"✅ Успішно згенеровано {num_rows} рядків у: {output_path}")
    except Exception as e:
        print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=1050)
    parser.add_argument('--output', type=str, default='data/coursera_data.csv')
    args = parser.parse_args()
    generate_coursera_data(args.output, args.count)