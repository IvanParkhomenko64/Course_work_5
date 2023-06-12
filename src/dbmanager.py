import psycopg2


class DBManager:
    def __init__(self, database_name: str, params: dict):
        self.database_name = database_name
        self.params = params
        self.conn = psycopg2.connect(dbname=database_name, **params)

    def get_companies_and_vacancies_count(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT name, open_vacancies FROM employers
                """
            )
            companies_and_vacancies_count = cur.fetchall()
        self.conn.commit()
        self.conn.close()
        return companies_and_vacancies_count

    def get_all_vacancies(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT employers.name, vacancies.name, salary_from, salary_to, vacancy_url FROM employers, vacancies
                WHERE vacancies.employer_id = employers.employer_id
                """
            )
            all_vacancies = cur.fetchall()
        self.conn.commit()
        self.conn.close()
        return all_vacancies

    def get_avg_salary_to(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG(salary_to) FROM vacancies
                """
            )
            avg_salary_to = cur.fetchall()
        self.conn.commit()
        self.conn.close()
        return int(avg_salary_to)

    def get_vacancies_with_higher_salary_to(self):
        with self.conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT name FROM vacancies
                WHERE salary_to > {self.get_avg_salary_to()}
                """
            )
            vacancies_with_higher_salary_to = cur.fetchall()
        self.conn.commit()
        self.conn.close()
        return vacancies_with_higher_salary_to

    def get_vacancies_with_keyword(self, keyword):
        with self.conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT name FROM vacancies
                WHERE name LIKE '%{keyword}%'
                """
            )
            vacancies_with_keyword = cur.fetchall()
        self.conn.commit()
        self.conn.close()
        return vacancies_with_keyword
