import getpass
import os

from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

from sentry.tools.slowsql.AskClaudeFixSlowSqlByFixInfo import askClaudeFixSlowSqlByFixInfo, \
    askClaudeFixSlowSqlByFixInfoTool
from sentry.tools.slowsql.SubmitMergeRequestForOptimizeSlowSqlByFixSuggest import \
    submitMergeRequestForOptimizeSlowSqlByFixSuggestTool

load_dotenv()
base_url = "https://api.deepseek.com"

if not os.environ.get("DEEPSEEK_API_KEY"):
    os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter API key for DeepSeek: ")
# 初始化 DeepSeek 模型
model = init_chat_model("deepseek-chat", model_provider="deepseek")

tools = [submitMergeRequestForOptimizeSlowSqlByFixSuggestTool]

# 创建提示模板
prompt = PromptTemplate.from_template("""你是一个专业的Java后端慢SQL分析助手。你的任务是：
    1. 从当前项目根目录下的「外部文件/审批慢SQL.csv」文档读取指定 hash的一条慢SQL信息
    2. 根据慢SQL的文本，结合「外部文件/审批库表总结」目录下的文件，分析该SQL所在代码中的位置（/Users/moka/IdeaProjects/PaProjects）
    3. 判断该慢SQL的解决方案，是可以调整表设计解决，或是调整业务逻辑解决
    4. 如果是调整表设计的方案，则输出修改方案
    示例：
        输出：
            [{{"reason":"workflow_platform_core库的workflow_core_flow_instance表，经常需要根据flow_def_id查询相关记录，但该字段在表上并无任何索引","fix_suggest":"建议新增索引，DDL语句：CREATE INDEX `idx_flow_def_id` ON `workflow_core_flow_instance` (`flow_def_id`);","fix_server":"hcm-workflow-platform-core"}}]
    
    5. 如果是调整业务逻辑解决，则调用SubmitMergeRequestForOptimizeSlowSqlByFixSuggest自动修复并提交MR。最终输出MR链接和描述
    SubmitMergeRequestForOptimizeSlowSqlByFixSuggest的使用示例：
        输入：
            [{{"reason":"com.moka.workflow.form.platform.composite.formrepo.def.service.impl.FormDefServiceImpl#batchGetByFormDefIdAndVersion 方法传入的formDefIds数量太多，导致SQL查询变慢","fix_suggest":"遵循开闭原则，新增一个V2方法，内部把formDefIds分块再依次查询，然后将调用方改为使用V2方法","fix_server":"hcm-workflow-form-platform"}}]
        输出：
            新增了分块查询逻辑
            MR:https://gitlab.mokahr.com/hcm-developer/xxx/-/merge_requests/xxx
    ================================================================================================================
    调用「askClaudeFixSlowSqlByFixInfoTool」和「submitMergeRequestForOptimizeSlowSqlByFixSuggest」时，必须传入标准JSON格式
    请始终使用可用的工具来获取准确的信息，而不是基于假设回答。
    
    你可以使用以下工具：
    {tools}
    
    请使用以下格式：
    问题: {input}
    思考: 你应该总是思考要做什么
    动作: 要采取的动作，应该是 [{tool_names}] 中的一个
    动作输入: 动作的输入
    观察: 动作的结果
    ... (这个 思考/动作/动作输入/观察 可以重复N次)
    思考: 我现在知道了最终答案
    最终答案: 对原始输入问题的最终答案
    {agent_scratchpad}""")

agent = create_react_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 循环对话
while True:
    try:
        question = input("请输入问题（输入 'exit' 退出）：\n")
        if question.lower() in ("exit", "quit"):
            print("已退出。")
            break

        print("正在处理您的问题...")
        result = agent_executor.invoke({"input": question})
        print("Agent回答：", result)

    except KeyboardInterrupt:
        print("\n已手动中断。")
        break
    except Exception as e:
        print(f"出错了：{e}")
        print(f"错误类型：{type(e).__name__}")