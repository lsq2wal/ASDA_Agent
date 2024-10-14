# main.py

from src.planner import Planner
from src.executor import Executor
from src.evaluator import Evaluator
from langchain_community.llms import Ollama

# from fastapi import FastAPI  
# from langserve import add_routes

# from langchain.memory import ConversationBufferMemory

def main():
    """
    运行基于 LLM 的多代理框架的主函数。
    """
    # 初始化本地 LLM
    llm = Ollama(model='llama3.1', base_url='http://localhost:11434')

    # 初始化规划器
    planner = Planner(llm)

    # 在接收用户任务时，要求提供数据文件路径
    print("欢迎使用自动化 scRNA-Seq 数据分析框架。")
    user_task = input("请输入您的 scRNA-seq 分析任务：\n")
    data_file_path = input("请输入您的 scRNA-seq 数据文件路径：\n")

    # 初始化执行器和评估器
    executor = Executor(llm, data_file_path)
    evaluator = Evaluator(llm)
    
    # # 初始化内存
    # memory = ConversationBufferMemory()
    # 初始化code文件保存路径
    save_path = '/home/share/huadjyin/home/liushiqiang/CellAgent/examples/cases1.1/code'

    # 使用规划器将任务分解为步骤
    print("\n正在规划任务...")
    steps = planner.plan(user_task)
    print("\n生成的计划：")

    for idx, step in enumerate(steps, 1):
        print(f"步骤 {idx}：{step}")
    
    # 执行并评估每个步骤
    for i, step in enumerate(steps, 1):
        print(f"\n---\n正在执行步骤 {i}：{step}\n")
        # 使用执行器为步骤生成代码
        code = executor.execute(step)
        print("生成的代码：\n")
        print(code)
        
        # 将代码保存到文件
        code_filename = f'{save_path}/step_{i}_code.py'
        with open(code_filename, 'w') as f:
            f.write(code)
        print(f"\n代码已保存到 {code_filename}")
        
        # 使用评估器评估代码
        print("\n正在评估代码...")
        evaluation = evaluator.evaluate(code)
        print("评估结果：\n")
        print(evaluation)
        
        # 决定是否继续或请求改进代码
        if "未发现问题" in evaluation or "看起来不错" in evaluation:
            print("继续进行下一步。")
        else:
            print("根据评估，代码需要改进。")
            

if __name__ == '__main__':
    main()
