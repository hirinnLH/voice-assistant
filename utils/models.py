from transformers import pipeline
import os
os.environ["HF_MIRROR"] = "tuna"

# 加载意图识别和实体识别管道
_get_question_intent_pipe = pipeline("text-classification", model="qanastek/XLMRoberta-Alexa-Intents-Classification")
# Use a pipeline as a high-level helper
get_question_argument = pipeline("token-classification", model="cartesinus/slurp-slot_baseline-xlm_r-en")


def get_user_intent(user_query: str):
    return _get_question_intent_pipe(user_query)[0]['label']

