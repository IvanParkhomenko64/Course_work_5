from src.config import config
from src.dbmanager import DBManager
from src.hh import HeadHunter
from src.utils import create_database, save_data_to_database


def main():
    hh = HeadHunter()

    employers_list = ['67611', '15478', '80', '6093775', '160748', '1329', '1532045', '3853446', '3992497', '1740'] # Список ID работотаделей: Тензор 67611, VK 15478, Альфа Банк 80, Aston 6093775, АО «ГНИВЦ» 160748, Европлан 1329, CarPrice 1532045, Solit Clouds 3853446, Keepcode 3992497, Яндекс 1740
    data = hh.get_hh_data(employers_list) # получаем список данных о работодателях и их вакансиях

    params = config()  # получаем параметры для подключения к СУБД

    create_database('headhunter', params)  # создаём БД
    print("БД headhunter успешно создана")

    save_data_to_database(data, 'headhunter', params)  # заполняем созданную БД из списка data
    print("Данные в БД headhunter успешно добавлены")

    db_manager = DBManager('headhunter', params)  # создаем класс для работы с созданной БД
    for i in db_manager.get_vacancies_with_keyword('Python'):  # для примера проверяем работу метода get_vacancies_with_keyword
        print(i)


if __name__ == '__main__':
    main()
