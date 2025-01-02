def just_plus(first, second):
    # Ожидаются параметры одинакового типа.
    # В ином случае должна выбрасываться ошибка.
    try:
        print(first + second)
    except TypeError:
        print('В функцию just_plus() переданы параметры, которые невозможно сложить или конкатенировать!')

        
first = 5
second = 10
just_plus(first, second)