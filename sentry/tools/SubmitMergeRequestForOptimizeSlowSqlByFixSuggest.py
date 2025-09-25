import json
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import gitlab
from langchain_core.tools import Tool
from sentry.tools.AskClaudeFixCodeFileByFixInfo import askClaudeFixCodeFileByFixInfo


class BuildPullRequest:
    def __init__(self, repo_path, project_id, base_branch, new_branch):
        load_dotenv()
        self.gitlab_token = os.environ.get("GITLAB_TOKEN")
        if not self.gitlab_token:
            raise ValueError("必须设置 GITLAB_TOKEN 环境变量")

        self.gitlab_url = os.environ.get("GITLAB_URL")
        if not self.gitlab_url:
            raise ValueError("必须设置 GITLAB_URL 环境变量")

        self.repo_path = Path(repo_path)
        self.project_id = project_id
        self.base_branch = base_branch
        self.new_branch = new_branch

        # 生成 worktree 路径，hc-ai 作为父文件夹
        if self.new_branch.startswith("hc-ai/"):
            # 提取 hc-ai 后面的部分作为子目录
            sub_path = self.new_branch[6:]  # 去掉 "hc-ai/" 前缀
            self.worktree_path = self.repo_path.parent / "hc-ai" / sub_path / self.repo_path.name
        else:
            # 非 hc-ai 分支保持原有逻辑
            self.worktree_name = self.new_branch.replace("/", "-")
            self.worktree_path = self.repo_path.parent / self.worktree_name / self.repo_path.name

        # 初始化 GitLab 客户端
        self.gl = gitlab.Gitlab(self.gitlab_url, private_token=self.gitlab_token)
        self.project = self.gl.projects.get(self.project_id)

    def check_worktree_exists(self):
        """检查 worktree 是否已存在"""
        try:
            result = subprocess.run([
                "git", "-C", str(self.repo_path),
                "worktree", "list", "--porcelain"
            ], capture_output=True, text=True, check=True)

            for line in result.stdout.strip().split('\n'):
                if line.startswith('worktree ') and str(self.worktree_path) in line:
                    return True
            return False
        except subprocess.CalledProcessError:
            return False

    def check_branch_exists(self, branch_name):
        """检查分支是否已存在（本地或远程）"""
        try:
            # 检查本地分支
            result = subprocess.run([
                "git", "-C", str(self.repo_path),
                "branch", "--list", branch_name
            ], capture_output=True, text=True, check=True)

            if result.stdout.strip():
                return True

            # 检查远程分支
            result = subprocess.run([
                "git", "-C", str(self.repo_path),
                "branch", "--list", "-r", f"origin/{branch_name}"
            ], capture_output=True, text=True, check=True)

            return bool(result.stdout.strip())
        except subprocess.CalledProcessError:
            return False

    def get_current_branch(self, repo_path=None):
        """获取当前分支名"""
        try:
            target_path = repo_path or self.repo_path
            result = subprocess.run([
                "git", "-C", str(target_path),
                "branch", "--show-current"
            ], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def create_worktree_and_branch(self):
        """创建 worktree 并生成新分支"""
        try:
            # 1. 检查 worktree 是否已存在
            if self.check_worktree_exists():
                print(f"[信息] Worktree 已存在: {self.worktree_path}")
                current_branch = self.get_current_branch(self.worktree_path)
                if current_branch == self.new_branch:
                    print(f"[成功] 已在目标分支: {self.new_branch}")
                    return
                else:
                    print(f"[信息] 当前分支: {current_branch}，切换到: {self.new_branch}")
                    if self.check_branch_exists(self.new_branch):
                        subprocess.run([
                            "git", "-C", str(self.worktree_path),
                            "checkout", self.new_branch
                        ], check=True)
                        print(f"[成功] 已切换到分支: {self.new_branch}")
                    else:
                        subprocess.run([
                            "git", "-C", str(self.worktree_path),
                            "checkout", "-b", self.new_branch, self.base_branch
                        ], check=True)
                        print(f"[成功] 已创建并切换到新分支: {self.new_branch}")
                    return

            # 2. 基础分支是否在主仓库被 checkout
            current_branch_at_main = self.get_current_branch(self.repo_path)
            if current_branch_at_main == self.base_branch:
                print(f"[信息] 基础分支 {self.base_branch} 已在主仓库检出")
                print("[信息] 使用分离 HEAD 创建 worktree ...")

                self.worktree_path.parent.mkdir(parents=True, exist_ok=True)

                result = subprocess.run([
                    "git", "-C", str(self.repo_path),
                    "rev-parse", self.base_branch
                ], capture_output=True, text=True, check=True)
                commit_hash = result.stdout.strip()

                cmd = [
                    "git", "-C", str(self.repo_path),
                    "worktree", "add", str(self.worktree_path), commit_hash
                ]
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                print(f"[成功] 已创建 worktree: {self.worktree_path}")
            else:
                self.worktree_path.parent.mkdir(parents=True, exist_ok=True)

                cmd = [
                    "git", "-C", str(self.repo_path),
                    "worktree", "add", str(self.worktree_path), self.base_branch
                ]
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                print(f"[成功] 已创建 worktree: {self.worktree_path}")

            # 3. 在 worktree 中创建/切换分支
            if self.check_branch_exists(self.new_branch):
                print(f"[信息] 分支 {self.new_branch} 已存在，切换中...")
                subprocess.run([
                    "git", "-C", str(self.worktree_path),
                    "checkout", self.new_branch
                ], check=True)
                print(f"[成功] 已切换到分支: {self.new_branch}")
            else:
                subprocess.run([
                    "git", "-C", str(self.worktree_path),
                    "checkout", "-b", self.new_branch
                ], check=True)
                print(f"[成功] 已创建新分支: {self.new_branch}")

        except subprocess.CalledProcessError as e:
            print(f"[错误] 创建 worktree/分支失败: {e.stderr if e.stderr else str(e)}")
            raise

    def git_commit_and_push(self, commit_message):
        """使用 GITLAB_TOKEN 提交并推送"""
        try:
            subprocess.run([
                "git", "-C", str(self.worktree_path),
                "config", "user.name", "HC AI Assistant"
            ], check=True)
            subprocess.run([
                "git", "-C", str(self.worktree_path),
                "config", "user.email", "huangcan@mokahr.com"
            ], check=True)

            subprocess.run([
                "git", "-C", str(self.worktree_path),
                "add", "."
            ], check=True)

            subprocess.run([
                "git", "-C", str(self.worktree_path),
                "commit", "-m", commit_message
            ], check=True)
            print(f"[成功] 已提交: {commit_message}")

            remote_url = f"https://oauth2:{self.gitlab_token}@{self.gitlab_url.replace('https://', '')}/{self.project.path_with_namespace}.git"
            subprocess.run([
                "git", "-C", str(self.worktree_path),
                "remote", "set-url", "origin", remote_url
            ], check=True)

            subprocess.run([
                "git", "-C", str(self.worktree_path),
                "push", "-u", "origin", self.new_branch
            ], check=True)
            print(f"[成功] 已推送分支: {self.new_branch}")

        except subprocess.CalledProcessError as e:
            print(f"[错误] Git 操作失败: {e}")
            raise

    def create_merge_request(self, title, description="", target_branch="main"):
        """创建合并请求"""
        try:
            mr = self.project.mergerequests.create({
                'source_branch': self.new_branch,
                'target_branch': target_branch,
                'title': title,
                'description': description
            })
            print(f"[成功] 已创建合并请求: {mr.web_url}")
            return mr.web_url
        except Exception as e:
            print(f"[错误] 创建合并请求失败: {e}")
            raise

    def cleanup_worktree(self, force=False):
        """清理 worktree"""
        try:
            if not self.check_worktree_exists():
                print(f"[信息] Worktree 不存在: {self.worktree_path}")
                return

            cmd = [
                "git", "-C", str(self.repo_path),
                "worktree", "remove", str(self.worktree_path)
            ]
            if force:
                cmd.append("--force")

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"[成功] 已清理 worktree: {self.worktree_path}")
            else:
                if not force:
                    print("[警告] 普通清理失败，尝试强制清理...")
                    self.cleanup_worktree(force=True)
                else:
                    print(f"[错误] 强制清理失败: {result.stderr}")
                    if self.worktree_path.exists():
                        import shutil
                        shutil.rmtree(self.worktree_path, ignore_errors=True)
                        print(f"[成功] 已手动删除目录: {self.worktree_path}")

                        subprocess.run([
                            "git", "-C", str(self.repo_path),
                            "worktree", "prune"
                        ], capture_output=True)
                        print("[成功] 已清理 worktree 记录")

        except Exception as e:
            print(f"[错误] 清理 worktree 出错: {e}")


