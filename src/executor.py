# executor.py


from langchain.prompts import PromptTemplate

class Executor:
    """
    执行器类，负责为每个任务步骤生成代码。
    """
    def __init__(self, llm, data_file_path):
        # 初始化大型语言模型
        self.llm = llm
        self.data_file_path = data_file_path
        # 定义用于代码生成的提示模板
        self.prompt_template = """你是一名专门从事 scRNA-seq 数据分析的高级编码助手。
请使用 Python 代码来执行以下任务：
任务：{task}

要求：
- 使用适当的库（如 Scanpy、Anndata 等）。
- 确保代码中正确地加载了数据文件：{data_file_path}。
- 提供完整的、可运行的代码，包括必要的导入和数据加载。
- 请勿添加任何解释或注释，只需提供代码。

代码格式：
```python
[您的代码]
"""
            
    def execute(self, task):
        """
        为给定的任务生成代码。
        """
        # 使用任务和数据文件路径格式化提示
        prompt = PromptTemplate(input_variables=["task", "data_file_path"], template=self.prompt_template)
        formatted_prompt = prompt.format(task=task, data_file_path=self.data_file_path)
        # 使用 LLM 生成代码
        response = self.llm.invoke(formatted_prompt)
        code = self.extract_code(response)
        return code

    def extract_code(self, response):
        """
        从 LLM 的响应中提取代码。
        """
        # 提取 ```python 和 ``` 之间的代码
        start = response.find('```python')
        end = response.find('```', start + 9)
        if start != -1 and end != -1:
            return response[start+9:end].strip()
        else:
            return response.strip()
