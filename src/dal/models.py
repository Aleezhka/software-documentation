from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class Specialization(Base):
    __tablename__ = 'specializations'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    rating = Column(Float, default=0.0)

    # Зв'язки (згідно UML)
    courses = relationship("Course", back_populates="specialization", cascade="all, delete-orphan")
    instructors = relationship("Instructor", back_populates="specialization")
    reviews = relationship("Review", back_populates="specialization", cascade="all, delete-orphan")

    def enroll(self, student_id: str):
        print(f"✅ Студент {student_id} записався на спеціалізацію '{self.title}'")

    def get_average_rating(self) -> float:
        return self.rating

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    specialization_id = Column(Integer, ForeignKey('specializations.id'))
    name = Column(String, nullable=False)
    final_deadline = Column(DateTime)

    specialization = relationship("Specialization", back_populates="courses")
    weeks = relationship("Week", back_populates="course", cascade="all, delete-orphan")

    def check_completion(self) -> bool:
        print(f"Перевірка завершеності курсу {self.name}...")
        return True

class Week(Base):
    __tablename__ = 'weeks'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    week_number = Column(Integer)
    soft_deadline = Column(DateTime)
    hard_deadline = Column(DateTime)

    course = relationship("Course", back_populates="weeks")

    def is_overdue(self) -> bool:
        return False

class Instructor(Base):
    __tablename__ = 'instructors'

    id = Column(Integer, primary_key=True)
    specialization_id = Column(Integer, ForeignKey('specializations.id'))
    full_name = Column(String, nullable=False)
    expertise = Column(String)

    specialization = relationship("Specialization", back_populates="instructors")

    def grade_assignment(self, score: int):
        print(f"Інструктор {self.full_name} оцінив роботу на {score} балів.")

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    specialization_id = Column(Integer, ForeignKey('specializations.id'))
    author = Column(String)
    rating = Column(Integer)
    text = Column(String)

    specialization = relationship("Specialization", back_populates="reviews")