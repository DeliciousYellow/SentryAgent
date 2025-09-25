import asyncio
import json
import re
from typing import Optional

from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions
from langchain_core.tools import Tool

from sentry.tools.issue.SearchSentryInfoByIssueId import search_sentry_json_by_issue_id


def askClaudeForFixSuggestByIssueId(issue_id, max_retries: int = 1) -> Optional[dict]:
    """
        传入issue_id自动查询Issue信息，调用Claude分析，并返回JSON格式修复建议
    """
    messages_content = search_sentry_json_by_issue_id(issue_id)
    print("查询到的Issue信息:" + messages_content)

    retries = 0
    pattern = r"```json\s*(\{.*?\})\s*```"
    while retries < max_retries:
        last_text = asyncio.run(ask_claude(messages_content))

        # 尝试提取 ```json ... ``` 中的 JSON
        match = re.search(pattern, last_text, re.DOTALL)
        if match:
            json_str = match.group(1)
            try:
                result_json = json.loads(json_str)
                return result_json
            except json.JSONDecodeError:
                print(f"第 {retries + 1} 次解析提取的 JSON 失败，重试...")
        else:
            # 尝试直接解析整个文本
            try:
                result_json = json.loads(last_text)
                return result_json
            except json.JSONDecodeError:
                print(f"第 {retries + 1} 次解析原文本 JSON 失败，重试...")

        retries += 1

    print("重试次数用完，仍无法得到合法 JSON")
    return None


