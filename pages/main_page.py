import environment
import allure
from helpers.waiting_helper import wait_until


class MainPage:
    def __init__(self, page):
        self.page = page
        self.first_value_input = page.locator('input:nth-of-type(1)')
        self.second_value_input = page.locator('input:nth-of-type(2)')
        self.submit_button = page.locator('#submit_btn')
        self.result_text = page.locator('#result')
        self.error_text = page.locator('.error-text')

        self.page.goto(f"{environment.get_environment('BASE_URL')}/")

    @allure.step('Ввести в форму перемножения "{first_value}" и "{second_value}"')
    def fill_form(self, first_value, second_value):
        self.first_value_input.fill(str(first_value))
        self.second_value_input.fill(str(second_value))
        return self

    @allure.step("Отправить форму на сервер")
    def submit(self):
        self.submit_button.click()

    @allure.step('Проверить что отображаемый результат равен "{value}"')
    def check_that_result_is(self, value):
        if self.error_text.is_visible():
            raise AssertionError(f'Ожидаемый результат <Result: {value}>. Актуальный <{self.error_text.inner_text()}>')
        else:
            wait_until(lambda: self.get_result() == value)
            assert self.result_text.inner_text() == value

    @allure.step('Проверить что присутствует сообщение об ошибке "{error_text}"')
    def check_that_error_is(self, error_text):
        assert self.error_text.inner_text() == error_text

    def get_result(self):
        self.page.wait_for_load_state("networkidle")
        return self.result_text.inner_text()