def submitMergeRequestForOptimizeSlowSqlByFixSuggest(input_json):
    """
    :param input_json:{
        need_fix_project_name
        new_branch_name
        base_branch_name
        fix_info
    }
    :return: mr_url
    """
    project_info_map = {
        "hcm-workflow-platform-web": {"project_id": 944,
                                      "local_repo_path": "/Users/moka/IdeaProjects/PaProjects/hcm-workflow-platform-web"},
        "hcm-workflow-platform-core": {"project_id": 981,
                                       "local_repo_path": "/Users/moka/IdeaProjects/PaProjects/hcm-workflow-platform-core"},
        "hcm-workflow-form-platform": {"project_id": 896,
                                       "local_repo_path": "/Users/moka/IdeaProjects/PaProjects/hcm-workflow-form-platform"},
        "hcm-workflow-process-platform": {"project_id": 1000,
                                          "local_repo_path": "/Users/moka/IdeaProjects/PaProjects/hcm-workflow-process-platform"},
        "hcm-workflow-platform-access": {"project_id": 1125,
                                         "local_repo_path": "/Users/moka/IdeaProjects/PaProjects/hcm-workflow-platform-access"}
    }

    input = json.loads(input_json)

    need_fix_project_name = input["need_fix_project_name"]
    repo_path = project_info_map.get(need_fix_project_name).get("local_repo_path")
    project_id = project_info_map.get(need_fix_project_name).get("project_id")

    new_branch_name = input["new_branch_name"]
    base_branch_name = input["base_branch_name"]
    pr_builder = BuildPullRequest(repo_path, project_id, base_branch_name, new_branch_name)

    fix_info = input["fix_info"]
    try:
        # 1. 创建worktree和分支
        pr_builder.create_worktree_and_branch()

        # 2. 使用Claude进行智能代码修复
        print("[信息] 开始使用Claude进行代码修复...")
        fix_info_json = json.dumps(fix_info, ensure_ascii=False)
        worktree_path = str(pr_builder.worktree_path)

        askClaudeFixCodeFileByFixInfo(fix_info_json, worktree_path)
        print(f"[成功] Claude已完成代码修复")

        # 3. 提交和推送
        reason = fix_info.get("reason", "AI代码修复")
        commit_message = f"fix: {reason}\n\n🤖 Generated with Claude AI Assistant"
        pr_builder.git_commit_and_push(commit_message)

        # 4. 创建MR
        fix_suggest = fix_info.get("fix_suggest", "")
        mr_title = f"🤖 AI代码修复: {reason[:50]}{'...' if len(reason) > 50 else ''}"
        mr_description = f"""## 🤖 AI自动代码修复

            **问题原因：**
            {reason}
            
            **修复建议：**
            {fix_suggest}
            
            **目标服务：**
            {fix_info.get("error_server", "unknown")}
            
            ---
            *此MR由AI自动生成和修复*
        """
        mr_url = pr_builder.create_merge_request(
            title=mr_title,
            description=mr_description,
            target_branch=base_branch_name
        )
        return mr_url

    except Exception as e:
        print(f"[错误] 流程失败: {e}")

    finally:
        try:
            pr_builder.cleanup_worktree()
        except Exception as cleanup_error:
            print(f"[警告] 清理 worktree 失败: {cleanup_error}")


