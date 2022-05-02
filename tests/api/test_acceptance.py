from api import calculator_api
import pytest
from helpers.decorators import Test, Step, Check
import allure

@Test('Сервис возвращает корректный результат умножения аргументов')
@pytest.mark.parametrize('a, b, expected_result', [
    (0, 5, 0),
    (5, 0, 0),
    (1, 5, 5),
    (5, 1, 5),
    (100, 5, 500),
    (5, 100, 500),
    (0, 0, 0),
    (100, 100, 10000)
])
def test_service_return_result_of_multiply_arguments(a, b, expected_result):
    with Step('Перемножаем числа "{a}" и "{b}"'):
        r = calculator_api.multiply(a, b)

    with Check('Сервис возвращает результат, равный {expected_result}'):
        assert int(r.text) == expected_result


@Test('Сервис возвращает сообщение об ошибке если переданные аргументы не корректны.')
@pytest.mark.parametrize('a, b', [
    (1.1, 1),
    (1, 1.1),
    ("1,1", "1"),
    ("1", "2,2"),
    ("F", "2"),
    ("1", "a"),
    ("", "1"),
    ("1", ""),
    (" ", "1"),
    ("1", " "),
    ("/", "1"),
    ("1", "/"),
    ("101", "1"),
    ("1", "101"),
    ("-1", "1"),
    ("1", "-1"),
])
def test_service_return_error_message_if_arguments_incorrect(a, b):
    with Step('Перемножаем аргументы "{a}" и "{b}"'):
        r = calculator_api.multiply(a, b)

    with Check('Сервис возвращает сообщение об ошибке'):
        assert r.text == "Something went wrong :("
