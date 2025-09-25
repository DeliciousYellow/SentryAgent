import asyncio
from typing import Optional

from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions
from langchain_core.tools import Tool


def askClaudeFixCodeFileByFixInfo(fix_info_json: str, worktree_path: str) -> Optional[dict]:
    """
    接收fix_info JSON字符串，调用Claude进行代码修改，返回修改后的文件内容
    
    Args:
        fix_info_json: 包含reason, fix_suggest, error_server的JSON字符串
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
                - 不要在代码中新增任何AI代码修复报告
                - 你无需任何输出
                示例输入：
                {{"reason": "GoOutDigestAdapter.java:69因为formDefDataDTO为NULL导致发生了空指针异常", "fix_suggest": "在GoOutDigestAdapter.java:69前增加空指针检查", "error_server": "hcm-workflow-platform-access"}}
                """
            )
    ) as client:
        # 发送修复请求
        print("\n=== Claude 代码修复参数 ===\n" + fix_info_json)
        await client.query(fix_info_json)

        full_text = ""
        print("=== Claude 代码修复过程开始 ===")
        
        async for message in client.receive_response():
            print(f"\n--- Message ---")
            print(message)
            print(f"--- End Message ---\n")
            
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'text'):
                        full_text += block.text
        
        print("=== Claude 代码修复过程结束 ===")

    print("\n=== Claude 代码修复结果 ===\n" + full_text)
    return full_text


askClaudeFixCodeFileByFixInfoTool = Tool(
    name="askClaudeFixCodeFileByFixInfoTool",
    func=askClaudeFixCodeFileByFixInfo,
    description="根据修复信息JSON，请求Claude进行代码文件修改"
)

if __name__ == '__main__':
    # 测试用例
    test_fix_info = """
    {
        "reason": "com/moka/workflow/platform/access/composite/message/handler/impl/digest/impl/GoOutDigestAdapter.java:69因为formDefDataDTO为NULL导致发生了空指针异常",
        "fix_suggest": "在com/moka/workflow/platform/access/composite/message/handler/impl/digest/impl/GoOutDigestAdapter.java:69前增加「if (Objects.isNull(formDefDataDTO)) {return goOutDigestSingleModelHandler.doGetDigestFieldWithData(calReq);}」",
        "error_server": "hcm-workflow-platform-access"
    }
    """

    test_worktree_path = "/Users/moka/IdeaProjects/PaProjects/hc-ai/fix/issue-id-21520265/hcm-workflow-platform-access"
    result = askClaudeFixCodeFileByFixInfo(test_fix_info, test_worktree_path)
    print("\naskClaudeFixCodeFileByFixInfoTool 返回结果：\n")
    print(result)