submitMergeRequestForOptimizeSlowSqlByFixSuggestTool = Tool(
    name="submitMergeRequestForOptimizeSlowSqlByFixSuggestTool",
    func=submitMergeRequestForOptimizeSlowSqlByFixSuggest,
    description="根据修复建议提交MR"
)

if __name__ == "__main__":
    input_json = """
    {
        "need_fix_project_name": "hcm-workflow-platform-access",
        "new_branch_name": "hc-ai/fix/issue-id-21520265",
        "base_branch_name": "release",
        "fix_info": {
            "reason": "com/moka/workflow/platform/access/composite/message/handler/impl/digest/impl/GoOutDigestAdapter.java:69因为formDefDataDTO为NULL导致发生了空指针异常",
            "fix_suggest": "在com/moka/workflow/platform/access/composite/message/handler/impl/digest/impl/GoOutDigestAdapter.java:69前增加「if (Objects.isNull(formDefDataDTO)) {return goOutDigestSingleModelHandler.doGetDigestFieldWithData(calReq);}」",
            "error_server": "hcm-workflow-platform-access"
        }
    }
    """
    mr_url = submitMergeRequestForOptimizeSlowSqlByFixSuggest(input_json)
    print("submitMergeRequestForOptimizeSlowSqlByFixSuggestTool返回结果：\n")
    print(mr_url)
