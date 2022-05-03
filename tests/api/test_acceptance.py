from api import calculator_api
import pytest
from helpers.decorators import Test


@Test('Сервис возвращает корректный результат умножения аргументов', story='positive')
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
        r = calculator_api.multiply(a, b)
        r.should_has_body(expected_result)


@Test('Сервис возвращает сообщение об ошибке если переданные аргументы не корректны.', story='negative')
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
        r = calculator_api.multiply(a, b)
        r.should_has_body("Something went wrong :(")
