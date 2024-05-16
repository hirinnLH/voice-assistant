from modules.basic_module import BasicFunction


def get_method(method_name, arguments):
    if method_name == 'get_current_time':
        return BasicFunction.get('get_current_time')()
    else:
        return f"没有找到函数{method_name}"


# class MethodFactory:
#     pass


__all__ = ['get_method']
