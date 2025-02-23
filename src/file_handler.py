import json
import os
from pathlib import Path

from src.abstract_cls import BaseFileHandler

# from src.api_handler import HeadHunterAPI
from src.exceptions import FileEmptyError, WrongAttributeChoiceError
from src.utils import data_filter
from src.vac_handler import VacHandler


class JSONHandler(BaseFileHandler):
    """
    Класс для работы с вакансиями в формате JSON файла.
    """

    def __init__(self, path="default_vacancies_file"):
        if path == "default_vacancies_file":
            self.__path = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "default_vacancies_file.json"
            )
        else:
            self.__path = (
                Path(__file__).resolve().parent.parent / "data" / f"{path}.json"
            )
        self.__id_list = []

    def show_vacs_id(self):
        """Технический метод для вывода списка id вакансий, который 'прошли' через экземпляр класса"""
        return self.__id_list

    def show_path(self):
        """Технический метод для вывода path"""
        return self.__path

    def change_id_list(self, vac_id: str, add_del_or_drop: str):
        """Метод работы с __id_list:
        в add_vacancies добавление id,
        в delete_vacancies удаление id,
        или очистка, если потребуется"""

        if add_del_or_drop == "add":
            self.__id_list.append(vac_id)
        elif add_del_or_drop == "delete":
            self.__id_list = [v for v in self.__id_list if v != vac_id]
        elif add_del_or_drop == "drop":
            self.__id_list = []
        else:
            raise WrongAttributeChoiceError(
                'Неправильный атрибут "add_or_del":'
                "add(добавление в список), delete(удаление из списка) или drop(обнуления)"
            )

    @staticmethod
    def __vac_validation(vacancy):

        if not isinstance(vacancy, VacHandler):
            raise TypeError("Вакансия должна быть VacHandler")

    @staticmethod
    def __read_file(path, add_or_del="add"):

        if add_or_del not in ["add", "del"]:
            raise WrongAttributeChoiceError(
                'Аттрибут add_or_del может иметь значения только "add" или "del"'
            )

        with open(path, "r+", encoding="utf-8") as file:

            if add_or_del == "add":
                try:
                    data = json.load(file)
                    if not isinstance(data, list):
                        data = [data]
                except (json.JSONDecodeError, ValueError):
                    data = []
                return data
            else:
                try:
                    data = json.load(file)
                    return data
                except json.JSONDecodeError:
                    raise FileEmptyError("Файл пуст")

    @staticmethod
    def __save_file(path, data):

        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_vacancies(self, vacancy: VacHandler):
        """Метод добавления вакансии в json файл. Дублирование исключено"""

        self.__vac_validation(vacancy)

        try:
            data = self.__read_file(self.__path)

            if not any(v["id"] == vacancy.id for v in data):
                data.append(vacancy.vacancy_to_dict)
                self.change_id_list(vacancy.id, "add")
                self.__save_file(self.__path, data)
        except FileNotFoundError:
            self.change_id_list(vacancy.id, "add")
            self.__save_file(self.__path, [vacancy.vacancy_to_dict])

    def get_filtered_from_file(self, keyword: int, criteria: str | int | None):
        """Метод получения из файла отфильтрованных по keyword(категории) и criteria(слову/числу) вакансий"""

        try:
            with open(self.__path, "r+", encoding="utf-8") as file:

                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    raise FileEmptyError("Файл пуст")

            return data_filter(data, keyword, criteria)

        except FileNotFoundError:
            print("Отсутствует файл для фильтрации")

    def delete_vacancies(self, vacancy: VacHandler):
        """Метод удаления из файла заданной вакансии"""

        self.__vac_validation(vacancy)

        try:
            data = self.__read_file(self.__path, "del")

            result_data = [v for v in data if v["id"] != vacancy.id]
            if len(result_data) != len(data):
                self.change_id_list(vacancy.id, "delete")

            self.__save_file(self.__path, data)

        except FileNotFoundError:
            print("Файл отсутствует")
        except ValueError:
            print("Вакансия отсутствует")


if __name__ == "__main__":

    print("------------------НАЧАЛО СИНТЕТИЧЕСКОЙ ПРОВЕРКИ------------------")
    path_to_file = "../data/default_vacancies_file.json"
    if os.path.exists(path_to_file):
        os.remove(path_to_file)
    if os.path.exists(path_to_file):
        print("Файл имеется, хотя не должен")
    else:
        print("Файл удалился, как и задумывалось")
    x = JSONHandler()
    vac = VacHandler(
        "1", "Первая вакансия", "https://hh.ru/vacancy/91178034", 10, 15, "RUR", "test1"
    )
    x.add_vacancies(vac)
    vac2 = VacHandler("2", "Вторая вакансия", "1/1", None, None, "RUR", "test2")
    x.add_vacancies(vac2)
    print('Должно быть ["1", "2"]: ', x.show_vacs_id())

    print("id_1_1", x.get_filtered_from_file(1, "1"))
    print("id_2_2", x.get_filtered_from_file(2, "Вторая вакансия"))
    print("id_1_3", x.get_filtered_from_file(3, "91178034"))
    print("id_1_4", x.get_filtered_from_file(4, "10 - 15"))
    print("id_1_5", x.get_filtered_from_file(5, "test1"))
    print("None_6", x.get_filtered_from_file(4, None))

    x.delete_vacancies(
        vac2
    )  # После этого в data/vacancies.json остается "Первая вакансия"
    print('Должно быть ["1"]: ', x.show_vacs_id())

    print("------------------КОНЕЦ СИНТЕТИЧЕСКОЙ ПРОВЕРКИ------------------", end="\n")

#     print('------------------НАЧАЛО ПРОВЕРКИ C РЕАЛЬНОЙ API------------------')
#     if os.path.exists(path_to_file):
#         os.remove(path_to_file)
#     if os.path.exists(path_to_file):
#         print('Файл имеется, хотя не должен')
#     else:
#         print('Файл удалился, как и задумывалось')
#
#     q = HeadHunterAPI()
#     print(q.print_params)
#     q.set_sort_by_top_salary()
#     print(q.print_params)
#     q.get_vacancies("Python")
#     qr = q.vacancies[:3]
#     api_vac_1 = VacHandler.vacancy_from_dict(qr[0])
#     api_vac_2 = VacHandler.vacancy_from_dict(qr[1])
#     api_vac_3 = VacHandler.vacancy_from_dict(qr[2])
#     print(api_vac_1.id)
#     json_file = JSONHandler()
#
#     json_file.add_vacancies(api_vac_1)
#     print(json_file.show_vacs_id())
#
#     json_file.add_vacancies(api_vac_2)
#     print(json_file.show_vacs_id())
#
#     json_file.add_vacancies(api_vac_3)
#     print(json_file.show_vacs_id())
#
#     print('Вакансия с id 116078697 ---', json_file.get_filtered_from_file(1, '116078697'))
#     print('Вакансия с id 116197378 ---', json_file.get_filtered_from_file(2, 'Senior'))
#     print('Вакансия с id 116197378 ---', json_file.get_filtered_from_file(3, '116197378'))
#     print('Вакансия не найдена ---', json_file.get_filtered_from_file(4, '50000 - 70000'))
#     print('Вакансия не найдена ---', json_file.get_filtered_from_file(4, '500000 - 700000'))
#     print(json_file.get_filtered_from_file(5, 'Отвечать за инфраструтурные решения'))
#     print('Вакансия не найдена ---', json_file.get_filtered_from_file(4, None))
#
#     print('------------------КОНЕЦ API ПРОВЕРКИ------------------', end='\n')
