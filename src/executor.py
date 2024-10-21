# src/executor.py

from src.tool_selector import ToolSelector
from src.code_programmer import CodeProgrammer

class Executor:
    """
    执行器类，负责执行每个子任务，包括工具选择和代码生成。
    """
    def __init__(self, llm, data_file_path, global_memory):
        self.llm = llm
        self.data_file_path = data_file_path
        self.global_memory = global_memory
        self.tool_selector = ToolSelector(llm)
        self.code_programmer = CodeProgrammer(llm, data_file_path)
