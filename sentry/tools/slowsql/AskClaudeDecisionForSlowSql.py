import asyncio
import json
import re
from typing import Optional

from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions
from langchain_core.tools import Tool


def askClaudeDecisionForSlowSql(slow_sql_info: str, max_retries: int = 1) -> Optional[dict]:
    """
    传入慢SQL相关信息，调用Claude分析并判断优化方案类型，返回JSON格式决策结果
    
    Args:
        slow_sql_info: 慢SQL相关信息（包括SQL语句、执行情况等）
        max_retries: 重试次数
    
    Returns: 
        dict: 包含决策结果的JSON对象，格式如下：
        {
            "decision_type": "table_design" | "business_logic",
            "reason": "分析原因",
            "fix_suggest": "具体建议",
            "fix_server": "相关服务名"
        }
    """
    print("接收到的慢SQL信息:" + slow_sql_info)

    retries = 0
    pattern = r"```json\s*(\{.*?\})\s*```"
    
    while retries < max_retries:
        last_text = asyncio.run(ask_claude_decision(slow_sql_info))

        # 简单提取 ```json ... ``` 中的 JSON
        match = re.search(pattern, last_text, re.DOTALL)
        if match:
            json_str = match.group(1)
            try:
                result_json = json.loads(json_str)
                if all(key in result_json for key in ["decision_type", "reason", "fix_suggest", "fix_server"]):
                    return result_json
            except json.JSONDecodeError:
                pass
        
        print(f"第 {retries + 1} 次尝试解析 JSON 失败，重试...")
        retries += 1

    print("重试次数用完，仍无法得到合法 JSON")
    return None


