from xml.etree import ElementTree as ET
import allure
from helpers.log_helper import log
import json
from hashlib import md5


def to_curl(request, compressed=False):
    """Получить curl из объекта requests (библиотеки requests)"""
    parts = [
        ('curl', None),
        ('-X', request.method),
    ]

    for k, v in sorted(request.headers.items()):
        if k not in ['Accept-Encoding', 'Connection', 'Content-Length', 'User-Agent']:
            parts += [('-H', '{0}: {1}'.format(k, v))]

    if request.body:
        parts += [('-d', request.body)]

    if compressed:
        parts += [('--compressed', None)]

    parts += [(None, request.url)]

    flat_parts = []
    for k, v in parts:
        if k:
            flat_parts.append(k)
        if v:
            flat_parts.append("'{0}'".format(v))

    return ' '.join(flat_parts)


def api_method():
    """
    Декоратор для методов api.
    - Добавляет логгирование запросов к апи и ответов
    - Добавляет проверку `status_code ответа. По-умолчанию проверяется на status_codr==200, но можно переопределить через
    передачу в функции expected_code=<ожидаемый status_code>
    """
    def my_decorator(func):
        def wrapped(self, *args, **kwargs):
            __tracebackhide__ = True
            # Устанавливаем ожидаемые валидные значения status_code
            expected_code = kwargs.pop("expected_code", 200)

            r = func(self, *args, **kwargs)

            # Логируем запрос и ответ
            try:
                method_description = func.__doc__.lstrip().split('\n')[0]
            except AttributeError:
                raise RuntimeError("Api Method doesn't has 'docstring' description. "
                                   "You must write what the method does in the docstring,"
                                   "because the message in the log is formed based on "
                                   "the first line of this description")

            with allure.step(method_description):

                if 'json' in r.headers.get('content-type', ''):
                    response = json.dumps(r.json(), indent=4, sort_keys=True, ensure_ascii=False)
                elif 'xml' in r.headers.get('content-type', ''):
                    root = ET.fromstring(r.text)
                    response = ET.tostring(root, encoding='unicode')
                elif 'image' in r.headers.get('content-type', ''):
                    response = f"image hash '{md5(r.content).hexdigest()}'"
                else:
                    response = r.text


                allure.attach(
                    f'\n\t[Request] => {to_curl(r.request)}' +
                    f'\n\t[Response]<= status_code = {r.status_code}, reason = {r.reason} '
                    'body = {response}',
                    'request.log',
                    allure.attachment_type.TEXT
                )

                log.api.info(
                    method_description +
                    f'\n\t[Request] => {to_curl(r.request)}' +
                    f'\n\t[Response]<= '
                    f'status_code = {r.status_code}, '
                    f'reason = {r.reason}, '
                    f'duration={round(r.elapsed.total_seconds(), 2)}, '
                    f'body = {response}'
                )

            # Сверяем полученный status code с ожидаемым
            if r.status_code != expected_code:
                raise AssertionError(
                    f"Не удалось: {method_description}" +
                    f'\n\t[Error] Expected status code {expected_code} but was {r.status_code}' +
                    f'\n\t[Request] => {to_curl(r.request)}' +
                    f'\n\t[Response]<= status_code = {r.status_code}, reason = {r.json()}'
                )

            return r

        return wrapped

    return my_decorator



