from transformers import pipeline

# 加载意图识别和实体识别管道
_get_question_intent_pipe = pipeline("text-classification", model="qanastek/XLMRoberta-Alexa-Intents-Classification")
# Use a pipeline as a high-level helper
get_question_argument = pipeline("token-classification", model="cartesinus/slurp-slot_baseline-xlm_r-en")


def get_user_intent(user_query: str):
    return _get_question_intent_pipe(user_query)[0]['label']
    # return _model_query(user_query, HuggingFaceModel.INTENT_MODEL.value)


def get_intent_slot(user_query: str):
    return get_question_argument(user_query)
    # return _model_query(user_query, HuggingFaceModel.SLOT_MODEL.value)


# def get_user_intent_correction(user_query: str):
#     return _model_query(user_query, HuggingFaceModel.CORRECTION_MODEL.value)

# output = query({
#     "inputs": "I like you. I love you",
# })
