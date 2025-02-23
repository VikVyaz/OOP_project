import pytest

from src.vac_handler import VacHandler


@pytest.fixture()
def fixt_vacs():
    return [
        VacHandler(
            "1",
            "Первая вакансия",
            "https://hh.ru/vacancy/91178034",
            10,
            15,
            "RUR",
            "test1",
        ),
        VacHandler("2", "Вторая вакансия", "1/1", None, None, "RUR", "test2"),
    ]


@pytest.fixture()
def fixt_vacs_list():
    return [
        {
            "id": "1",
            "name": "Первая вакансия",
            "alternate_url": "https://hh.ru/vacancy/91178034",
            "salary": {"from": 10, "to": 15, "currency": "RUR"},
            "snippet": {"responsibility": "test1"},
        },
        {
            "id": "2",
            "name": "Вторая вакансия",
            "alternate_url": "1/1",
            "salary": None,
            "snippet": {"responsibility": "test2"},
        },
    ]


@pytest.fixture()
def fixt_currency_rates() -> list:
    api_out_data = {"data": {"test": {"value": 2}}}

    out_data = 0.5

    return [api_out_data, out_data]
