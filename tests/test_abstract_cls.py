from src.abstract_cls import BaseFileHandler, Parser


class ParserTest(Parser):

    def get_vacancies(self, keyword: str):
        pass


def test_parser():
    assert ParserTest().get_vacancies("test") is None


class BaseFileHandlerTest(BaseFileHandler):
    def add_vacancies(self, vacancy):
        pass

    def get_filtered_from_file(self, keyword: int, criteria: str):
        pass

    def delete_vacancies(self, vacancy):
        pass


def test_base_file_handler(fixt_vacs):
    test = BaseFileHandlerTest()
    assert test.add_vacancies(fixt_vacs[0]) is None
    assert test.get_filtered_from_file(1, "test") is None
    assert test.delete_vacancies(fixt_vacs[0]) is None
