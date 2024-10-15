# src/planner.py


from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re

class Planner:
    """
    规划器类，负责将用户的主要任务分解为可执行的步骤。
    """
    def __init__(self, llm):
        # 初始化大型语言模型
        self.llm = llm
        self.parser = StrOutputParser()
        # 定义用于规划的提示模板
        self.prompt_template = """你是一名专门从事生物信息学的规划助手。
请将以下 scRNA-seq 数据分析任务分解为可执行的步骤。
请按照以下格式输出：
1. [步骤一]
2. [步骤二]
...

任务：{task}

必须遵守的要求：1、请注意，每个步骤前都有数字和句点，每个步骤占一行 2、每个步骤必须包含一个具体的任务，不能只包含一个概念或概括。

"""
            
    def plan(self, task):
        """
        生成计划，将任务分解为步骤。
        """
        # 使用用户的任务格式化提示
        prompt_planner = PromptTemplate(input_variables=["task"], template=self.prompt_template)
        
        # 使用 LLM 获取响应
        chain = prompt_planner | self.llm | self.parser

        # 从响应中解析步骤
        response = chain.invoke({"task":task})
        print(response)
        steps = self.parse_steps(response)

        return steps

    def parse_steps(self, response):
        """
        从 LLM 的响应中解析编号的步骤。
        """
        steps = []
        # 使用正则表达式匹配数字和句点开头的行
        lines = response.strip().split('\n')
        for line in lines:
            match = re.match(r'^\s*\d+\.\s*(.*)', line)
            if match:
                step = match.group(1).strip()
                steps.append(step)
        return steps

