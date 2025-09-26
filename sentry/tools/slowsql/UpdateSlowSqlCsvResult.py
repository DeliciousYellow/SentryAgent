import pandas as pd
import json
from pathlib import Path
from typing import Optional
from langchain_core.tools import Tool


def update_slow_sql_csv_result(input_json: str) -> str:
    """
    更新慢SQL审批CSV文件，将分析结果写入对应行的下一列
    不修改原文件，而是生成一个新的修改后的CSV文件
    
    Args:
        input_json: JSON字符串，包含以下字段：
        {
            "sql_hash": "慢SQL的hash值",
            "result_type": "ddl" | "mr" | "ai_analysis",  # 结果类型
            "result_content": "DDL语句 | MR链接 | AI分析输出",
            "ai_decision": "可选：AI决策的完整JSON" # 仅当result_type为"mr"时需要
        }
    
    Returns:
        str: 操作结果消息
    """
    try:
        # 解析输入参数
        input_data = json.loads(input_json)
        sql_hash = input_data["sql_hash"]
        result_type = input_data["result_type"]  # "ddl", "mr", 或 "ai_analysis"
        result_content = input_data["result_content"]
        ai_decision = input_data.get("ai_decision")  # 可选的AI决策JSON
        
        # 原CSV文件路径
        original_csv_path = Path("/Users/moka/PycharmProjects/SentryAgent/外部文件/审批慢SQL.csv")
        # 修改后的CSV文件路径
        updated_csv_path = Path("/Users/moka/PycharmProjects/SentryAgent/外部文件/审批慢SQL_已分析.csv")
        
        # 确定要读取的CSV文件（优先读取已有的分析结果文件）
        if updated_csv_path.exists():
            csv_file_path = updated_csv_path
            print(f"[信息] 读取已有的分析结果文件: {csv_file_path}")
        elif original_csv_path.exists():
            csv_file_path = original_csv_path
            print(f"[信息] 读取原始CSV文件: {csv_file_path}")
        else:
            return f"错误：CSV文件不存在：{original_csv_path}"
        
        # 读取CSV文件
        df = pd.read_csv(csv_file_path, encoding='utf-8-sig')
        
        # 查找对应的SQL hash行
        hash_column = 'sql_hash'
        if hash_column not in df.columns:
            return f"错误：CSV文件中未找到sql_hash列"
        
        # 找到匹配的行
        matching_rows = df[df[hash_column] == sql_hash]
        
        if matching_rows.empty:
            return f"错误：未找到hash为 {sql_hash} 的记录"
        
        if len(matching_rows) > 1:
            return f"警告：找到多条hash为 {sql_hash} 的记录，将更新第一条"
        
        # 获取行索引
        row_index = matching_rows.index[0]
        
        # 确定要更新的列并添加列标题（如果需要）
        if result_type == "ddl":
            column_index = 5
            column_name = "DDL建议"
            result_label = "DDL建议"
        elif result_type == "mr":
            column_index = 6
            column_name = "MR链接"
            result_label = "MR链接"
        elif result_type == "ai_analysis":
            column_index = 7
            column_name = "AI分析"
            result_label = "AI分析"
        else:
            return f"错误：不支持的结果类型：{result_type}，支持'ddl'、'mr'或'ai_analysis'"
        
        # 确保CSV有足够的列，并设置列名
        while len(df.columns) <= column_index:
            new_col_name = f"分析结果_{len(df.columns) - 4}"  # 从第5列开始是分析结果
            df[new_col_name] = ''
        
        # 设置特定列的名称
        if column_index == 5:
            df.rename(columns={df.columns[5]: "DDL建议"}, inplace=True)
        elif column_index == 6:
            df.rename(columns={df.columns[6]: "MR链接"}, inplace=True)
        elif column_index == 7:
            df.rename(columns={df.columns[7]: "AI分析"}, inplace=True)
        
        # 更新指定行和列，确保列的数据类型正确
        df.iloc[row_index, column_index] = str(result_content)
        
        # 如果是MR类型且有AI决策数据，同时保存到AI分析列
        if result_type == "mr" and ai_decision:
            # 确保AI分析列存在
            while len(df.columns) <= 7:
                new_col_name = f"分析结果_{len(df.columns) - 4}"
                df[new_col_name] = ''
            if len(df.columns) > 7:
                df.rename(columns={df.columns[7]: "AI分析"}, inplace=True)
            
            # 格式化AI决策数据（压缩格式，无换行符）
            ai_analysis_content = json.dumps(ai_decision, ensure_ascii=False, separators=(',', ':'))
            df.iloc[row_index, 7] = ai_analysis_content
        
        # 保存到修改后的CSV文件
        df.to_csv(updated_csv_path, index=False, encoding='utf-8-sig')
        
        return f"成功：已将{result_label}更新到分析结果文件，hash={sql_hash}，内容={result_content}，文件路径：{updated_csv_path}"
        
    except json.JSONDecodeError as e:
        return f"错误：JSON解析失败：{e}"
    except Exception as e:
        return f"错误：更新CSV文件失败：{e}"


