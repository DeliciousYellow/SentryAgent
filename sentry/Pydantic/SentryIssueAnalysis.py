from typing import Optional, Dict, Any, List

from pydantic import BaseModel, Field


class SentryIssueAnalysis(BaseModel):
    """Sentry 问题分析结果 - 极简版本，只保留核心原始数据"""
    
    model_config = {"exclude_none": True}  # 排除None值

    issue_id: str = Field(description="Sentry 问题的唯一标识ID")
    error_message: str = Field(description="错误消息")
    timestamp: Optional[str] = Field(default=None, description="发生时间")
    
    # 原始数据（核心信息）
    stacktrace_frames: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="来自entries[stacktrace].data.frames的原始堆栈帧数据"
    )
    
    request_data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="来自entries[request].data的原始请求数据"
    )
    
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="来自sentry_data.context的上下文信息"
    )
    
    culprit: Optional[str] = Field(
        default=None,
        description="来自sentry_data.culprit的罪魁祸首信息"
    )
    
    def to_ai_analysis_format(self) -> Dict[str, Any]:
        """转换为AI分析所需的格式"""
        
        # 构建堆栈跟踪字符串
        stack_trace_lines = []
        first_filename = None
        first_line_number = None
        
        if self.stacktrace_frames:
            for frame in self.stacktrace_frames:
                filename = frame.get("filename", "unknown")
                function = frame.get("function", "unknown")
                line_no = frame.get("lineNo")
                module = frame.get("module", "")
                
                if line_no:
                    line_str = f"at {module}.{function}({filename}:{line_no})"
                    # 记录第一个有效的文件和行号
                    if not first_filename and filename != "unknown":
                        first_filename = filename
                        first_line_number = line_no
                else:
                    line_str = f"at {module}.{function}({filename})"
                
                stack_trace_lines.append(line_str)
        
        return {
            "issue_id": self.issue_id,
            "error_message": self.error_message,
            "error_type": "Unknown",  # 从error_message推断
            "stack_trace": "\n".join(stack_trace_lines),
            "source_code": None,  # 需要单独获取
            "file_name": first_filename,
            "line_number": first_line_number
        }
