from unittest.mock import mock_open, patch

import pytest

from src.exceptions import WrongAttributeChoiceError
from src.file_handler import JSONHandler


def test_init():
    test_cls = JSONHandler()
    assert "default_vacancies_file.json" in str(test_cls.show_path())
    test_cls_2 = JSONHandler("test")
    assert "test.json" in str(test_cls_2.show_path())
    assert test_cls.show_vacs_id() == []


def test_change_id_list():
    test_cls = JSONHandler()
    test_cls.change_id_list("test", "add")
    assert test_cls.show_vacs_id() == ["test"]
    test_cls.change_id_list("test", "delete")
    assert test_cls.show_vacs_id() == []
    test_cls.change_id_list("test", "add")
    test_cls.change_id_list("test", "drop")
    assert test_cls.show_vacs_id() == []

    with pytest.raises(WrongAttributeChoiceError):
        test_cls.change_id_list("test", "error")


def test_error_type():
    test_cls = JSONHandler()

    with pytest.raises(TypeError):
        test_cls.add_vacancies("123")

    with pytest.raises(TypeError):
        test_cls.delete_vacancies("123")


@patch("builtins.open", new_callable=mock_open)
@patch("json.dump")
@patch("json.load")
def test_add_vacancy(mock_load, mock_dump, mock_open, fixt_vacs_list, fixt_vacs):
    test_cls = JSONHandler()

    mock_load.return_value = []
    mock_dump.return_value = 0
    assert test_cls.add_vacancies(fixt_vacs[0]) is None
    assert test_cls.show_vacs_id() == ["1"]

    test_cls.change_id_list("1", "drop")
    mock_load.side_effect = FileNotFoundError
    assert test_cls.add_vacancies(fixt_vacs[0]) is None
    assert test_cls.show_vacs_id() == ["1"]


def test_get_filtered_from_file():
    pass


def test_delete_vacancies():
    pass
