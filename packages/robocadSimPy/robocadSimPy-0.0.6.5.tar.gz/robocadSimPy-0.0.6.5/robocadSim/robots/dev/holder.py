LOG_ALL: int = 0  # печатает все
LOG_EXC_INFO: int = 1  # все, кроме простой информации
LOG_EXC_WARN: int = 2  # все, кроме предупреждений
LOG_NOTHING: int = 3  # ничего

LOG_LEVEL: int = LOG_EXC_INFO


class ConnectionResetWarning(Warning):
    pass
