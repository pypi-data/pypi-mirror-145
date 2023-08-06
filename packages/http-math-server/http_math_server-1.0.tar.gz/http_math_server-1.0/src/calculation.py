import operator 
import math


FUNCTIONS = {
    operator: {
        'add',
        'sub',
        'mul',
        'truediv',
        'mod',
    },

    math: {
        'copysign',
        'fmod',
        'ldexp',
        'pow',
    }
}


def calculate(data: str) -> dict:
    splited_data = data.split()
    try:
        func_name, num1, num2 = splited_data
    except ValueError as ex:
        return f"{type(ex).__name__}: {ex}"
    try:
        num1, num2 = float(num1), float(num2)
    except ValueError as ex:
        return f"{type(ex).__name__}: {ex}"

    try:
        for pkg, funcs in FUNCTIONS.items():
            if func_name in funcs:
                try:
                    result = operator.methodcaller(func_name, num1, num2)(pkg)
                except ZeroDivisionError as ex:
                    return f"{type(ex).__name__}: {ex}"
                return {
                    'operator': func_name,
                    'num1': num1,
                    'num2': num2,
                    'result': str(result)
                }

        # If function isn't found
        raise AttributeError("No such function.")
    except AttributeError as ex:
        return f"{type(ex).__name__}: {ex}"
