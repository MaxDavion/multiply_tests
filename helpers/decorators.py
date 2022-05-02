# -*- coding: utf-8 -*-
from functools import wraps
import inspect
import re
import types
from allure_commons import _allure
from allure_commons.types import LabelType
from _pytest.mark import MarkDecorator, Mark
import allure


Step = _allure.step
Given = _allure.step
Check = _allure.step


def Test(severity=None):
    """ Декоратор на тест
    :param severity: критичность теста (trivial, minor, normal, critical, blocker)
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            # Вытаскиваем название теста и его описание из докстринга тестовой функции
            if func.__doc__ is not None:
                # строки состоящие только из пробелов не включаем
                # удаляем пробелы в начале и конце строки
                docstring_list = [string.strip() for string in func.__doc__.split('\n')
                                  if string.isspace() is not True and len(string) > 0]

                title = docstring_list[0]
                description = "<hr><font color=45B2C9>" \
                              "<b>{}</b>" \
                              "<ul>{}</ul>" \
                              "</font><hr>".format(docstring_list[0],
                                                   "".join("<li>{}</li>".format(i) for i in docstring_list[1:]))

                _allure.Dynamic.title(title)
                _allure.Dynamic.description_html(description)

            else:
                # если у тестовой функции по нет докстринга, то название теста будет само название функции
                _allure.Dynamic.title(func.__name__)

            if severity:
                _allure.Dynamic.severity(severity)

            return func(*args, **kwargs)
        return wrapper
    return decorator