def read_slow_sql_by_hash(sql_hash: str) -> Optional[dict]:
    """
    根据hash读取慢SQL信息，优先从分析结果文件读取
    
    Args:
        sql_hash: SQL的hash值
        
    Returns:
        dict: 包含SQL信息的字典，如果未找到则返回None
    """
    try:
        # 原CSV文件路径
        original_csv_path = Path("/Users/moka/PycharmProjects/SentryAgent/外部文件/审批慢SQL.csv")
        # 修改后的CSV文件路径
        updated_csv_path = Path("/Users/moka/PycharmProjects/SentryAgent/外部文件/审批慢SQL_已分析.csv")
        
        # 确定要读取的CSV文件（优先读取已有的分析结果文件）
        if updated_csv_path.exists():
            csv_file_path = updated_csv_path
            print(f"[信息] 从分析结果文件读取: {csv_file_path}")
        elif original_csv_path.exists():
            csv_file_path = original_csv_path
            print(f"[信息] 从原始文件读取: {csv_file_path}")
        else:
            print(f"错误：CSV文件不存在：{original_csv_path}")
            return None
        
        # 读取CSV文件
        df = pd.read_csv(csv_file_path, encoding='utf-8-sig')
        
        # 查找对应的SQL hash行
        matching_rows = df[df['sql_hash'] == sql_hash]
        
        if matching_rows.empty:
            print(f"未找到hash为 {sql_hash} 的记录")
            return None
            
        # 获取第一行匹配记录
        row = matching_rows.iloc[0]
        
        result = {
            "sql_hash": row['sql_hash'],
            "create_time": row['create_time'],
            "count": row['count'],
            "sql_text": row['sql_text']
        }
        
        # 如果是从分析结果文件读取，还包含分析结果
        if csv_file_path == updated_csv_path:
            if 'DDL建议' in df.columns and pd.notna(row.get('DDL建议')):
                result['ddl_suggestion'] = row['DDL建议']
            if 'MR链接' in df.columns and pd.notna(row.get('MR链接')):
                result['mr_link'] = row['MR链接']
            if 'AI分析' in df.columns and pd.notna(row.get('AI分析')):
                result['ai_analysis'] = row['AI分析']
        
        return result
        
    except Exception as e:
        print(f"读取CSV文件失败：{e}")
        return None


# 创建LangChain工具
updateSlowSqlCsvResultTool = Tool(
    name="updateSlowSqlCsvResultTool",
    func=update_slow_sql_csv_result,
    description="更新慢SQL审批CSV文件，将DDL建议或MR链接写入对应hash行的结果列中"
)

