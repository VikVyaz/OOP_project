from src.utils import get_currency


class VacHandler:
    """
    Класс работы с вакансиями в упрощенной форме, согласно актуальным потребностям
    """

    __slots__ = (
        "init_id",
        "name",
        "url",
        "salary_from",
        "salary_to",
        "currency",
        "description",
        "id",
        "average_salary",
    )

    def __init__(
            self,
            init_id: str,
            name: str,
            url: str,
            salary_from: int | None,
            salary_to: int | None,
            currency: str | None,
            description: str | None,
    ):

        self.__init_validation(
            init_id, name, url, salary_from, salary_to, currency, description
        )

        self.id = init_id
        self.name = name
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.description = description
        try:
            self.average_salary = sum([salary_from, salary_to]) / 2
        except TypeError:
            if self.salary_from:
                self.average_salary = self.salary_from
            else:
                self.average_salary = self.salary_to

    @staticmethod
    def __type_validation(target):
        if not isinstance(target, VacHandler):
            raise TypeError("Вакансия должна быть VacHandler")

    def __gt__(self, other):  # >
        self.__type_validation(other)

        try:
            if self.__salary_contrast(other) == 1:
                return True
            else:
                return False
        except TypeError:
            print('Сравнение невозможно')

    def __lt__(self, other):  # <
        self.__type_validation(other)

        try:
            if self.__salary_contrast(other) == 1:
                return False
            else:
                return True
        except TypeError:
            print('Сравнение невозможно')

    @staticmethod
    def __init_validation(
            init_id: str,
            name: str,
            url: str,
            salary_from: int | None,
            salary_to: int | None,
            currency: str | None,
            description: str | None,
    ):
        checking_in = {
            "init_id": str,
            "name": str,
            "url": str,
            "salary_from": int | None,
            "salary_to": int | None,
            "currency": str | None,
            "description": str | None,
        }

        for atr_name, atr_type in checking_in.items():
            if not isinstance(locals()[atr_name], atr_type):
                raise TypeError(f"{atr_name} задана неправильно")

    def __salary_contrast(self, other_vac):
        """
        Сравнение вакансий по зп с проверкой на курс валют в реальном времени.
        Если валюта в вакансии не RUR (рос. рубли), переводит по реальному курсу в рос. рубли
        """

        if not self.currency or not other_vac.currency:
            if self.average_salary:
                return 1
            elif other_vac.average_salary:
                return 2
            else:
                print("У обоих вакансий зп не задана. Сравнение невозможно.")

        else:
            self_average_salary = self.average_salary
            other_vac_average_salary = other_vac.average_salary

            self_currency = self.currency
            other_vac_currency = other_vac.currency

            if self.currency != "RUR":
                self_average_salary = self.average_salary * get_currency(self.currency)
                self_currency = "RUR"
            if other_vac.currency != "RUR":
                other_vac_average_salary = other_vac.average_salary * get_currency(
                    other_vac.currency
                )
                other_vac_currency = "RUR"

            salary_dict = {
                f"{self_average_salary}": {
                    "number": 1,
                    "name": f"{self.name}",
                    "currency": f"{self_currency}",
                },
                f"{other_vac_average_salary}": {
                    "number": 2,
                    "name": f"{other_vac.name}",
                    "currency": f"{other_vac_currency}",
                },
            }

            bigger_salary = str(max(self_average_salary, other_vac_average_salary))
            return salary_dict[bigger_salary]["number"]

    @classmethod
    def vacancy_from_dict(cls, vac: dict):
        """Метод трансформации dict -> объект класса VacHandler"""

        vac_id: str = vac.get("id")
        vac_name: str = vac.get("name")
        vac_url: str = vac.get("alternate_url")
        vac_salary_from: int | None = (
            vac.get("salary", {}).get("from", None) if vac["salary"] else None
        )
        vac_salary_to: int | None = (
            vac.get("salary", {}).get("to", None) if vac["salary"] else None
        )
        vac_currency: str | None = (
            vac.get("salary", {}).get("currency", None) if vac["salary"] else None
        )
        vac_description: str | None = vac.get("snippet", {}).get("responsibility", None)

        return cls(
            vac_id,
            vac_name,
            vac_url,
            vac_salary_from,
            vac_salary_to,
            vac_currency,
            vac_description,
        )

    @property
    def vacancy_to_dict(self) -> dict:
        """Метод трансформации объект класса VacHandler -> dict"""
        result = {
            "id": self.id,
            "name": self.name,
            "alternate_url": self.url,
            "salary": {
                "from": self.salary_from,
                "to": self.salary_to,
                "currency": self.currency,
            },
            "snippet": {"responsibility": self.description},
        }
        if not self.salary_from and not self.salary_to:
            result["salary"] = None
        return result


# if __name__ == '__main__':
    # print(get_currency('RUR'))
    # test_dict = {
    #     'id': '123',
    #     'name': 'test',
    #     'alternate_url': 'url',
    #     'snippet': {'responsibility': 'test'},
    #     "salary": {
    #         "from": 50,
    #         "to": 100,
    #         "currency": "KZT"
    #     }
    # }
    #
    # x1 = VacHandler('1', 'Первая вакансия', 'url1', 100, 150, 'RUR', 'test')
    # x2 = VacHandler('2', 'Вторая вакансия', 'url2', 150, 200, 'RUR', 'test')
    # x3 = VacHandler('3', 'Третья вакансия', 'url3', None, None, None, 'test')
    # x4 = VacHandler('4', 'Четвертая вакансия', 'url3', None, None, None, 'test')
    # print('сравнение', x1 > x2)
    # print('сравнение', x1 > x3)
    # print('сравнение', x3 > x4)
    # print('сравнение', x1 > 123)

    # print(x1.id,
    #       x1.name,
    #       x1.url,
    #       x1.average_salary,
    #       x1.currency,
    #       x1.description,
    #       sep=' | '
    #       )

    # test = x1.vacancy_from_dict(test_dict)
    # print(test.id,
    #       test.name,
    #       test.url,
    #       f'salary: {test.average_salary}',
    #       test.currency,
    #       test.description,
    #       sep=' | '
    #       )

    # print(x1.vacancy_to_dict)
    # print(x2.vacancy_to_dict)
    # print(x3.vacancy_to_dict)
    # print(x4.vacancy_to_dict)
