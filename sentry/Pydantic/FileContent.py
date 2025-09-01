from pydantic import BaseModel, Field


class FileContent(BaseModel):
    """文件搜索到的结果"""
    file_path: str = Field(description="文件路径")
    file_content: str = Field(description="文件内容")
