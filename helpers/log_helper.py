import os
from datetime import *
import sys
import loguru
import environment


def get_logfile(logfile_prefix, folder=None):
    """ Получить путь и название файла, куда писать лог
    :param logfile_prefix: префикс лог-файлов
    :param folder: название подпапки в директории `logs`, в которую будут сохраняться лог-файлы (если не задан,
    то логи будут сохраняться в саму папку `logs`).
    :return: str, название лог-файла сгенеренное по шаблону {logfile_prefix}{текущая дата и время}
    (пример: my_prefix_01Mar-11:34:03.txt)
    """
    # Если название папки передано без завершающего слэша, то добавляем его, что бы воспринималось как папка
    if folder is not None and not folder.endswith('/'):
        folder = f"{folder}/"

    log_folder = environment.get_logs_folder()
    return os.path.join(log_folder, folder, f"{logfile_prefix}_{datetime.now().strftime('%d%b-%H:%M:%S')}.txt")


class Log:

    _DEFAULT_LOG_LEVEL = "INFO"
    _DEFAULT_LOG_NAMESPACES = "api, test"
    _DEFAULT_LOG_FORMAT = "<green> {time:YYYY-MM-DD HH:mm:ss} </green> " \
                          "| <level> {level} </level> " \
                          "| <fg 148,0,211> {extra[namespace]} </fg 148,0,211> " \
                          "| <level> {module} </level> | <level> {message} </level>"

    __logger = None

    def __setup_logger_if_it_not_exist(self):
        """Сконфигурировать логгирование"""
        if not self.__logger:
            self.__logger = loguru.logger
            self.__logger.remove()  # Удаляем предустановленный логгер

            # Подгружаем переопределение дефолтных настроек логгирования пользовательскими
            env = environment.get_environment()
            level = env.get('LOG_LEVEL', self._DEFAULT_LOG_LEVEL).upper()
            namespaces = env.get('LOG_NAMESPACES', self._DEFAULT_LOG_NAMESPACES).split(', ')
            format = env.get('LOG_FORMAT', self._DEFAULT_LOG_FORMAT)

            # Добавляем вывод логов в консоль
            self.__logger.add(
                sys.stdout,
                format=format,
                colorize=True,
                level=level,
                filter=lambda record: record["extra"].get("namespace") in namespaces
            )
            # Добавляем вывод логов в файл
            self.__logger.add(
                get_logfile(logfile_prefix='test_run', folder='tests/'),
                format=format,
                colorize=False,
                level=level,
                filter=lambda record: record["extra"].get("namespace") in namespaces
            )

    @property
    def api(self):
        self.__setup_logger_if_it_not_exist()
        return loguru.logger.bind(namespace="api")

    @property
    def test(self):
        self.__setup_logger_if_it_not_exist()
        return loguru.logger.bind(namespace="test")

log = Log()
