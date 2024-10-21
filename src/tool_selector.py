# src/tool_selector.py

from langchain_core.prompts import PromptTemplate
import json
from src.tools.tool_registry import ToolRegistry
from src.utils.json_utils import extract_and_parse_json

class ToolSelector:
    """
    工具选择器，负责为当前任务步骤选择合适的工具。
    """
    def __init__(self, llm):
        self.llm = llm
        self.tool_registry = ToolRegistry()
        # 定义工具选择器的系统提示
        self.prompt_template = """你是一名专业的生物信息学工具选择专家。
请根据用户的需求和当前任务步骤，从可用的工具列表中选择最合适的工具。
输出格式为 JSON。

用户需求：
{user_requirements}

当前任务步骤：
{step_description}

可用工具列表：
{available_tools}

输出格式要求：
{{
  "selected_tools": ["工具1", "工具2", ...]
}}

要求：
1、请确保输出的 JSON 格式必须正确，方便提取。
2、请确保选择的工具在可用工具列表中。
3、请确保selected_tools 是一个列表，包含了所选工具的名称。
"""

    def select_tools(self, step_description, user_requirements):
        prompt = PromptTemplate(
            input_variables=["user_requirements", "step_description", "available_tools"],
            template=self.prompt_template
        )
        formatted_prompt = prompt.format(
            user_requirements=user_requirements,
            step_description=step_description,
            available_tools=json.dumps(self.tool_registry.get_available_tools(), ensure_ascii=False)
        )

        # 使用 LLM 获取响应
        response = self.llm.invoke(formatted_prompt)

        print(response)

        # 解析 JSON 响应
        parsed_json = extract_and_parse_json(response)

        print(parsed_json)

        if parsed_json:
            selected_tools = parsed_json.get('selected_tools', [])
            # 获取工具的文档
            tools_docs = self.tool_registry.get_tools_docs(selected_tools)
            return tools_docs
        else:
            print("工具选择器生成的 JSON 无法解析，请检查提示模板或 LLM 输出。")
            return []

