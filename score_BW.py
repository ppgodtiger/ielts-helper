from zhipuai import ZhipuAI
api_key = "248ed8a12c8bc4868d987029dea07085.autrJ6X3Vg84GM5y"  # 替换为你的API密钥
client = ZhipuAI(api_key=api_key)

def rate_essay(essay_content):
    """
    为雅思作文评分并给出改进方案。
    essay_content: 用户输入的雅思作文内容。
    API返回的评分结果和改进方案。
    """
    messages = [
        {
            "role": "user",
            "content": f"你是一个大作文的批改员，为以下大作文评分。若下文不是雅思作文为0;只用输出分数,不准输出其他数据：\n\n{essay_content}"
        }
    ]
    # 发送请求到API
    response = client.chat.completions.create(
        model="glm-4",
        messages=messages,
        top_p= 0.1,
        temperature= 0.95,
        max_tokens=200,
    )
    # 检查是否有响应
    if response.choices:
        # 返回第一个结果的完整消息内容
        return response.choices[0].message.content
    else:
        # 如果没有响应，返回错误信息
        return "No response received from the API."