readSlowSqlByHashTool = Tool(
    name="readSlowSqlByHashTool", 
    func=lambda hash: json.dumps(read_slow_sql_by_hash(hash), ensure_ascii=False) if read_slow_sql_by_hash(hash) else "未找到对应记录",
    description="根据hash从慢SQL审批CSV文件中读取SQL信息"
)

if __name__ == "__main__":
    print("=== 测试优化后的CSV更新逻辑（包含AI分析列）===")
    
    # 测试读取功能
    print("1. 测试读取慢SQL信息")
    sql_info = read_slow_sql_by_hash("299560ec4687fa45916095da5f793c06")
    print("读取结果：", json.dumps(sql_info, ensure_ascii=False, indent=2) if sql_info else "未找到")
    
    # 测试更新功能 - DDL
    print("\n2. 测试更新DDL结果")
    ddl_update = {
        "sql_hash": "test_hash_ddl_001",
        "result_type": "ddl",
        "result_content": "CREATE INDEX `idx_proc_inst_id` ON `act_hi_taskinst` (`PROC_INST_ID_`);"
    }
    result = update_slow_sql_csv_result(json.dumps(ddl_update, ensure_ascii=False))
    print("DDL更新结果：", result)
    
    # 测试更新功能 - 单独的AI分析
    print("\n3. 测试单独保存AI分析结果")
    ai_analysis_update = {
        "sql_hash": "test_hash_ai_001",
        "result_type": "ai_analysis",
        "result_content": json.dumps({
            "decision_type": "table_design",
            "reason": "测试原因：该表缺少索引",
            "fix_suggest": "测试建议：创建索引提升查询性能",
            "fix_server": "test-service"
        }, ensure_ascii=False, separators=(',', ':'))
    }
    result = update_slow_sql_csv_result(json.dumps(ai_analysis_update, ensure_ascii=False))
    print("AI分析更新结果：", result)
    
    # 测试更新功能 - MR带AI决策
    print("\n4. 测试更新MR结果（同时保存AI决策）")  
    mr_with_ai_update = {
        "sql_hash": "test_hash_mr_001",
        "result_type": "mr", 
        "result_content": "https://gitlab.mokahr.com/hcm-developer/workflow-process/-/merge_requests/123",
        "ai_decision": {
            "decision_type": "business_logic",
            "reason": "该SQL来自批量查询方法，传入参数过多导致IN查询性能下降",
            "fix_suggest": "建议分批处理，每批最多200个参数",
            "fix_server": "hcm-workflow-process-platform"
        }
    }
    result = update_slow_sql_csv_result(json.dumps(mr_with_ai_update, ensure_ascii=False))
    print("MR+AI决策更新结果：", result)
    
    # 验证读取包含所有分析结果
    print("\n5. 验证读取包含完整分析结果")
    test_cases = ["test_hash_ddl_001", "test_hash_ai_001", "test_hash_mr_001"]
    for test_hash in test_cases:
        sql_info_with_analysis = read_slow_sql_by_hash(test_hash)
        print(f"\n测试hash {test_hash}:")
        if sql_info_with_analysis:
            for key, value in sql_info_with_analysis.items():
                if key == 'ai_analysis' and value:
                    # AI分析内容较长，格式化显示
                    try:
                        ai_data = json.loads(value)
                        print(f"  {key}: {json.dumps(ai_data, ensure_ascii=False, indent=4)}")
                    except:
                        print(f"  {key}: {value}")
                else:
                    print(f"  {key}: {value}")
        else:
            print("  未找到记录")
    
    print("\n✅ 测试完成！")
    print("📁 原文件保持不变：外部文件/审批慢SQL.csv") 
    print("📁 分析结果保存至：外部文件/审批慢SQL_已分析.csv")
    print("📊 新增功能：")
    print("  - DDL建议列（第5列）")
    print("  - MR链接列（第6列）") 
    print("  - AI分析列（第7列）- 压缩JSON格式")
    print("  - MR提交时自动保存AI决策数据")