import environment
import os
import allure


def pytest_addoption(parser):
    parser.addoption("--BASE_URL", action="store", default='http://13.49.131.32')
    parser.addoption("--ALLURE", action="store_true", default=False,)


def pytest_configure(config):
    """Хук pytest'а: выполняется самым первым."""
    # 1. Загружаем и сохраняем в глобальную переменную ENVIRONMENT, все настройки целевой среды
    environment.set_environment(
        BASE_URL=config.getoption("--BASE_URL")
    )

    # 2. Указываем в какую папку формировать allure-отчет,  если передана опция сохранения результатов
    # прохождения тестов в формате allure
    if config.getoption("--ALLURE", None):
        config.option.allure_report_dir = os.path.join(environment.get_logs_folder(), f'allure-results')


# def pytest_collection_modifyitems(config, items):
#     """ Хук pytest'а, который позволяет влиять на тесты во время их выполнения """
#     # 1. Allure: Для каждого теста в allure-отчете  формируем Description из docstring теста
#     for item in items:
#         title = f'<hr><font color=45B2C9>' \
#                 f'<b>{item.function.__name__}<br></b>' \
#                 f'<ul></ul>' \
#                 f'</font><hr>'
#         if item.function.__doc__ is not None:
#             docstring = item.function.__doc__.split("*")
#             desc = "{}" \
#                    "<ul>{}</ul>".format(docstring[0], "".join("<li>{}</li>".format(i) for i in docstring[1:]))
#             title = title.replace("<ul></ul>", desc)
#         item.add_marker(allure.description_html(title))
#         item.add_marker(allure.feature('UI'))

def pytest_runtest_protocol(item, nextitem):
    # 1. Проставляем каждому тесту feature для отображения в allure-отчете
    if 'tests/ui' in str(item.path):
        item.add_marker(allure.epic('UI'))
    elif 'tests/api' in str(item.path):
        item.add_marker(allure.epic('API'))
    else:
        item.add_marker(allure.epic('UNKNOW'))

    item.add_marker(allure.feature('multiply'))