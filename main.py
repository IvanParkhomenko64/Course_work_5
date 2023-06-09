from hh import HeadHunter


def main():
    vacancies_json = []
    #keyword = input('Введите ключевое слово для поиска: ')
    hh = HeadHunter()
    #hh.get_vacancies(pages_count=10)
    #print(hh.get_request())
    #print(hh.get_page(0))
    employers_list = ['733', '67611']
    n = hh.get_hh_data(employers_list)
    print(n[1]['vacancies'])


if __name__ == '__main__':
    main()
