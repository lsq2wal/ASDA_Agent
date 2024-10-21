# src/code_programmer.py

from langchain_core.prompts import PromptTemplate

class CodeProgrammer:
    """
    代码生成器，负责根据工具选择器提供的工具，生成完成当前任务的代码。
    """
    def __init__(self, llm, data_file_path):
        self.llm = llm
        self.data_file_path = data_file_path
        # 定义代码生成器的系统提示
        self.prompt_template = """你是一名专业的生物信息学代码编写专家。
请根据以下信息，编写完成当前任务步骤的 Python 代码。

用户需求：
{user_requirements}

数据描述：
{data_description}

历史代码：
{historical_code}

当前任务步骤：
{step_description}

选定工具及其文档：
{tools_docs}

人类专家经验：
- 在预处理中，通常需要去除低质量的细胞和基因，并识别高变基因。
- 在批次效应校正中，可以使用 Harmony、Scanorama、scVI 等工具，选择最佳的结果。
- 在细胞类型注释中，可以使用多种方法，综合评估以获得最佳结果。

要求：
- 使用选定的工具完成任务。
- 代码应包括必要的导入和数据加载。
- 代码中应使用数据文件路径：{data_file_path}
- 请勿添加任何解释或注释，只需提供代码。
- 输出格式为代码块，使用 ```python 和 ``` 包裹。

"""

    def generate_code(self, step_description, user_requirements, data_description, global_memory, tools_docs, local_memory):
        prompt = PromptTemplate(
            input_variables=["user_requirements", "data_description", "historical_code", "step_description", "tools_docs", "data_file_path"],
            template=self.prompt_template
        )
        formatted_prompt = prompt.format(
            user_requirements=user_requirements,
            data_description=data_description,
            historical_code=global_memory.get_all_code(),
            step_description=step_description,
            tools_docs=tools_docs,
            data_file_path=self.data_file_path
        )

        # 使用 LLM 获取响应
        response = self.llm.invoke(formatted_prompt)
        code = self.extract_code(response)
        analysis = self.extract_analysis(response)
        return code, analysis

    def optimize_code(self, evaluation_feedback, local_memory):
        # 根据评估器的反馈和本地内存，优化代码
        # 实现自我迭代优化机制
        prompt_template = """你是一名专业的生物信息学代码编写专家。
请根据以下信息，优化之前编写的代码：

评估反馈：
{evaluation_feedback}

之前的尝试：
{previous_attempts}

请重新编写优化后的代码，输出格式为代码块，使用 ```python 和 ``` 包裹。
"""

        previous_attempts = "\n".join([f"尝试 {item['attempt']} 的代码：\n{item['code']}" for item in local_memory])

        prompt = PromptTemplate(
            input_variables=["evaluation_feedback", "previous_attempts"],
            template=prompt_template
        )
        formatted_prompt = prompt.format(
            evaluation_feedback=evaluation_feedback,
            previous_attempts=previous_attempts
        )

        # 使用 LLM 获取响应
        response = self.llm.invoke(formatted_prompt)
        code = self.extract_code(response)
        analysis = self.extract_analysis(response)
        return code, analysis

    def extract_code(self, response):
        start = response.find('```python')
        end = response.find('```', start + 9)
        if start != -1 and end != -1:
            return response[start+9:end].strip()
        else:
            return response.strip()

    def extract_analysis(self, response):
        # 如果有分析文本，可以在此提取
        return ""
