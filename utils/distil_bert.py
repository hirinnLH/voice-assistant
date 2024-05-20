from transformers import pipeline
from modules import get_method

# 加载意图识别和实体识别管道
nlp = pipeline("text-classification", model="qanastek/XLMRoberta-Alexa-Intents-Classification")
# Use a pipeline as a high-level helper
pipe = pipeline("token-classification", model="cartesinus/slurp-slot_baseline-xlm_r-en")

if __name__ == "__main__":
    # 示例用户输入
    user_input = "上海今天幾度？"

    # 使用模型进行意图和实体识别
    intent_classify = nlp(user_input)
    token_getter = pipe(user_input)

    # 从识别结果中提取意图和实体
    intent = intent_classify[0]['label']

    # 调用本地函数并传递参数
    print(get_method(intent, token_getter))
