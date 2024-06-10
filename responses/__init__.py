from responses.basic_response import BasicResponse


def get_response(query, method_name, arguments=None):
    if arguments is None:
        arguments = {}
    if method_name == "datetime_query" and ("點" in query or "時間" in query):
        return BasicResponse.get("time_query")(arguments)
    elif method_name == "datetime_query" and ("日期" in query or "號" in query):
        return BasicResponse.get("date_query")(arguments)
    elif method_name == "weather_query":
        # arguments = [argument.get("word") for argument in arguments if argument.get("entity") == "B-place_name"]
        return BasicResponse.get("weather_query")(arguments)
    else:
        return f"没有找到函数{method_name}"
