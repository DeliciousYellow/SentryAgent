import getpass
import os

from dotenv import load_dotenv
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from sentry.tools.AskClaudeFixSlowSqlByFixInfo import askClaudeFixSlowSqlByFixInfoTool
from sentry.tools.AskClaudeForFixSuggestByIssueId import askClaudeForFixSuggestByIssueIdTool
from sentry.tools.SubmitMergeRequestByFixSuggest import submitMergeRequestByFixSuggestTool
from sentry.tools.SubmitMergeRequestForOptimizeSlowSqlByFixSuggest import \
    submitMergeRequestForOptimizeSlowSqlByFixSuggestTool

load_dotenv()

if not os.environ.get("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter API key for Anthropic Claude: ")

# 支持自定义 base_url（用于中转站）
base_url = os.environ.get("ANTHROPIC_BASE_URL")
if base_url:
    print(f"使用自定义 base_url: {base_url}")

# 初始化 Claude 模型
model = init_chat_model("claude-3-5-sonnet", model_provider="anthropic", base_url=base_url)

tools = [askClaudeFixSlowSqlByFixInfoTool, submitMergeRequestForOptimizeSlowSqlByFixSuggestTool]

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的Java后端慢SQL分析助手。你的任务是：
        1. 从当前项目根目录下的「外部文件/审批慢SQL.csv」文档读取指定 hash的一条慢SQL信息
        2. 根据慢SQL的文本，结合「外部文件/审批库表总结」目录下的文件，分析该SQL所在代码中的位置（/Users/moka/IdeaProjects/PaProjects）
        3. 判断该慢SQL的解决方案，是可以调整表设计解决，或是调整业务逻辑解决
        4. 如果是调整表设计的方案，则输出修改方案
        示例：
            输出：
                [{{\"reason\":\"workflow_platform_core库的workflow_core_flow_instance表，经常需要根据flow_def_id查询相关记录，但该字段在表上并无任何索引\",\"fix_suggest\":\"建议新增索引，DDL语句：CREATE INDEX `idx_flow_def_id` ON `workflow_core_flow_instance` (`flow_def_id`);\",\"fix_server\":\"hcm-workflow-platform-core\"}}]
    
        5. 如果是调整业务逻辑解决，则调用SubmitMergeRequestForOptimizeSlowSqlByFixSuggest自动修复并提交MR。最终输出MR链接和描述
        SubmitMergeRequestForOptimizeSlowSqlByFixSuggest的使用示例：
            输入：
                [{{\"reason\":\"com.moka.workflow.form.platform.composite.formrepo.def.service.impl.FormDefServiceImpl#batchGetByFormDefIdAndVersion 方法传入的formDefIds数量太多，导致SQL查询变慢\",\"fix_suggest\":\"遵循开闭原则，新增一个V2方法，内部把formDefIds分块再依次查询，然后将调用方改为使用V2方法\",\"fix_server\":\"hcm-workflow-form-platform\"}}]
            输出：
                新增了分块查询逻辑
                MR:https://gitlab.mokahr.com/hcm-developer/xxx/-/merge_requests/xxx
        ================================================================================================================
        调用「askClaudeFixSlowSqlByFixInfoTool」和「submitMergeRequestForOptimizeSlowSqlByFixSuggest」时，必须传入标准JSON格式
        请始终使用可用的工具来获取准确的信息，而不是基于假设回答。"""
     ),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad")
])

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 循环对话
while True:
    try:
        question = input("请输入问题（输入 'exit' 退出）：\n")
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
        print(f"错误类型：{type(e).__name__}")
        import traceback
        traceback.print_exc()