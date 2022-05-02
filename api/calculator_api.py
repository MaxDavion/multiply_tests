import requests
import environment
from ._base import api_method


@api_method()
def multiply(a, b):
    """Перемножить два числа"""
    url = f"{environment.get_environment('BASE_URL')}:8080"
    payload = f"first={a}&second={b}"
    return requests.post(url=url, data=payload, timeout=30)

