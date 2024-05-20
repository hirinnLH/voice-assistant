# Use a pipeline as a high-level helper
# Use a pipeline as a high-level helper
from transformers import pipeline

# 加载文本生成pipeline
text_generator = pipeline('text-generation', model='bert-base-uncased')

if __name__ == "__main__":
    user_input = "現在幾點了？11：43"
    # 输入文本
    # input_text = "Hello, how are you?"

    # 生成回复
    generated_text = text_generator(user_input, max_length=50)

    print(generated_text)