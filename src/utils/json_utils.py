# src/utils/json_utils.py

import json

def extract_and_parse_json(response):
    """从 LLM 响应中提取并解析 JSON"""
    try:
        # 尝试找到 JSON 的起始和结束位置
        start = response.index('{')
        end = response.rindex('}')
        json_str = response[start:end+1]
        
        # 解析 JSON 字符串
        return json.loads(json_str)
    except ValueError as e:
        print(f"未能找到有效的 JSON 部分: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {str(e)}")
    return None
