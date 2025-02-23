import os
import urllib

import requests
from dotenv import load_dotenv

load_dotenv()


def get_currency(vacancy_currency: str) -> list[dict]:
    """
    Функция получения актуального курса валют
    """

    if vacancy_currency == "RUR":
        vacancy_currency = "RUB"

    apikey = os.getenv("EXCHANGE_APIKEY")

    url = "https://api.currencyapi.com/v3/latest"
    params = {"base_currency": "RUB"}
    encoded_params = urllib.parse.urlencode(params)
    full_url = f"{url}?{encoded_params}"
    headers = {"apikey": f"{apikey}"}

    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        api_result = response.json()
        result = round(1 / api_result["data"][vacancy_currency]["value"], 2)
        return result
    except requests.exceptions.HTTPError:
        raise requests.exceptions.HTTPError("HTTP Error")
    except requests.exceptions.RequestException:
        raise requests.exceptions.RequestException("Request Exception Error")


def data_filter(data: list, keyword: int, criteria: str) -> list | str:
    """
    Функция фильтрации списка со словарями вакансий относительно keyword(категории) и criteria(слова/цифр)
    """

    keywords_area = {"1": "id", "2": "name"}
    result = []

    for filter_vac in data:
        if keyword in [1, 2]:
            if criteria in filter_vac[keywords_area[str(keyword)]]:
                result.append(filter_vac)
        elif keyword == 3:
            url_num = filter_vac["alternate_url"].split("/")
            if criteria == url_num[-1]:
                result.append(filter_vac)
        elif keyword == 4:
            if filter_vac["salary"] and criteria:
                pay_range = criteria.split(" - ")
                if filter_vac["salary"]["currency"] != "RUR":
                    currency_multiplier = get_currency(filter_vac["salary"]["currency"])
                    filter_salary_from = (
                        filter_vac["salary"]["from"] * currency_multiplier
                        if filter_vac["salary"]["from"]
                        else None
                    )
                    filter_salary_to = (
                        filter_vac["salary"]["to"] * currency_multiplier
                        if filter_vac["salary"]["to"]
                        else None
                    )
                else:
                    filter_salary_from = filter_vac["salary"]["from"]
                    filter_salary_to = filter_vac["salary"]["to"]

                if not filter_salary_from:
                    filter_salary_from = 0
                if not filter_salary_to:
                    filter_salary_to = 999999999999999999999999

                if (
                    int(pay_range[0]) >= filter_salary_from
                    and int(pay_range[1]) <= filter_salary_to
                ):
                    result.append(filter_vac)
            elif filter_vac["salary"] is None and criteria is None:
                result.append(filter_vac)
        else:
            if criteria in filter_vac["snippet"]["responsibility"]:
                result.append(filter_vac)
    else:
        if result:
            return result
        else:
            return "Вакансия не найдена"


if __name__ == "__main__":
    print(get_currency("USD"))
