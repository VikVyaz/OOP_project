import os
import re

from src.api_handler import HeadHunterAPI
from src.file_handler import JSONHandler
from src.utils import data_filter
from src.vac_handler import VacHandler


def user_input():
    # search_criteria = input("Введите слово для поиска по названию вакансии:\n")
    #
    # number_of_vacs = input("Сколько вакансий записать в файл(цифра):\n")
    #
    # input_keyword = input(
    #     "Введите категорию фильтрации вакансий (цифрой 1-5):\n"
    #     "1 - id вакансии\n"
    #     "2 - название вакансии\n"
    #     "3 - url вакансии\n"
    #     "4 - зарплата\n"
    #     "5 - описание вакансии (ответственность)\n"
    # )
    #
    # input_criteria = input(
    #     "Критерий для категории поиска:\n"
    #     "для id - номер\n"
    #     'для зарплаты - формат "10000 - 15000"\n'
    #     "для url - номер (https://hh.ru/vacancy/<номер>)\n"
    #     "для названия вакансии или описания - слово\n"
    # )
    #
    # top_salary_quantity = input(
    #     "Введите количество топовых по зарплате вакансий (цифра):\n"
    # )
    #
    # if int(input_keyword) not in [1, 2, 3, 4, 5]:
    #     raise TypeError("Категория поиска должна быть введена цифрой от 1 до 5")
    # if input_keyword == "4" and not bool(re.fullmatch(r"^\d+ - \d+$", input_criteria)):
    #     raise TypeError(
    #         'Критерий для категории "зарплата" должна быть формата "<цифра> - <цифра>"'
    #     )

    search_criteria = 'Python'
    number_of_vacs = '10'
    input_keyword = '2'
    input_criteria = 'Python'
    top_salary_quantity = '5'

    default_api_result = HeadHunterAPI()
    default_api_result.get_vacancies(search_criteria)  # сортировка не по зп

    # list[dict] с вакансиями
    api_search_result = default_api_result.vacancies

    # Фильтрация по категории и критерию
    filtered_vacs = data_filter(api_search_result, int(input_keyword), input_criteria)

    # Записываем в JSON файл, на всякий случай удаляем возможно присутствующий JSON файл
    path = "./data/vacancies.json"
    if os.path.exists(path):
        os.remove(path)
    json_file_handler = JSONHandler()
    for vac in filtered_vacs[: int(number_of_vacs)]:
        json_file_handler.add_vacancies(VacHandler.vacancy_from_dict(vac))

    # Вывод списка id вакансий в json файле
    print(json_file_handler.show_vacs_id())

    # Получение топ N вакансий с сортировкой по величине зп
    top_salary_api_result = HeadHunterAPI()
    top_salary_api_result.set_sort_by_top_salary()
    top_salary_api_result.get_vacancies(search_criteria)  # сортировка по зп
    top_salary_result = top_salary_api_result.vacancies[: int(top_salary_quantity)]

    # Запись их в отдельный файл, на всякий случай удаляя предыдущий файл
    path = "./data/top_salary_vacancies.json"
    if os.path.exists(path):
        os.remove(path)
    top_salary_json_file = JSONHandler("salary")
    for top_salary_vac in top_salary_result:
        top_salary_json_file.add_vacancies(VacHandler.vacancy_from_dict(top_salary_vac))

    # Вывод id вакансий с топ зп
    # for id_vac in top_salary_json_file.show_vacs_id():
    #     print(int(id_vac), sep=", ")
    print(top_salary_json_file.show_vacs_id())


if __name__ == "__main__":
    user_input()
