from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IDataRepository(ABC):
    @abstractmethod
    def read_raw_data_from_csv(self, file_path: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def save_entities(self, entities: List[Any]) -> None:
        pass

    @abstractmethod
    def get_all_specializations(self) -> List[Any]:
        pass

    @abstractmethod
    def clear_database(self) -> None:
        pass