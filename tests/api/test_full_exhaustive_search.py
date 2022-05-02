from api import calculator_api
import pytest


@pytest.mark.parametrize('a', [i for i in range(0, 10)])
@pytest.mark.parametrize('b', [i for i in range(0, 10)])
def test_exhaustive_search(a, b):
    """Тест поиска значений, которые при перемножении дают неверный результат."""
    r = calculator_api.multiply(a, b)
    assert int(r.text) == a * b

