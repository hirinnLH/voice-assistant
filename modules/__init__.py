from modules.basic_module import BasicFunction


def get_method(method_name, arguments=None):
    if arguments is None:
        arguments = []
    if method_name == 'datetime_query':
        return BasicFunction.get('datetime_query')()
    elif method_name == 'weather_query':
        arguments = [argument.get('word') for argument in arguments if argument.get('entity') == 'B-place_name']
        return BasicFunction.get('weather_query')(arguments)
    else:
        return f"没有找到函数{method_name}"


# class MethodFactory:
#     pass


__all__ = ['get_method']
