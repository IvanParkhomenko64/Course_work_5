from hh import HeadHunter


def main():
    vacancies_json = []
    #keyword = input('Введите ключевое слово для поиска: ')
    hh = HeadHunter()
    hh.get_vacancies(pages_count=10)
    print(hh.get_formatted_vacancies())


if __name__ == '__main__':
    main()
