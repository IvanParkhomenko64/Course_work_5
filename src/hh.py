from src.parsingerror import ParsingError
import requests
from typing import Any


class HeadHunter:
    """Класс для получения данных о вакансиях с сайта HeadHunter"""

    def __init__(self):
        self.__header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0"}
        self.__params = {
            "page": 0,  # номер страницы
            "per_page": 100  # количество отображаемых записей на странице
        }
        self.__vacancies = []

    def get_hh_data(self, employers_ids: list[str]) -> list[dict[str, Any]]:
        """Получение данных о работодателях и их вакансиях."""
        data = []
        for employer_id in employers_ids:
            try:
                employer_data = requests.get(f'https://api.hh.ru/employers/{employer_id}', headers=self.__header,
                                             params=self.__params).json()
            except ParsingError:
                print('Ошибка получения данных о работодателях!')
                break
            vacancies_data = []
            count_open_vacancies = int(employer_data['open_vacancies'])
            if count_open_vacancies <= 100:
                params = {
                    'employer_id': employer_id,
                    'page': 0,
                    'per_page': 100
                }
                try:
                    response = requests.get('https://api.hh.ru/vacancies', headers=self.__header, params=params).json()
                except ParsingError:
                    print('Ошибка получения данных о вакансиях!')
                    break
                vacancies_data.extend(response['items'])
            elif count_open_vacancies >= 2000:
                for i in range(19):
                    params = {
                        'employer_id': employer_id,
                        'page': i,
                        'per_page': 100
                    }
                    try:
                        response = requests.get('https://api.hh.ru/vacancies', headers=self.__header, params=params).json()
                    except ParsingError:
                        print('Ошибка получения данных о вакансиях!')
                        break
                    vacancies_data.extend(response['items'])
            else:
                for i in range(count_open_vacancies // 100):
                    params = {
                        'employer_id': employer_id,
                        'page': i,
                        'per_page': 100
                    }
                    try:
                        response = requests.get('https://api.hh.ru/vacancies', headers=self.__header, params=params).json()
                    except ParsingError:
                        print('Ошибка получения данных о вакансиях!')
                        break
                    vacancies_data.extend(response['items'])
            data.append({
                'employer': employer_data,
                'vacancies': vacancies_data
            })
        return data
