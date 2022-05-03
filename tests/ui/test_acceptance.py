from pages.main_page import MainPage
import pytest
from helpers.decorators import Test


@Test('Приложение показывает корректный результат умножения аргументов', story="positive")
def test_app_show_result_of_multiply_two_arguments(page):
    main_page = MainPage(page)
    main_page.fill_form(5, 5).submit()

    main_page.check_that_result_is("Result: 25")


@Test('При выполнении второй операции перемножения приложение показывает новый результат', story="positive")
def test_app_change_result_in_second_operation(page):
    """Приложение сделано так, что при выполнении второй и последующих операций перемножения оно не сразу очищает
    предыдущий результат, а только после того, как получит ответ. Данный тест направлен на проверку этой особенности."""
    main_page = MainPage(page)
    main_page.fill_form(10, 10).submit()
    main_page.check_that_result_is("Result: 100")

    main_page.fill_form(100, 100).submit()
    main_page.check_that_result_is("Result: 10000")


@Test('Приложение отображает сообщение об ошибке если переданные аргумент не корректны', story="negative")
@pytest.mark.parametrize('first_value, second_value', [
    (1.1, 1),
    (1, 1.1),
    ("1,1", "1"),
    ("1", "2,2"),
    ("a", "2"),
    ("1", "a"),
    ("", "1"),
    ("1", ""),
    (" ", "1"),
    ("1", " "),
    ("!", "1"),
    ("1", "?"),
    ("101", "1"),
    ("1", "101"),
    ("-1", "1"),
    ("1", "-1"),
])
def test_app_show_error_if_arguments_incorrect(page, first_value, second_value):
    main_page = MainPage(page)
    main_page.fill_form(first_value, second_value).submit()

    main_page.check_that_error_is('Only numbers from 0 to 100 and not empty')
    assert main_page.get_result() == "Result:"
