import asyncio
from typing import Optional

from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions
from langchain_core.tools import BaseTool, Tool


def askClaudeFixSlowSqlByFixInfo(fix_info_json: str, worktree_path: str) -> Optional[dict]:
    """
    接收fix_info JSON字符串，调用Claude进行代码修改，返回修改后的文件内容
    
    Args:
        fix_info_json: 包含reason, fix_suggest, fix_server的JSON字符串
        worktree_path: 指定的工作目录路径
    
    Returns: None
    """
    print("接收到的修复信息:" + fix_info_json)
    print(f"使用指定的工作目录: {worktree_path}")
    asyncio.run(ask_claude_fix(fix_info_json, worktree_path))
    return None


async def ask_claude_fix(fix_info_json: str, worktree_path: str = None) -> str:
    """
    调用Claude进行代码修改
    """
    print(f"使用worktree工作目录: {worktree_path}")

    async with ClaudeSDKClient(
            options=ClaudeCodeOptions(
                max_turns=20,
                max_thinking_tokens=10000,
                cwd=worktree_path,
                allowed_tools=["Read", "Bash", "Grep", "Write", "Edit"],
                disallowed_tools=["Bash(rm*)"],
                permission_mode="acceptEdits",
                system_prompt=f"""
                你是一个专业的慢SQL优化Java工程师
                你需要根据输入的修复信息对代码文件进行修改：
                
                1. 根据 reason 字段理解问题原因
                2. 根据 fix_suggest 字段中的具体修复建议进行代码修改
                3. 使用 Read 工具读取需要修改的文件
                4. 使用 Edit 或 Write 工具实现具体的代码修改
                5. 确保修改后的代码语法正确且逻辑合理
                6. 所有的修改无需确认，直接执行
                
                注意事项：
                - 仔细分析 fix_suggest 中的文件路径和具体修改位置
                - 如果涉及导入新的类，请确保添加相应的 import 语句
                - 保持原有代码的格式和风格
                - 只修改必要的部分，不要做不相关的改动
                - 不要在代码中新增任何AI慢SQL优化报告
                - 你无需任何输出
                示例输入：
                [{{"reason":"com.moka.workflow.form.platform.composite.formrepo.def.service.impl.FormDefServiceImpl#batchGetByFormDefIdAndVersion 方法传入的formDefIds数量太多，导致SQL查询变慢","fix_suggest":"遵循开闭原则，新增一个V2方法，内部把formDefIds分块再依次查询，然后将调用方改为使用V2方法","fix_server":"hcm-workflow-form-platform"}}]
                """
            )
    ) as client:
        # 发送修复请求
        print("\n=== Claude 慢SQL优化参数 ===\n" + fix_info_json)
        await client.query(fix_info_json)

        full_text = ""
        print("=== Claude 慢SQL优化过程开始 ===")
        async for message in client.receive_response():
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'text'):
                        # 边打印边收集
                        print("\n")
                        print(block.text, end='', flush=True)
                        full_text += block.text
        print("\n=== Claude 慢SQL优化过程结束 ===")

    print("\n=== Claude 慢SQL优化结果 ===\n" + full_text)
    return full_text


askClaudeFixSlowSqlByFixInfoTool = Tool(
    name="askClaudeFixSlowSqlByFixInfoTool",
    func=askClaudeFixSlowSqlByFixInfo,
    description="根据修复信息JSON，请求Claude进行代码文件修改"
)

if __name__ == '__main__':
    # 测试用例
    test_fix_info = """
    [{"reason":"com.moka.workflow.form.platform.composite.formrepo.def.service.impl.FormDefServiceImpl#batchGetByFormDefIdAndVersion 方法传入的formDefIds数量太多，导致SQL查询变慢","fix_suggest":"遵循开闭原则，新增一个V2方法，内部把formDefIds分块再依次查询，然后将调用方改为使用V2方法","fix_server":"hcm-workflow-form-platform"}]
    """

    test_worktree_path = "/Users/moka/IdeaProjects/PaProjects/hc-ai/fix/issue-id-21520265/hcm-workflow-platform-access"
    result = askClaudeFixSlowSqlByFixInfo(test_fix_info, test_worktree_path)
    print("\naskClaudeFixSlowSqlByFixInfoTool 返回结果：\n")
    print(result)
