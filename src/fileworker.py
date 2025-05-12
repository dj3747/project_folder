import json
from abc import ABC, abstractmethod

class FileWorker(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def add_vacancy(self, vacancy):
        """Добавляет вакансию в файл"""
        pass

    @abstractmethod
    def get_vacancies(self, **filters):
        """Получает вакансии из файла по указанным критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        """Удаляет вакансию из файла"""
        pass

class JsonVacancyStorage(FileWorker):
    """Класс для работы с JSON-файлом"""