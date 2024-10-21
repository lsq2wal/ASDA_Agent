# src/evaluator.py

from langchain.prompts import PromptTemplate

class Evaluator:
    """
    评估器类，评估生成代码和执行结果的质量。
    """
    def __init__(self, llm):
        self.llm = llm
        # 定义评估器的系统提示
        self.prompt_template = """你是一名经验丰富的生物信息学专家。
请根据以下信息，评估代码执行结果的正确性和合理性，并给出改进建议。

用户需求：
{user_requirements}

数据描述：
{data_description}

当前任务步骤：
{step_description}

代码执行结果：
{execution_result}

请按照以下格式输出：

评估结果：
[您的评估]

改进建议：
[您的建议]

请勿包含其他内容。
"""

    def evaluate(self, code, execution_result, step_description, user_requirements, data_description):
        prompt = PromptTemplate(
            input_variables=["user_requirements", "data_description", "step_description", "execution_result"],
            template=self.prompt_template
        )
        formatted_prompt = prompt.format(
            user_requirements=user_requirements,
            data_description=data_description,
            step_description=step_description,
            execution_result=execution_result
        )

        # 使用 LLM 获取响应
        response = self.llm.invoke(formatted_prompt)
        return response.strip()

    def is_result_satisfactory(self, evaluation):
        """
        根据评估结果，判断是否需要改进。
        """
        if '改进建议' in evaluation and ('无' in evaluation or '暂无' in evaluation):
            return True
        else:
            return False
