from abc import ABC, abstractmethod

from src.vac_handler import VacHandler


class Parser(ABC):
    """
    Абстрактный класс для работы с api
    """

    @abstractmethod
    def get_vacancies(self, keyword: str):
        pass


class BaseFileHandler(ABC):
    """
    Абстрактный класс для работы с файлами
    """

    @abstractmethod
    def add_vacancies(self, vacancy: VacHandler):
        pass

    @abstractmethod
    def get_filtered_from_file(self, keyword: int, criteria: str):
        pass

    @abstractmethod
    def delete_vacancies(self, vacancy: VacHandler):
        pass
