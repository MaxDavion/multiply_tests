from waiting import wait, TimeoutExpired

def wait_until(predicate, timeout_seconds=10, sleep_seconds=0.5):
    """Дождаться пока переданная функция-предикат предикат не будет True или не истечет переданный таймаут.

    :param timeout: таймаут ожидания по истечении которого будет брошено исключение TimeoutExpired
    :param sleep_seconds: интервал выполнения функции (например: каждую 1 секунду)
    """
    try:
        wait(
            predicate=predicate,
            timeout_seconds=timeout_seconds,
            sleep_seconds=sleep_seconds,
        )
    except TimeoutExpired:
        return False