async def ask_claude_decision(slow_sql_info: str) -> str:
    """
    调用Claude进行慢SQL优化决策分析
    """
    async with ClaudeSDKClient(
            options=ClaudeCodeOptions(
                max_turns=20,
                max_thinking_tokens=10000,
                cwd="/Users/moka/IdeaProjects/PaProjects",
                allowed_tools=["Read", "Bash", "Grep"],
                disallowed_tools=["Write", "Bash(rm*)"],
                permission_mode="default",
                system_prompt="""
                你是一个专业的数据库性能优化决策专家，专门负责慢SQL分析和优化方案决策。

                **重要资源：**
                你可以使用「外部文件/审批库表总结」目录下的文件来获取数据库表结构信息和索引情况。这些文件包含了各个数据库和表的详细结构说明，对于分析慢SQL和制定优化方案非常重要。

                你的核心任务是：
                1. 深入分析慢SQL的执行情况和性能问题根因
                2. 结合数据库表结构和业务代码上下文进行综合判断（使用Read工具查看「外部文件/审批库表总结」中的相关表结构文件）
                3. 决策最优的解决方案类型：表设计调整 OR 业务逻辑调整
                4. 提供具体可执行的优化建议

                决策原则：
                
                **选择表设计调整的情况：**
                - SQL查询涉及的表缺少必要的索引（通过查看「外部文件/审批库表总结」中的表结构确认）
                - 表结构设计不合理导致的查询效率问题
                - 联表查询缺少外键索引
                - 字段类型或长度不当影响查询性能
                - 分区表设计不当
                
                **选择业务逻辑调整的情况：**
                - SQL查询逻辑本身存在优化空间（如避免子查询、优化JOIN等）
                - 业务代码中存在N+1查询问题
                - 批量操作可以替代循环单条操作
                - 缓存策略可以减少数据库查询
                - 分页查询参数不合理
                - 业务逻辑导致的全表扫描

                分析步骤：
                1. 解析SQL语句，识别查询模式和涉及的表
                2. 使用Read工具查看「外部文件/审批库表总结」目录下对应表的结构文件，了解表的字段和索引情况
                3. 分析执行计划，找出性能瓶颈点
                4. 考虑业务代码调用场景（可以使用Grep工具在/Users/moka/IdeaProjects/PaProjects中搜索相关代码）
                5. 权衡方案的实施成本和效果
                6. 做出最终决策并给出具体建议

                输出格式要求：
                必须输出标准JSON格式，包含以下字段：
                - decision_type: "table_design" 或 "business_logic"
                - reason: 详细的问题分析和决策理由
                - fix_suggest: 具体的优化建议和实施方案
                - fix_server: 涉及的服务名称

                示例输出1（表设计调整）：
                ```json
                {
                    "decision_type": "table_design",
                    "reason": "workflow_platform_core库的workflow_core_flow_instance表，经常需要根据flow_def_id字段进行查询，但该字段在表上并无任何索引，导致全表扫描严重影响查询性能",
                    "fix_suggest": "建议新增索引，DDL语句：CREATE INDEX `idx_flow_def_id` ON `workflow_core_flow_instance` (`flow_def_id`);",
                    "fix_server": "hcm-workflow-platform-core"
                }
                ```

                示例输出2（业务逻辑调整）：
                ```json
                {
                    "decision_type": "business_logic", 
                    "reason": "com.moka.workflow.form.platform.composite.formrepo.def.service.impl.FormDefServiceImpl#batchGetByFormDefIdAndVersion 方法传入的formDefIds数量过大（超过1000个），导致IN条件查询性能急剧下降",
                    "fix_suggest": "遵循开闭原则，新增一个V2方法，内部将formDefIds按200个一组进行分块处理，然后循环调用原方法进行查询，最后合并结果。同时将调用方改为使用V2方法",
                    "fix_server": "hcm-workflow-form-platform"
                }
                ```

                注意事项：
                - 必须基于具体的SQL语句和执行情况进行分析，不要做无根据的假设
                - 优先考虑对系统影响最小、实施成本最低的方案
                - 确保建议的可执行性和技术可行性
                - 输出格式必须严格遵守JSON标准
                
                **重要：最终必须输出一个完整的JSON对象，不要包含任何其他内容。JSON对象应该包含decision_type、reason、fix_suggest、fix_server四个字段。**
                """
            )
    ) as client:
        # 发送查询
        print("\n=== Claude 慢SQL决策分析参数 ===\n" + slow_sql_info)
        query_prompt = f"""
        请分析以下慢SQL信息：

        {slow_sql_info}

        请执行分析，然后在最后一定要输出一个JSON格式的决策结果。

        **重要：无论分析过程多复杂，最后必须输出一个完整的JSON对象，格式如下：**

        ```json
        {{
            "decision_type": "table_design 或 business_logic",
            "reason": "详细的问题分析和决策理由",
            "fix_suggest": "具体的优化建议和实施方案", 
            "fix_server": "涉及的服务名称"
        }}
        ```

        决策后请立即输出上述JSON格式，不要有其他结论性文字。
        """
        await client.query(query_prompt)

        full_text = ""
        print("=== Claude 慢SQL决策分析过程开始 ===")
        
        async for message in client.receive_response():
            print(f"\n--- Message ---")
            print(message)
            print(f"--- End Message ---\n")
            
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'text'):
                        full_text += block.text
        
        print("=== Claude 慢SQL决策分析过程结束 ===")
    
    print("\n=== Claude 慢SQL决策分析结果 ===\n" + full_text)
    return full_text


askClaudeDecisionForSlowSqlTool = Tool(
    name="askClaudeDecisionForSlowSqlTool",
    func=askClaudeDecisionForSlowSql,
    description="传入慢SQL信息，使用Claude进行优化方案决策，返回表设计调整或业务逻辑调整的判断结果"
)

if __name__ == '__main__':
    # 测试用例
    test_slow_sql_info = """
    {
        "sql_hash": "abc123",
        "sql_text": "SELECT * FROM workflow_core_flow_instance WHERE flow_def_id = 'def456' AND status = 1",
        "execution_time": "2.5s",
        "rows_examined": 50000,
        "server": "hcm-workflow-platform-core"
    }
    """
    
    result = askClaudeDecisionForSlowSql(test_slow_sql_info)
    print("\naskClaudeDecisionForSlowSqlTool 返回结果：\n")
    print(result)
