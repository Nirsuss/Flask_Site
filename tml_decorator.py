from functools import wraps


def decorator_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 1 Код для выполнения перед вызвом декорируем  фунцией.
        # 2 Вызов декорируем функции и возврат полученных результатов.
        return func(*args, **kwargs)

    # 3 Код для выполнения вместо вызова декорируем функции
    return wrapper()
