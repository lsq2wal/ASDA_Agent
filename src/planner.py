# src/planner.py

from langchain_core.prompts import PromptTemplate
from src.utils.json_utils import extract_and_parse_json

class Planner:
    """
    规划器类，负责将用户的主要任务分解为可执行的步骤。
    """
    def __init__(self, llm, data_representation):
        self.llm = llm
        self.data_representation = data_representation
        # 定义用于规划的提示模板
        self.prompt_template = """你是一名专门从事生物信息学的规划助手。
请根据以下信息，为用户的 scRNA-seq 数据分析任务生成详细的任务规划。
输出格式为 JSON，以便于后续子任务的提取。

用户任务描述：
{user_task}

用户数据描述：
{data_representation}

输出格式要求：
{{
  "steps": [
    {{
      "id": 1,
      "description": "步骤一描述"
    }},
    {{
      "id": 2,
      "description": "步骤二描述"
    }},
    ...
  ]
}}

请确保输出的 JSON 格式正确，且包含所有必要的步骤。
"""

    def plan(self, user_task):
        prompt = PromptTemplate(
            input_variables=["user_task", "data_representation"],
            template=self.prompt_template
        )
        formatted_prompt = prompt.format(
            user_task=user_task,
            data_representation=self.data_representation
        )

        # 使用 LLM 获取响应
        response = self.llm.invoke(formatted_prompt)
        print(response)

        # 尝试提取 JSON 并解析
        parsed_json = extract_and_parse_json(response)
        # 解析 JSON 响应
        if parsed_json:
            steps = parsed_json.get('steps', [])
            return steps
        else:
            print("规划器生成的 JSON 无法解析，请检查提示模板或 LLM 输出。")
            return []

    def generate_final_result(self):
        """
        生成最终结果，可能包括结果汇总、可视化等。
        """
        # 由于所有步骤的代码和结果都已在 Jupyter Notebook 中
        # 因此可以直接将 Notebook 作为最终结果
        pass
