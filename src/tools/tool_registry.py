# src/tools/tool_registry.py

class ToolRegistry:
    """
    工具注册表，管理所有可用的工具。
    """
    def __init__(self):
        # 定义可用的工具及其描述
        self.tools = {
            "Scanpy": "An open-source toolkit for analyzing single-cell gene expression data.",
            "Harmony": "Integration of single-cell data using Harmony algorithm.",
            "Scanorama": "Batch correction and integration of single-cell data.",
            "CellTypist": "Automated cell type annotation for single-cell data.",
            "ScType": "A tool for cell type identification in single-cell RNA-seq data.",
            "CellPhoneDB": "Infers cell-cell communication networks from single-cell transcriptomics data.",
            "CellChat": "A tool for analyzing cell-cell communication.",
            "scVI": "Single-cell Variational Inference for scRNA-seq data.",
            "CellMarkerACT": "A tool for cell type annotation using CellMarker database."
        }

    def get_available_tools(self):
        return [{"name": name, "description": desc} for name, desc in self.tools.items()]

    def get_tools_docs(self, tool_names):
        # 返回选定工具的名称和描述
        return [{"name": name, "description": self.tools.get(name, "")} for name in tool_names]
