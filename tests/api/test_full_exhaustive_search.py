from api import calculator_api
import pytest
from helpers.decorators import Test


@Test('Тест поиска значений, которые при перемножении дают неверный результат.', story='exhaustive_search')
@pytest.mark.parametrize('a', [i for i in range(0, 100)])
@pytest.mark.parametrize('b', [i for i in range(0, 100)])
def test_exhaustive_search(a, b):
    r = calculator_api.multiply(a, b)
    r.should_has_body(a * b)

