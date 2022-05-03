import requests
import allure


class ApiRequest:
    """ Набор staticmethod для работы с requests
    * Вместо стандартного объекта Response возвращают его же но обернутым во враппер 'SResponse'
    """

    @staticmethod
    def request(method, url, verify=False, **kwargs):
        return ApiResponse(requests.request(method, url, verify=verify, **kwargs))

    @staticmethod
    def get(url, params=None, verify=False, **kwargs):
        return ApiResponse(requests.get(url, params, verify=verify, **kwargs))

    @staticmethod
    def post(url, data=None, verify=False, json=None, **kwargs):
        return ApiResponse(requests.post(url, data, json, verify=verify, **kwargs))

    @staticmethod
    def delete(url, verify=False, **kwargs):
        return ApiResponse(requests.delete(url, verify=verify, **kwargs))

    @staticmethod
    def update(url, data=None, verify=False, **kwargs):
        return ApiResponse(requests.patch(url, data, verify=verify, **kwargs))

    @staticmethod
    def put(url, data=None, verify=False, **kwargs):
        return ApiResponse(requests.put(url, data, verify=verify, **kwargs))

    @staticmethod
    def prepare_request(prepared_request):
        return ApiResponse(requests.Session().send(prepared_request))

    @staticmethod
    def patch(url, data=None, verify=False, json=None, **kwargs):
        return ApiResponse(requests.patch(url, data, json=json, verify=verify, **kwargs))


class ApiResponse(requests.Response):
    """ Класс-wrapper: обёртывает объект 'Response', библиотеки requests
    * Позволяет расширять её своими методами и свойствами
    * Поддерживает все методы и свойства оригинального объекта (в.т.ч. их перегрузку)
    """
    def __init__(self, origin_responce):
        super(ApiResponse, self).__init__()
        for k, v in origin_responce.__dict__.items():
            self.__dict__[k] = v

    @allure.step('Проверить что сервис вернул "{body}"')
    def should_has_body(self, body):
        assert self.text == str(body), f'Ожидаемый результат "{body}". Полученный результат: "{self.text}"'