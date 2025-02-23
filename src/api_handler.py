import requests

from src.abstract_cls import Parser


class HeadHunterAPI(Parser):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100, "area": 113}
        self.__vacancies = []

    def get_vacancies(self, keyword: str):
        """
        Метод получения вакансий с HeadHunter по ключевому слову в названии в вакансии
        """
        self.__params["text"] = f"NAME:{keyword}"
        while self.__params.get("page") != 5:
            response = requests.get(
                self.__url, headers=self.__headers, params=self.__params
            )
            response.raise_for_status()
            vacancies = response.json()["items"]
            self.vacancies.extend(vacancies)
            self.__params["page"] += 1

    @property
    def vacancies(self):
        return self.__vacancies

    def set_sort_by_top_salary(self):
        """Метод установки сортировки по топ зп"""
        self.__params["order_by"] = "salary_desc"

    def set_default_search_params(self):
        """Метод сброса сортировки на стандартную"""
        self.__params.pop("order_by", None)

    @property
    def print_init(self):
        """Технический метод для тестов"""
        return [self.__url, self.__headers, self.__params]


# if __name__ == '__main__':
#     x = HeadHunterAPI()
#     x.get_vacancies("Python")
#     print(x.vacancies)
