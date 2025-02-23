from unittest.mock import MagicMock, patch

import pytest
import requests

from src.utils import data_filter, get_currency


@patch("src.utils.requests.get")
def test_show_currency_rates(mock_get: MagicMock, fixt_currency_rates: list) -> None:
    """Тест для src.utils.get_currency()"""

    mock_get.return_value.json.return_value = fixt_currency_rates[0]
    assert get_currency("test") == fixt_currency_rates[1]


@patch("src.utils.requests.get")
def test_show_currency_rates_errors(
    mock_get: MagicMock, fixt_currency_rates: list
) -> None:
    """Тест для обработки ошибок в src.utils.get_currency"""

    mock_get.side_effect = requests.exceptions.HTTPError
    with pytest.raises(requests.exceptions.HTTPError):
        error = get_currency("RUR")

    mock_get.side_effect = requests.exceptions.RequestException
    with pytest.raises(requests.exceptions.RequestException):
        error = get_currency("RUR")


vacs_list = [
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

usd_vac = [
    {
        "id": "3",
        "name": "Третья вакансия",
        "alternate_url": "1/10",
        "salary": {"from": 1, "to": 100, "currency": "USD"},
        "snippet": {"responsibility": "test3"},
    }
]

none_vac = [
    {
        "id": "4",
        "name": "None вакансия",
        "alternate_url": "1/10",
        "salary": {"from": None, "to": None, "currency": "RUR"},
        "snippet": {"responsibility": "test4"},
    }
]


@patch("src.utils.requests.get")
@pytest.mark.parametrize(
    "keyword, criteria, expected_list",
    [
        (1, "1", [vacs_list[0]]),
        (2, "Первая вакансия", [vacs_list[0]]),
        (3, "91178034", [vacs_list[0]]),
        (4, "11 - 14", [vacs_list[0]]),
        (5, "test1", [vacs_list[0]]),
        (1, "2", [vacs_list[1]]),
        (2, "Вторая вакансия", [vacs_list[1]]),
        (3, "1", [vacs_list[1]]),
        (4, None, [vacs_list[1]]),
        (5, "test2", [vacs_list[1]]),
        (1, "error", "Вакансия не найдена"),
        (2, "error", "Вакансия не найдена"),
        (3, "error", "Вакансия не найдена"),
        (4, "1 - 1", "Вакансия не найдена"),
        (5, "error", "Вакансия не найдена"),
    ],
)
def test_data_filter(mock_get, keyword, criteria, expected_list, fixt_currency_rates):
    mock_get.return_value.json.return_value = fixt_currency_rates[0]
    assert data_filter(vacs_list, keyword, criteria) == expected_list


@patch("src.utils.requests.get")
def test_usd_n_none_vacs(mock_get):

    mock_get.return_value.json.return_value = {"data": {"USD": {"value": 0.01}}}
    assert data_filter(usd_vac, 4, "150 - 151") == usd_vac
    assert data_filter(none_vac, 4, "1 - 10") == none_vac
