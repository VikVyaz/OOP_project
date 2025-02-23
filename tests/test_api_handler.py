from unittest.mock import patch

from src.api_handler import HeadHunterAPI


def test_init_and_params():
    test_api = HeadHunterAPI()
    assert test_api.print_init == [
        "https://api.hh.ru/vacancies",
        {"User-Agent": "HH-User-Agent"},
        {"text": "", "page": 0, "per_page": 100, "area": 113},
    ]
    test_api.set_sort_by_top_salary()
    assert test_api.print_init[2] == {
        "text": "",
        "page": 0,
        "per_page": 100,
        "area": 113,
        "order_by": "salary_desc",
    }
    test_api.set_default_search_params()
    assert test_api.print_init[2] == {
        "text": "",
        "page": 0,
        "per_page": 100,
        "area": 113,
    }


@patch("src.api_handler.requests.get")
def test_get_vacancies(mock_requests):
    test_api = HeadHunterAPI()
    mock_requests.return_value.json.return_value = {"items": ["test"]}
    test_api.get_vacancies("test")
    assert test_api.print_init[2] == {
        "text": "NAME:test",
        "page": 5,
        "per_page": 100,
        "area": 113,
    }
    assert len(test_api.vacancies) == 5
