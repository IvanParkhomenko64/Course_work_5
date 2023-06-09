from parsingerror import ParsingError
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

    @staticmethod
    def get_salary(salary):
        formatted_salary = [None, None]
        if salary and salary['from'] and salary['from'] != 0:
            formatted_salary[0] = salary['from'] if salary['currency'].lower() == 'rur' else salary['from'] * 80
        if salary and salary['to'] and salary['to'] != 0:
            formatted_salary[1] = salary['to'] if salary['currency'].lower() == 'rur' else salary['to'] * 80
        return formatted_salary

    def get_hh_data(self, employers_ids: list[str]) -> list[dict[str, Any]]:
        """Получение данных о работодателях и их вакансиях."""
        data = []
        for employer_id in employers_ids:
            employer_data = requests.get(f'https://api.hh.ru/employers/{employer_id}', headers=self.__header, params=self.__params).json()
            vacancies_data = []
            count_open_vacancies = int(employer_data['open_vacancies'])
            if count_open_vacancies <= 100:
                params = {
                    'employer_id': employer_id,  # ID 2ГИС
                    'page': 0,  # Номер страницы
                    'per_page': 100  # Кол-во вакансий на 1 странице
                }
                response = requests.get('https://api.hh.ru/vacancies', headers=self.__header, params=params).json()
                vacancies_data.extend(response['items'])
            elif count_open_vacancies >= 2000:
                for i in range(19):
                    params = {
                        'employer_id': employer_id,  # ID 2ГИС
                        'page': i,  # Номер страницы
                        'per_page': 100  # Кол-во вакансий на 1 странице
                    }
                    response = requests.get('https://api.hh.ru/vacancies', headers=self.__header, params=params).json()
                    vacancies_data.extend(response['items'])
            else:
                for i in range(count_open_vacancies // 100):
                    params = {
                        'employer_id': employer_id,  # ID 2ГИС
                        'page': i,  # Номер страницы
                        'per_page': 100  # Кол-во вакансий на 1 странице
                    }
                    response = requests.get('https://api.hh.ru/vacancies', headers=self.__header, params=params).json()
                    vacancies_data.extend(response['items'])
            data.append({
                'employer': employer_data,
                'vacancies': vacancies_data
            })
        return data

    def get_request(self):
        response = requests.get('https://api.hh.ru/employers/80', headers=self.__header, params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()['open_vacancies']

    def get_page(self, page):
        params = {
            'employer_id': 80,  # ID 2ГИС
            'page': page,  # Номер страницы
            'per_page': 100  # Кол-во вакансий на 1 странице
        }
        response = requests.get('https://api.hh.ru/vacancies', headers=self.__header, params=params)
        return response.json()

    def get_vacancies(self, pages_count=1):
        while self.__params['page'] < pages_count:
            print(f"HeadHunter, Парсинг страницы {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print('Ошибка получения данных!')
                break
            print(f"Найдено ({len(values)}) вакансий.")
            self.__vacancies.extend(values)
            self.__params['page'] += 1

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        for vacancy in self.__vacancies:
            salary_from, salary_to = self.get_salary(vacancy['salary'])
            formatted_vacancies.append({
                'id': vacancy['id'],
                'title': vacancy['name'],
                'url': vacancy['alternate_url'],
                'salary_from': salary_from,
                'salary_to': salary_to,
                'employer': vacancy['employer']['name'],
                'api': 'HeadHunter'
            })
        return formatted_vacancies
