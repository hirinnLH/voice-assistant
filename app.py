from utils import get_open_ai_client, get_response_from_openai

client = get_open_ai_client()

tools = [
    {
        "type": "function",
        "function": {"name": "get_current_time",
                     "description": "To get the current time from system time",
                     },
        "parameters": {}
    }
]


def test_model(model):
    history = [
        {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"}
    ]

    def chat(query, history):
        history.append({
            "role": "user",
            "content": query
        })
        completion = client.chat.completions.create(
            model=model,
            messages=history,
            temperature=0.3,
        )
        result = completion.choices[0].message.content
        history.append({
            "role": "assistant",
            "content": result
        })
        return result

    print(chat("地球的自转周期是多少？", history))
    print(chat("月球呢？", history))


if __name__ == "__main__":
    # test_model("moonshot-v1-8k")
    query = '地球的自转周期是多少'
    messages = [
        # {'role': 'system',
        #  'content': '你是一个優秀的語音助手，你可以藉助自己的知識或用戶給的function幫助用戶得到他想要的答案。'},
        {'role': 'user', 'content': query},
    ]
    result = get_response_from_openai(client=client, messages=messages, tools=tools, model='moonshot-v1-8k')
    print(result)
