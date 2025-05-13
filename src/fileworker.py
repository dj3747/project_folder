import json
import os
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
    def delete_vacancy(self, vacancy_id):
        """Удаляет вакансию из файла"""
        pass


class JsonVacancyStorage(FileWorker):
    """Класс для работы с JSON-файлом"""

    def __init__(self, filename="vacancies.json"):
        self.__filename = os.path.join(os.getcwd(), filename)  # Приватный атрибут имени файла

    def _read_file(self):
        """Читает данные из JSON-файла"""
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []  # Если файл не найден, возвращаем пустой список

    def _write_file(self, data):
        """Записываем данные в JSON-файл"""
        try:
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"Данные успешно записаны в файл {self.__filename}.")
        except Exception as e:
            print(f"Ошибка записи в файл: {e}")

    def add_vacancy(self, vacancy):
        vacancies = self._read_file()

        if not any(existing_vacancy.get("Вакансия") == vacancy.get("title") for existing_vacancy in vacancies):
            formatted_vacancy = {
                "Вакансия": vacancy.get("title"),
                "Ссылка": vacancy.get("link"),
                "Зарплата": vacancy.get("salary"),
                "Описание": vacancy.get("description"),
            }
            vacancies.append(formatted_vacancy)
            print(f"Данные для записи в файл: {vacancies}")  # Отладка
            self._write_file(vacancies)  # Запись данных
            print(f"\nВакансия добавлена в файл:\n{formatted_vacancy}")
        else:
            print(f"Вакансия '{vacancy.get('title')}' уже существует в файле.")

    def get_vacancies(self, **filters):
        """
        Возвращает список вакансий из файла по указанным критериям.
        Например, filter может быть: {"salary_from": 100000, "keywords": "Python"}.
        """
        vacancies = self._read_file()
        for key, value in filters.items():
            vacancies = [vacancy for vacancy in vacancies if vacancy.get(key) == value]
        return vacancies

    def delete_vacancy(self, vacancy_id):
        """Удаляет вакансию по указанному ID"""
        vacancies = self._read_file()
        updated_vacancies = [vacancy for vacancy in vacancies if vacancy.get("id") != vacancy_id]

        if len(vacancies) != len(updated_vacancies):
            self._write_file(updated_vacancies)
            print(f"Вакансия с ID {vacancy_id} удалена.")
        else:
            print(f"Вакансия с ID {vacancy_id} не найдена.")
