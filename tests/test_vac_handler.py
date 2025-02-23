from unittest.mock import patch

import pytest

from src.vac_handler import VacHandler


def test_wrong_input():
    with pytest.raises(TypeError):
        VacHandler(1, "", "", 0, 1, "", "")


def test_average_salary_none():
    test1 = VacHandler("", "", "", None, 1, "", "")
    test2 = VacHandler("", "", "", 2, None, "", "")
    assert test1.average_salary == 1
    assert test2.average_salary == 2


def test_salary_contract_wrong_type(fixt_vacs):
    with pytest.raises(TypeError):
        var = fixt_vacs[0] > "123"
        var = fixt_vacs[0] < "123"


def test_salary_none(capsys):
    test_none = VacHandler("", "None", "", None, None, None, "")
    test_ok = VacHandler("", "ok", "", 1, 2, "test", "")

    var = test_none > test_none
    message = capsys.readouterr()
    assert message.out.strip() == "У обоих вакансий зп не задана. Сравнение невозможно."

    var = test_none > test_ok
    message1 = capsys.readouterr()
    var = test_ok > test_none
    message2 = capsys.readouterr()
    assert message1.out.strip() == message2.out.strip()


def test_salary_contrast(capsys):
    test_1 = VacHandler("1", "1", "", 2, 2, "RUR", "")
    test_2 = VacHandler("2", "2", "", 1, 2, "RUR", "")
    test_3 = VacHandler("3", "3", "", None, None, None, "")
    test_4 = VacHandler("4", "4", "", None, None, None, "")

    assert test_1 > test_2
    assert not test_2 > test_1
    assert test_1 > test_3
    assert not test_3 > test_4


@patch("src.utils.requests.get")
def test_currency_contrast_with_api(mock_api, capsys):
    rur_vac = VacHandler("", "RUR vac", "", 1, 1, "RUR", "")
    usd_vac = VacHandler("", "USD vac", "", 10, 11, "USD", "")

    mock_api.return_value.json.return_value = {"data": {"USD": {"value": 0.01}}}

    assert rur_vac < usd_vac
    assert not rur_vac > usd_vac


def test_vac_to_dict():
    test_vac = VacHandler("2", "Вторая вакансия", "1/1", None, None, "RUR", "test2")
    test_dict = {
        "id": "2",
        "name": "Вторая вакансия",
        "alternate_url": "1/1",
        "salary": None,
        "snippet": {"responsibility": "test2"},
    }

    assert test_vac.vacancy_to_dict == test_dict
    assert (
        VacHandler.vacancy_from_dict(test_dict).vacancy_to_dict
        == test_vac.vacancy_to_dict
    )
