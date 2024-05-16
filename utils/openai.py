from typing import List

from openai import OpenAI
import json
from enum import Enum
from modules import get_method


class AIModel(Enum):
    GPT3Turbo = 'gpt-3.5-turbo'
    GPT4 = 'gpt-4'
    MOONSHOT = 'moonshot-v1-8k'


def getOpenAIClient():
    with open('manifest.json') as f:
        token = json.load(f)['moonshot']
    return OpenAI(
        api_key=token['api_key'],
        base_url=token['base_url']
    )


def get_response_from_openai(
        client,
        messages: List,
        model=AIModel.GPT3Turbo.value,
        tools=None,
        tool_choice='auto'):
    if tools is None:
        tools = []
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice=tool_choice
    )
    result = _form_api_result(client, messages, response)
    return result


def _form_api_result(client, messages, response):
    message = response.choices[0].message

    if message.tool_calls:
        function_name = message.tool_calls[0].function.name
        arguments = json.loads(message.tool_calls[0].function.arguments)
        function_result = get_method(function_name, arguments)
        messages.append({
            "role": "function",
            "name": function_name,
            "content": function_result,
        })
        function_response = _get_function_response_from_openai(client, messages)
        return function_response
    else:
        return message.content


def _get_function_response_from_openai(client,
                                       messages: List,
                                       model=AIModel.GPT3Turbo.value,):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    result = _form_api_result(client, messages, response)
    return result
