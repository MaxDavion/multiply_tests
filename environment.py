import os

ENVIRONMENT = None


def set_environment(**kwargs):
    """ Установить конфигурацию на которой работать
    :param args:
    :return: dict,
    """
    global ENVIRONMENT
    if ENVIRONMENT == None:
        ENVIRONMENT = {}
        ENVIRONMENT.update(kwargs)


def get_environment(key=None):
    global ENVIRONMENT
    return ENVIRONMENT if key is None else ENVIRONMENT[key]


def get_logs_folder():
    root_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'logs')
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)
    return root_folder

