# main.py

from src.planner import Planner
from src.executor import Executor
from src.evaluator import Evaluator
from src.memory import GlobalMemory
from src.code_sandbox import CodeSandbox
from langchain_community.llms import Ollama

# # 初始化openAI的API
# from langchain_openai import ChatOpenAI
# import getpass
# import os

# os.environ["OPENAI_API_KEY"] = getpass.getpass()


# from fastapi import FastAPI  
# from langserve import add_routes

# from langchain.memory import ConversationBufferMemory

def main():
    """
    运行基于 LLM 的多代理框架的主函数。
    """
    # 初始化本地 LLM
    llm = Ollama(model='llama3.1', base_url='http://localhost:11434')

    # 初始化 OpenAI LLM
    # llm = ChatOpenAI(model_name='gpt-4', temperature=0)

    # 初始化全局内存
    global_memory = GlobalMemory()

    # 初始化代码沙箱
    code_sandbox = CodeSandbox(notebook_path='/home/share/huadjyin/home/liushiqiang/CellAgent/examples/notebooks/analysis.ipynb')


    # 在接收用户任务时，要求提供数据文件路径
    print("欢迎使用自动化 scRNA-Seq 数据分析框架。")
    user_task = input("请输入您的 scRNA-seq 分析任务：\n")
    data_file_path = input("请输入您的 scRNA-seq 数据文件路径：\n")

    # 检查数据文件是否存在
    import os
    if not os.path.exists(data_file_path):
        print(f"数据文件 {data_file_path} 不存在。请检查路径。")
        return

    # 读取数据，获取数据的字符串表示 ψ(D)
    import scanpy as sc
    adata = sc.read_h5ad(data_file_path)
    data_representation = str(adata)
    print(data_representation)

    # 初始化规划器
    planner = Planner(llm, data_representation)
    # 初始化执行器和评估器
    executor = Executor(llm, data_file_path, global_memory)
    evaluator = Evaluator(llm)
    
    # # 初始化内存
    # memory = ConversationBufferMemory()
    # 初始化code文件保存路径
    # save_path = '/home/share/huadjyin/home/liushiqiang/CellAgent/examples/cases1.1/code'

    # 使用规划器将任务分解为步骤
    print("\n正在规划任务...")
    steps = planner.plan(user_task)
    print("\n生成的计划：")

    for idx, step in enumerate(steps, 1):
        print(f"步骤 {idx}：{step['description']}")
    
    # 执行并评估每个步骤
    for i, step in enumerate(steps, 1):
        print(f"\n---\n正在执行步骤 {i}：{step['description']}\n")

        # 初始化本地内存
        local_memory = []

        # 自我迭代优化
        success = False
        attempt = 0
        max_attempts = 2  # 根据不同步骤设置不同的最大尝试次数
        if "批次效应校正" in step['description']:
            max_attempts = 3  # 批次效应校正默认尝试三次

        while not success and attempt < max_attempts:
            attempt += 1
            print(f"尝试第 {attempt} 次...")

            # 工具选择器选择工具
            tools = executor.tool_selector.select_tools(step['description'], user_task)

            # 代码生成器生成代码
            code, analysis = executor.code_programmer.generate_code(
                step_description=step['description'],
                user_requirements=user_task,
                data_description=data_representation,
                global_memory=global_memory,
                tools_docs=tools,
                local_memory=local_memory
            )

            # 将代码添加到本地内存
            local_memory.append({
                'attempt': attempt,
                'code': code,
                'analysis': analysis
            })

            # 将代码添加到全局内存
            global_memory.add_code(code)

            # 将代码添加到代码沙箱（Jupyter Notebook）
            code_sandbox.add_code_cell(code)

            # 执行代码沙箱，捕获执行结果或异常
            execution_result = code_sandbox.execute_notebook()

            # 评估器评估执行结果
            evaluation = evaluator.evaluate(
                code=code,
                execution_result=execution_result,
                step_description=step['description'],
                user_requirements=user_task,
                data_description=data_representation
            )

            # 判断结果是否满意
            if evaluator.is_result_satisfactory(evaluation):
                print("步骤执行成功。")
                success = True
            else:
                print("步骤执行未通过评估，需要优化。")
                # 如果未达到最大尝试次数，提示代码生成器优化
                if attempt < max_attempts:
                    executor.code_programmer.optimize_code(
                        evaluation_feedback=evaluation,
                        local_memory=local_memory
                    )
                else:
                    print("已达到最大尝试次数，跳过此步骤。")
            print(local_memory)

        # 在步骤完成后，重置本地内存
        local_memory = []

    # 最终结果生成
    print("\n所有步骤已完成，正在生成最终结果...")
    final_result = planner.generate_final_result()
    print("最终结果已保存至 ./examples/notebooks/analysis.ipynb")
    print("您可以打开该 Notebook 查看完整的分析流程和结果。")
            

if __name__ == '__main__':
    main()
