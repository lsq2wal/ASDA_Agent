# src/memory.py

class GlobalMemory:
    """
    全局内存，存储每个历史步骤的最终代码。
    """
    def __init__(self):
        self.codes = []

    def add_code(self, code):
        self.codes.append(code)

    def get_all_code(self):
        return "\n".join(self.codes)
