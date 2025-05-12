from abc import ABC, abstractmethod

import requests


class JobAPI(ABC):
    """Абстрактный метод для взаимодействия с API сервисом вакансий"""

    def __init__(self, base_url):
        self._base_url = base_url  # Приватный атрибут для хранения базового URL

    @abstractmethod
    def _connect(self):
        """Абстрактный метод подключения к API"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword, page=0, per_page=100):
        """Абстрактный метод для получения списка вакансий"""
        pass


class HhRuAPI(JobAPI):
    """Класс для работы с API платформы hh.ru"""

    def __init__(self):
        super().__init__("https://api.hh.ru/vacancies")  # Установка базового URL
        self._headers = {"User-Agent": "HH-User-Agent"}  # Заголовки для запросов

    def _connect(self):
        """Метод подключения к API hh.ru"""
        try:
            response = requests.get(self._base_url, headers=self._headers)
            response.raise_for_status()  # Проверка успешности запроса
            print("Подключение к API hh.ru успешно!")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка подключения к API hh.ru: {e}")

    def get_vacancies(self, keyword, page=0, per_page=100):
        """Метод для получения списка вакансий
        :param keyword: Ключевое слово для поиска вакансий
        :param page: Номер страницы для получения данных
        :param per_page: Количество вакансий на странице
        :return: Список вакансий (словарей)
        """
        self._connect()  # Проверка подключения перед запросом данных
        params = {
            "text": keyword,  # Поисковый запрос
            "page": page,  # Номер страницы
            "per_page": per_page,  # Количество вакансий на странице
            "area": 113,  # ограничение по России
        }
        try:
            response = requests.get(self._base_url, headers=self._headers, params=params)
            response.raise_for_status()  # Проверка успешности запроса
            data = response.json()
            print(f"Получено {len(data.get('items', []))} вакансий на странице {page}.")
            return data.get("items", [])
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Ошибка при получении данных: {e}")
