# evaluator.py

from langchain.prompts import PromptTemplate

class Evaluator:
    """
    评估器类，评估生成代码的质量。
    """
    def __init__(self, llm):
        # 初始化大型语言模型
        self.llm = llm
        # 定义用于评估的提示模板
        self.prompt_template = """你是一名经验丰富的代码审查员。
请评估以下 Python 代码的正确性、效率和对最佳实践的遵循。
请按照以下格式输出：

评估结果：
[您的评估]

改进建议：
[您的建议]

代码：
```python
{code}
"""
            
    def evaluate(self, code):
        """
        评估给定的代码。
        """
        # 使用代码格式化提示
        prompt = PromptTemplate(input_variables=["code"], template=self.prompt_template)
        formatted_prompt = prompt.format(code=code)
        # 使用 LLM 评估代码
        response = self.llm.invoke(formatted_prompt)
        return response.strip()
