# Создайте исключение здесь
class LenTooLongError(Exception):
    pass


name = 'ЛилуминАй ЛекатАриба ЛаминачАй Экбат Дэ СэбАт'


def check_name(name):
    if len(name) > 4:
        raise LenTooLongError # Вызовите исключение здесь


check_name(name)