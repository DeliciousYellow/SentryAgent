import getpass
import os

# 禁用 gRPC 的 ALTS 警告
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_TRACE"] = ""

from dotenv import load_dotenv
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# submitMergeRequestForOptimizeSlowSqlByFixSuggestTool 内部已包含代码修复功能，无需单独的修复工具
from sentry.tools.slowsql.AskClaudeDecisionForSlowSql import askClaudeDecisionForSlowSqlTool
from sentry.tools.slowsql.SubmitMergeRequestForOptimizeSlowSqlByFixSuggest import \
    submitMergeRequestForOptimizeSlowSqlByFixSuggestTool
from sentry.tools.slowsql.UpdateSlowSqlCsvResult import updateSlowSqlCsvResultTool, readSlowSqlByHashTool

load_dotenv()

if not os.environ.get("DEEPSEEK_API_KEY"):
    os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter API key for DeepSeek: ")
# 初始化 DeepSeek 模型
model = init_chat_model("deepseek-chat", model_provider="deepseek")

tools = [readSlowSqlByHashTool, askClaudeDecisionForSlowSqlTool, submitMergeRequestForOptimizeSlowSqlByFixSuggestTool, updateSlowSqlCsvResultTool]

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的Java后端慢SQL分析助手。
    用户会直接输入一个慢SQL的hash值，你需要对这个hash对应的慢SQL进行分析和优化。
    你的任务是：
        1. 使用「readSlowSqlByHashTool」，传入用户输入的hash值来读取慢SQL信息
        2. 调用「askClaudeDecisionForSlowSqlTool」决策工具，传入慢SQL的相关信息，让决策工具进行完整分析，包括：
           - 分析SQL所在代码位置
           - 结合数据库表结构进行分析
           - 判断是通过调整表设计解决，还是通过调整业务逻辑解决
        3. 根据决策结果执行相应操作：
        
        **如果是表设计调整（decision_type="table_design"）：**
        - 输出DDL建议
        - 调用「updateSlowSqlCsvResultTool」将DDL语句记录到CSV文件
            
        **如果是业务逻辑调整（decision_type="business_logic"）：**  
        - 调用「submitMergeRequestForOptimizeSlowSqlByFixSuggestTool」自动修复并提交MR
          参数格式：{{"need_fix_project_name":"决策结果中的fix_server","new_branch_name":"hc-ai/fix/slow-sql-{{input}}","base_branch_name":"release","fix_info":{{"reason":"决策结果中的reason","fix_suggest":"决策结果中的fix_suggest","fix_server":"决策结果中的fix_server"}}}}
        - 调用「updateSlowSqlCsvResultTool」将MR链接和AI决策记录到CSV文件
          参数格式：{{"sql_hash":"{{input}}","result_type":"mr","result_content":"MR链接","ai_decision":决策结果的完整JSON对象}}
        
        请始终使用可用的工具来获取准确的信息，而不是基于假设回答。"""
     ),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad")
])

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

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
