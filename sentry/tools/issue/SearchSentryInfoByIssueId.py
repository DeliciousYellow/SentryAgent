import json
import os
from typing import Optional

import requests
import time

from dotenv import load_dotenv
from langchain.tools import Tool

from sentry.Pydantic.SentryIssueAnalysis import SentryIssueAnalysis

SENTRY_BASE_URL = "https://dev-sentry.mokahr.com/"
SENTRY_ORGANIZATION_SLUG = "moka"
load_dotenv()
SENTRY_AUTH_TOKEN = os.environ.get("SENTRY_AUTH_TOKEN")

def search_sentry_json_by_issue_id(issue_id: str) -> str:
    result = search_sentry_info_by_issue_id(issue_id)
    clean_data = json.dumps(remove_none_recursive(result.model_dump()), indent=2)
    return clean_data

def search_sentry_info_by_issue_id(issue_id: str) -> Optional[SentryIssueAnalysis]:
    """
    根据issueId查询sentry信息并返回结构化的分析结果
    """
    api_url = f"{SENTRY_BASE_URL}api/0/issues/{issue_id}/events/latest/"
    headers = {
        "Authorization": f"Bearer {SENTRY_AUTH_TOKEN}"
    }
    print(f"Querying Sentry API: {api_url}")
    return fetch_sentry_data(api_url, headers, issue_id)


def fetch_sentry_data(api_url, headers, issue_id, max_retries=6, base_delay=1):
    """
    从 Sentry API 获取数据，失败时按指数退避重试
    :param api_url: Sentry API URL
    :param headers: 请求头
    :param issue_id: issue ID
    :param max_retries: 最大重试次数
    :param base_delay: 基础等待时间（秒）
    """
    attempt = 0
    while attempt <= max_retries:
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            sentry_data = response.json()

            # 解析 Sentry 数据并构造 SentryIssueAnalysis 对象
            analysis = _parse_sentry_data(sentry_data, issue_id)
            return analysis

        except requests.exceptions.RequestException as e:
            if _is_connection_reset_error(e):
                attempt += 1
                wait_time = base_delay * (2 ** (attempt - 1))  # 指数退避
                print(f"Sentry API 请求失败（第 {attempt} 次）：{e}，{wait_time}s 后重试...")
                time.sleep(wait_time)
            else:
                print(f"请求 Sentry API 失败: {e}")
                return None
        except Exception as e:
            print(f"解析 Sentry 数据失败: {e}")
            return None

    print("达到最大重试次数，仍未成功请求 Sentry API")
    return None


def _is_connection_reset_error(exc):
    """递归检查异常链中是否有 ConnectionResetError"""
    while exc:
        if isinstance(exc, ConnectionResetError):
            return True
        exc = getattr(exc, "__cause__", None) or getattr(exc, "__context__", None)
    return False


def _parse_sentry_data(sentry_data: dict, issue_id: str) -> SentryIssueAnalysis:
    """
    解析 Sentry 原始数据并转换为 SentryIssueAnalysis 对象
    极简版本，只提取必要的原始数据
    """
    # 基本信息
    error_message = sentry_data.get("message", "未知错误")
    timestamp = sentry_data.get("dateCreated")
    
    # 提取核心原始数据
    context = sentry_data.get("context")
    culprit = sentry_data.get("culprit")
    stacktrace_frames = None
    request_data = None
    
    # 处理特殊的消息格式 + 提取原始数据
    entries = sentry_data.get("entries", [])
    for entry in entries:
        entry_type = entry.get("type")
        entry_data = entry.get("data", {})
        
        # 处理消息格式
        if entry_type == "message":
            formatted = entry_data.get("formatted")
            if formatted:
                error_message = formatted
        
        # 提取堆栈跟踪原始数据
        elif entry_type == "stacktrace":
            stacktrace_frames = entry_data.get("frames", [])
        
        # 从异常中提取堆栈跟踪原始数据
        elif entry_type == "exception":
            values = entry_data.get("values", [])
            if values:
                stacktrace = values[0].get("stacktrace", {})
                stacktrace_frames = stacktrace.get("frames", [])
        
        # 提取请求数据
        elif entry_type == "request":
            request_data = entry_data
    
    return SentryIssueAnalysis(
        issue_id=str(issue_id),
        error_message=error_message,
        timestamp=timestamp,
        stacktrace_frames=stacktrace_frames,
        request_data=request_data,
        context=context,
        culprit=culprit
    )

def remove_none_recursive(obj):
    if isinstance(obj, dict):
        return {k: remove_none_recursive(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [remove_none_recursive(v) for v in obj if v is not None]
    else:
        return obj


search_sentry_json_by_issue_id_tool = Tool(
    name="SearchSentryInfoByIssueId",
    func=search_sentry_json_by_issue_id,
    description="根据issueId查询sentry信息"
)

if __name__ == '__main__':
    # issue_id = "21516270"
    issue_id = "21521595"
    result = search_sentry_info_by_issue_id(issue_id)

    if result:
        print(f"\n=== issueId:{issue_id} 分析结果 ===")
        print(f"问题ID: {result.issue_id}")

        print(f"\n完整JSON格式:")
        print(result.model_dump_json(indent=2))
    else:
        print("未查询到sentry信息")
