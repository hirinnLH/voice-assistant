from utils import get_intent_slot, get_user_intent_correction, get_user_intent
from modules import get_method


if __name__ == "__main__":
    query = '今天氣溫幾度'
    user_intent_correction = get_user_intent_correction(query)
    user_intent = get_user_intent(query)
    intent_arguments = get_intent_slot(query)
    result = get_method(user_intent, intent_arguments)
    print(result)
