import json
from datetime import datetime

from requests import request

from helpers.utils import ApiCallException
from redsoft.settings import WEATHER_BASE_URL, WEATHER_API_KEY


class OpenWeatherApi:
    """
    Класс для работы с интеграционным сервисом, который предоставляет информацию о погоде
    """
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def get_full_weather_by_date(self, location: str, date_start: datetime, date_end: datetime) -> dict:
        """
        Получить информацию по погоде в локации за временной промежуток
        :param location: Локация "{Город},{Код страны}"
        :param date_start: Начало временного отрезка
        :param date_end: Конец временного отрезка
        :return: Экземпляр класса dict с информацией о погоде
        """
        path = self._generate_path(paths=['timeline',
                                          location,
                                          date_start.strftime('%Y-%m-%d'),
                                          date_end.strftime('%Y-%m-%d')],
                                   key=self.api_key)
        url = '/'.join([
            self.base_url.strip('/'),
            path.strip('/'),
        ])
        response = self.call('GET', url)

        if response.ok:
            return json.loads(response.content)
        raise ApiCallException('invalid response from api server',
                               url=url,
                               content=response.content,
                               status_code=response.status_code)

    def _generate_path(self, paths: list, **kwargs) -> str:
        """
        Генерация пути с квери-параметрами
        :param paths: Список из путей
        :param kwargs: Квери-параметры
        :return: Путь с квери-параметрами
        """
        query = self._generate_query(**kwargs)
        path = '/'.join(paths)
        if query:
            return '?'.join([path, query])
        return path

    @staticmethod
    def _generate_query(**kwargs) -> str:
        """
        Генерация строки с квери-параметрами
        :param kwargs: Квери-параметры
        :return: Строка состоящая из квери-параметров для вставки в путь
        """
        return '&'.join([
            f"{key}={value}"
            for key, value in kwargs.items()
            if value
        ])

    @staticmethod
    def call(method: str, url: str, json_data: dict = None, params: dict = None):
        """
        Отправка запроса на сторонний сервис
        """
        return request(
            method=method,
            url=url,
            json=json_data,
            params=params,
        )


open_weather_api = OpenWeatherApi(WEATHER_BASE_URL, WEATHER_API_KEY)
