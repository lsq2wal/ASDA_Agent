#src/code_sandbox.py

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os
from datetime import datetime

class CodeSandbox:
    """
    代码沙箱，使用 Jupyter Notebook 来执行代码。
    """
    def __init__(self, notebook_path):
        """
        初始化沙箱，指定要保存的 Notebook 路径。
        
        :param notebook_path: Notebook 文件的保存路径
        """
        self.notebook_path = notebook_path
        self.nb = nbformat.v4.new_notebook()
        self.nb['cells'] = []

    def add_code_cell(self, code):
        """
        添加代码单元格到 Notebook。
        
        :param code: 要执行的代码
        """
        cell = nbformat.v4.new_code_cell(code)
        self.nb['cells'].append(cell)

    def _generate_unique_filename(self, base_path):
        """
        生成唯一的文件名，如果文件存在则在文件名后添加时间戳或递增编号。
        
        :param base_path: 基础文件路径
        :return: 不重名的文件路径
        """
        if not os.path.exists(base_path):
            return base_path
        else:
            # 添加时间戳避免重名
            base, ext = os.path.splitext(base_path)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            return f"{base}_{timestamp}{ext}"

    def execute_notebook(self):
        """
        执行 Notebook 并保存结果。
        
        :return: 执行结果信息，成功或错误信息
        """
        try:
            # 获取 Notebook 保存的目录路径
            notebook_dir = os.path.dirname(self.notebook_path)
            if not os.path.exists(notebook_dir):
                os.makedirs(notebook_dir)

            # 检查是否有重名文件，生成唯一文件名
            unique_notebook_path = self._generate_unique_filename(self.notebook_path)

            # ExecutePreprocessor 设置
            ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

            # 设置工作目录为 Notebook 所在目录
            execute_path = {'metadata': {'path': notebook_dir if notebook_dir else './'}}

            # 执行 Notebook
            print(f"正在执行 Notebook: {unique_notebook_path}")
            ep.preprocess(self.nb, execute_path)

            # 保存执行后的 Notebook
            with open(unique_notebook_path, 'w', encoding='utf-8') as f:
                nbformat.write(self.nb, f)

            print(f"Notebook 已成功保存到: {unique_notebook_path}")
            return f"执行成功，保存为: {unique_notebook_path}"

        except Exception as e:
            error_message = f"执行出错：{str(e)}"
            print(error_message)
            return error_message
