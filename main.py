from config import config
from src.dbmanager import DBManager


def main():
    # hh = HeadHunter()
    #
    #
    # employers_list = ['67611', '15478', '80', '6093775', '160748', '1329', '1532045', '3853446', '3992497', '1740'] # Тензор 67611, VK 15478, Альфа Банк 80, Aston 6093775, АО «ГНИВЦ» 160748, Европлан 1329, CarPrice 1532045, Solit Clouds 3853446, Keepcode 3992497, Яндекс 1740
    # # #employers_list = ['67611', '80']
    # data = hh.get_hh_data(employers_list)
    #
    params = config()
    #
    # create_database('headhunter', params)
    # save_data_to_database(data, 'headhunter', params)
    # print("Данные в headhunter успешно добавлены")

    db_manager = DBManager('headhunter', params)
    for i in db_manager.get_vacancies_with_keyword('Python'):
        print(i)


if __name__ == '__main__':
    main()
