import getpass
import os

from dotenv import load_dotenv
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from sentry.tools.issue.AskClaudeForFixSuggestByIssueId import askClaudeForFixSuggestByIssueIdTool
from sentry.tools.issue.SubmitMergeRequestByFixSuggest import submitMergeRequestByFixSuggestTool

load_dotenv()
base_url = "https://api.deepseek.com"

if not os.environ.get("DEEPSEEK_API_KEY"):
    os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter API key for DeepSeek: ")
# 初始化 DeepSeek 模型
model = init_chat_model("deepseek-chat", model_provider="deepseek")

tools = [askClaudeForFixSuggestByIssueIdTool, submitMergeRequestByFixSuggestTool]

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的Java后端开发错误分析助手。你的任务是：
        1. 根据用户提供的IssueId，调用askClaudeForFixSuggestByIssueIdTool分析错误和修复建议
        调用askClaudeForFixSuggestByIssueIdTool时，直接传入IssueId字符串即可
        2. 如果是非技术BUG，直接返回分析的结果
        3. 判断如果是技术BUG，调用submitMergeRequestByFixSuggestTool提交MR
        调用askClaudeForFixSuggestByIssueIdTool时，必须传入标准JSON格式
        示例：
            askClaudeForFixSuggestByIssueIdTool示例输入为：
            {{
                "need_fix_project_name": "hcm-workflow-platform-access",
                "new_branch_name": "hc-ai/fix/issue-id-21520265",
                "base_branch_name": "release",
                "fix_info": {{
                    "reason": "…空指针异常描述…",
                    "fix_suggest": "在…前增加 if (Objects.isNull(formDefDataDTO)) {{return goOutDigestSingleModelHandler.doGetDigestFieldWithData(calReq);}}",
                    "error_server": "hcm-workflow-platform-access"
                }}
            }}
            其中new_branch_name是固定的 hc-ai/fix/issue-id-「本次提问的IssueId」
            fix_info是askClaudeForFixSuggestByIssueIdTool返回的JSON内容不做任何修改
            need_fix_project_name一般都与error_server一致，需要你理解并赋值
        请始终使用可用的工具来获取准确的信息，而不是基于假设回答。"""
     ),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad")
])

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# result = agent_executor.invoke({"input": "issuesId为 21516736"})
# print("Agent回答：", result)
# 循环对话
while True:
    try:
        question = input("请输入IssueId（输入 'exit' 退出）：\n")
        if question.lower() in ("exit", "quit"):
            print("已退出。")
            break

        result = agent_executor.invoke({"input": question})
        print("Agent回答：", result)

    except KeyboardInterrupt:
        print("\n已手动中断。")
        break
    except Exception as e:
        print(f"出错了：{e}")

# issuesId为 21516736 上传文件的文件名不能超过150个字符
# issuesId为 21513875 空指针
# issuesId为 21514138 动态接口调用失败 Access
# issuesId为 21520265 示例的空指针
