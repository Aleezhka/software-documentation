from abc import ABC, abstractmethod
from typing import List, Any

class IView(ABC):
    """
    Інтерфейс презентаційного рівня (PL).
    Визначає методи взаємодії з користувачем без реалізації бізнес-логіки.
    """

    @abstractmethod
    def display_message(self, message: str) -> None:
        """Показує текстове повідомлення (успіх/помилка)."""
        pass

    @abstractmethod
    def render_specialization_list(self, specializations: List[Any]) -> None:
        """Відображає список спеціалізацій, отриманих від BLL."""
        pass

    @abstractmethod
    def render_statistics(self, stats: str) -> None:
        """Відображає аналітичні дані."""
        pass

    @abstractmethod
    def show_import_progress(self, current: int, total: int) -> None:
        """Відображає прогрес обробки рядків CSV."""
        pass

    @abstractmethod
    def get_input(self, prompt: str) -> str:
        """Отримує ввід від користувача."""
        pass