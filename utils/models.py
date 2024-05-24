from enum import Enum

import json
import requests
from transformers import pipeline

# 加载意图识别和实体识别管道
# _get_question_intent_pipe = pipeline("text-classification", model="qanastek/XLMRoberta-Alexa-Intents-Classification")
# Use a pipeline as a high-level helper
# get_question_argument = pipeline("token-classification", model="cartesinus/slurp-slot_baseline-xlm_r-en")


# shibing624/mengzi-t5-base-chinese-correction


def _get_hugging_face_instance():
    with open('manifest.json') as f:
        token = json.load(f)['hugging-face']
    return {
        'intent_api_url': token['intent_api_url'],
        'slot_api_url': token['slot_api_url'],
        'correction_api_url': token['correction_api_url'],
        'header': {"Authorization": "Bearer " + token['token']}
    }


hugging_face_token = _get_hugging_face_instance()


class HuggingFaceModel(Enum):
    INTENT_MODEL = hugging_face_token['intent_api_url']
    SLOT_MODEL = hugging_face_token['slot_api_url']
    CORRECTION_MODEL = hugging_face_token['correction_api_url']


HUGGING_FACE_HEADER = hugging_face_token['header']


def _model_query(user_query: str, model: str):
    payload = {
        "inputs": user_query
    }
    response = requests.post(model, headers=HUGGING_FACE_HEADER, json=payload)
    return response.json()


def get_user_intent(user_query: str):
    # return _get_question_intent_pipe(user_query)[0]['label']
    return _model_query(user_query, HuggingFaceModel.INTENT_MODEL.value)


def get_intent_slot(user_query: str):
    return _model_query(user_query, HuggingFaceModel.SLOT_MODEL.value)


def get_user_intent_correction(user_query: str):
    return _model_query(user_query, HuggingFaceModel.CORRECTION_MODEL.value)

# output = query({
#     "inputs": "I like you. I love you",
# })
