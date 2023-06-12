import psycopg2
from typing import Any


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о работодателях и их вакансиях"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(
        f"""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '{database_name}' 
        AND pid <> pg_backend_pid();
        """
    )

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                open_vacancies INTEGER
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                name VARCHAR,
                salary_from INTEGER,
                salary_to INTEGER,
                vacancy_url TEXT
            )
        """)
    conn.commit()
    conn.close()


def get_salary(salary):
    """Вспомогательная функция для проверки наличия данных о ЗП и их записи в переменную списка"""
    formatted_salary = [None, None]
    if salary and salary['from'] and salary['from'] != 0:
        formatted_salary[0] = salary['from']
    if salary and salary['to'] and salary['to'] != 0:
        formatted_salary[1] = salary['to']
    return formatted_salary


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных о работодателях и их вакансиях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data:
            employer_data = employer['employer']
            cur.execute(
                """
                INSERT INTO employers (name, open_vacancies)
                VALUES (%s, %s)
                RETURNING employer_id
                """,
                (employer_data['name'], employer_data['open_vacancies'])
            )
            employer_id = cur.fetchone()[0]
            vacancies_data = employer['vacancies']
            for vacancy in vacancies_data:
                salary_from, salary_to = get_salary(vacancy['salary'])
                cur.execute(
                    """
                    INSERT INTO vacancies (employer_id, name, salary_from, salary_to, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (employer_id, vacancy['name'], salary_from, salary_to,
                     vacancy['alternate_url'])
                )
    conn.commit()
    conn.close()