async def ask_claude(req_json: str) -> str:
    async with ClaudeSDKClient(
            options=ClaudeCodeOptions(
                max_turns=20,
                max_thinking_tokens=10000,
                cwd="/Users/moka/IdeaProjects/PaProjects",
                allowed_tools=["Read", "Bash", "Grep"],
                disallowed_tools=["Write", "Bash(rm*)"],
                permission_mode="plan",
                system_prompt="""
                你需要根据输入的Sentry告警信息：
                1.分析报错所在方法的上下文，并分析报错原因
                2.具体问题发生在什么服务（如果是调用["hcm-workflow-platform-web","hcm-workflow-platform-core","hcm-workflow-form-platform","hcm-workflow-process-platform""hcm-workflow-platform-access"]服务之外的接口导致的问题，则输出对应的服务）
                3.可能的修复方案
                你的最终输出只能是标准的JSON格式
                完整的输入输出示例：
                示例1：
                    输入：
                    {"issue_id":"21520265","error_message":"GoOutDigestAdapter-getDigestFieldWithData策略判断失败走默认逻辑","timestamp":"2025-08-26T03:04:35Z","stacktrace_frames":[{"filename":"CoreMessageConsumer.java","absPath":"CoreMessageConsumer.java","module":"com.moka.workflow.platform.access.runner.mq.CoreMessageConsumer","function":"onMessage","context":[],"lineNo":34,"inApp":false},{"filename":"AbsCoreMessageConsumer.java","absPath":"AbsCoreMessageConsumer.java","module":"com.moka.workflow.platform.access.runner.mq.AbsCoreMessageConsumer","function":"doMessage","context":[],"lineNo":60,"inApp":false},{"filename":"MessageRouter.java","absPath":"MessageRouter.java","module":"com.moka.workflow.platform.access.composite.message.MessageRouter","function":"route","context":[],"lineNo":51,"inApp":false},{"filename":"AbstractMessageProcessor.java","absPath":"AbstractMessageProcessor.java","module":"com.moka.workflow.platform.access.composite.message.processor.impl.AbstractMessageProcessor","function":"process","context":[],"lineNo":102,"inApp":false},{"filename":"Optional.java","absPath":"Optional.java","module":"java.util.Optional","function":"ifPresent","context":[],"lineNo":159,"inApp":false},{"filename":"AbstractMessageProcessor.java","absPath":"AbstractMessageProcessor.java","module":"com.moka.workflow.platform.access.composite.message.processor.impl.AbstractMessageProcessor","function":"lambda$process$1","context":[],"lineNo":105,"inApp":false},{"filename":"AddCommentPushMessageHandler.java","absPath":"AddCommentPushMessageHandler.java","module":"com.moka.workflow.platform.access.composite.message.handler.impl.push.impl.AddCommentPushMessageHandler","function":"handle","context":[],"lineNo":101,"inApp":false},{"filename":"AddCommentPushMessageHandler.java","absPath":"AddCommentPushMessageHandler.java","module":"com.moka.workflow.platform.access.composite.message.handler.impl.push.impl.AddCommentPushMessageHandler","function":"processCommentAt","context":[],"lineNo":187,"inApp":false},{"filename":"AddCommentPushMessageHandler.java","absPath":"AddCommentPushMessageHandler.java","module":"com.moka.workflow.platform.access.composite.message.handler.impl.push.impl.AddCommentPushMessageHandler","function":"doPush","context":[],"lineNo":216,"inApp":false},{"filename":"AddCommentPushMessageHandler.java","absPath":"AddCommentPushMessageHandler.java","module":"com.moka.workflow.platform.access.composite.message.handler.impl.push.impl.AddCommentPushMessageHandler","function":"getDigestContent","context":[],"lineNo":287,"inApp":false},{"filename":"GoOutDigestAdapter.java","absPath":"GoOutDigestAdapter.java","module":"com.moka.workflow.platform.access.composite.message.handler.impl.digest.impl.GoOutDigestAdapter","function":"getDigestFieldWithData","context":[],"lineNo":69,"inApp":false}],"context":{"Sentry-Threadname":"org.springframework.kafka.KafkaListenerEndpointContainer#1-0-C-1","X-B3-SpanId":"a872d26ad8a7436e","X-B3-TraceId":"a872d26ad8a7436e","X-Span-Export":"false","applicationName":"hcm-workflow-platform-access","hostAddress":"172.17.113.38","hostname":"hcm-workflow-platform-access-78f6886586-b64j9","loggingLevelRoot":"info","spanExportable":"false","spanId":"a872d26ad8a7436e","springProfilesActive":"prod-ali","traceId":"a872d26ad8a7436e"},"culprit":"com.moka.workflow.platform.access.composite.message.handler.impl.digest.impl.GoOutDigestAdapter in getDigestFieldWithData"}
                    输出：
                    {"reason": "com/moka/workflow/platform/access/composite/message/handler/impl/digest/impl/GoOutDigestAdapter.java:69因为formDefDataDTO为NULL导致发生了空指针异常","fix_suggest": "在com/moka/workflow/platform/access/composite/message/handler/impl/digest/impl/GoOutDigestAdapter.java:69前增加「if (Objects.isNull(formDefDataDTO)) {return goOutDigestSingleModelHandler.doGetDigestFieldWithData(calReq);}」","error_server": "hcm-workflow-platform-access"}
                示例2：
                    输入：
                    {"issue_id":"21521595","error_message":"preCheckDataLanding Access:HCM,PreCheckInterface:http://hcm-organization/client/org/workflow/v1/precheck/contractjobchange  error换签合同开始日期不能小于等于原合同开始日期:","timestamp":"2025-08-28T08:41:39Z","stacktrace_frames":[{"filename":"CommonConcurrentTaskExecutor.java","absPath":"CommonConcurrentTaskExecutor.java","module":"com.moka.workflow.platform.base.common.util.CommonConcurrentTaskExecutor","function":"lambda$executeTaskList$0","context":[],"lineNo":73,"inApp":false},{"filename":"LinkedLandingHandler.java","absPath":"LinkedLandingHandler.java","module":"com.moka.workflow.form.platform.composite.formrepo.checkListLanding.service.LinkedLandingHandler$1","function":"call","context":[],"inApp":false},{"filename":"LinkedLandingHandler.java","absPath":"LinkedLandingHandler.java","module":"com.moka.workflow.form.platform.composite.formrepo.checkListLanding.service.LinkedLandingHandler$1","function":"call","context":[],"inApp":false},{"filename":"InstanceMethodInterTemplate.java","absPath":"InstanceMethodInterTemplate.java","module":"org.apache.skywalking.apm.plugin.jdk.threading.ThreadingMethodInterceptor_internal","function":"intercept","context":[],"lineNo":87,"inApp":false},{"module":"com.moka.workflow.form.platform.composite.formrepo.checkListLanding.service.LinkedLandingHandler$1$auxiliary$mo3OnJ2L","function":"call","context":[],"inApp":false},{"filename":"LinkedLandingHandler.java","absPath":"LinkedLandingHandler.java","module":"com.moka.workflow.form.platform.composite.formrepo.checkListLanding.service.LinkedLandingHandler$1","function":"call$accessor$MG4PrW8T","context":[],"inApp":false},{"filename":"CommonConcurrentTaskExecutor.java","absPath":"CommonConcurrentTaskExecutor.java","module":"com.moka.workflow.platform.base.common.util.CommonConcurrentTaskExecutor$Task","function":"call","context":[],"inApp":false},{"filename":"InstanceMethodInterTemplate.java","absPath":"InstanceMethodInterTemplate.java","module":"org.apache.skywalking.apm.plugin.jdk.threading.ThreadingMethodInterceptor_internal","function":"intercept","context":[],"lineNo":87,"inApp":false},{"module":"com.moka.workflow.platform.base.common.util.CommonConcurrentTaskExecutor$Task$auxiliary$SaZyKsIw","function":"call","context":[],"inApp":false},{"filename":"CommonConcurrentTaskExecutor.java","absPath":"CommonConcurrentTaskExecutor.java","module":"com.moka.workflow.platform.base.common.util.CommonConcurrentTaskExecutor$Task","function":"call$original$DTIWC3MG$accessor$o75ziOMZ","context":[],"inApp":false},{"filename":"CommonConcurrentTaskExecutor.java","absPath":"CommonConcurrentTaskExecutor.java","module":"com.moka.workflow.platform.base.common.util.CommonConcurrentTaskExecutor$Task","function":"call$original$DTIWC3MG","context":[],"lineNo":220,"inApp":false},{"filename":"LinkedLandingHandler.java","absPath":"LinkedLandingHandler.java","module":"com.moka.workflow.form.platform.composite.formrepo.checkListLanding.service.LinkedLandingHandler$1","function":"apply","context":[],"lineNo":89,"inApp":false},{"filename":"LinkedLandingHandler.java","absPath":"LinkedLandingHandler.java","module":"com.moka.workflow.form.platform.composite.formrepo.checkListLanding.service.LinkedLandingHandler$1","function":"apply","context":[],"lineNo":118,"inApp":false},{"filename":"FeignInvoker.java","absPath":"FeignInvoker.java","module":"com.moka.workflow.form.platform.composite.utils.FeignInvoker","function":"preCheckDataLanding","context":[],"lineNo":94,"inApp":false},{"filename":"DefaultInvoker.java","absPath":"DefaultInvoker.java","module":"com.moka.workflow.platform.base.common.invoker.DefaultInvoker","function":"getResultByInterfaceKey","context":[],"lineNo":96,"inApp":false},{"filename":"DefaultInvoker.java","absPath":"DefaultInvoker.java","module":"com.moka.workflow.platform.base.common.invoker.DefaultInvoker","function":"getResultByInterfaceKeyInfo","context":[],"lineNo":126,"inApp":false}],"context":{"Sentry-Threadname":"checkListPreCheck-9","X-B3-ParentSpanId":"844fd6d2a3cd3d62","X-B3-SpanId":"f1bca746df829657","X-B3-TraceId":"2a93b5f93adf81df","X-Span-Export":"false","applicationName":"hcm-workflow-form-platform","hostAddress":"172.17.209.51","hostname":"hcm-workflow-form-platform-7b588f5c57-rs5gn","loggingLevelRoot":"info","parentId":"844fd6d2a3cd3d62","spanExportable":"false","spanId":"f1bca746df829657","springProfilesActive":"prod-ali","traceId":"2a93b5f93adf81df"},"culprit":"com.moka.workflow.platform.base.common.invoker.DefaultInvoker in getResultByInterfaceKeyInfo"}
                    输出：
                    {"reason":"调用`http://hcm-organization/client/org/workflow/v1/precheck/contractjobchange`接口时，业务校验失败：换签合同开始日期不能小于等于原合同开始日期","fix_suggest":"业务校验非技术问题","error_server":"hcm-organization"}
                """
            )
    ) as client:
        # 发送查询
        print("\n=== Claude 分析参数 ===\n" + req_json)
        await client.query(req_json)

        full_text = ""
        print("=== Claude 分析过程开始 ===")
        
        async for message in client.receive_response():
            print(f"\n--- Message ---")
            print(message)
            print(f"--- End Message ---\n")
            
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'text'):
                        full_text += block.text
        
        print("=== Claude 分析过程结束 ===")
    print("\n=== Claude 分析结果 ===\n" + full_text)
    return full_text


askClaudeForFixSuggestByIssueIdTool = Tool(
    name="askClaudeForFixSuggestByIssueIdTool",
    func=askClaudeForFixSuggestByIssueId,
    description="使用IssueId，请求Claude并给出修复建议"
)

if __name__ == '__main__':
    # "21520265"
    # "21513589"
    # "21521595"
    # "21521511"
    # "21521408"
    # "21521723"
    result = askClaudeForFixSuggestByIssueId("21515919")
    print("askClaudeForFixSuggestByIssueIdTool结果:\n")
    print(result)
