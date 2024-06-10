from utils import get_intent_slot, get_user_intent
from modules import get_method
from responses import get_response


if __name__ == "__main__":
    query = '今天幾度'
    # user_intent_correction = get_user_intent_correction(query)
    user_intent = get_user_intent(query)
    intent_arguments = get_intent_slot(query)
    method_result = get_method(user_intent, intent_arguments)
    result = get_response(query, user_intent, method_result)
    # result = get_method("weather_query", [])
    print(result)
