import environment
import os


def pytest_addoption(parser):
    parser.addoption("--BASE_URL", action="store", default='http://13.49.131.32')
    parser.addoption("--ALLURE", action="store_true", default=False,)


def pytest_configure(config):
    """Хук pytest'а: выполняется самым первым."""
    # 1. Загружаем и сохраняем в глобальную переменную ENVIRONMENT, все настройки целевой среды
    environment.set_environment(
        BASE_URL=config.getoption("--BASE_URL")
    )

    if config.getoption("--ALLURE", None):
        config.option.allure_report_dir = os.path.join(environment.get_logs_folder(), f'allure-results')