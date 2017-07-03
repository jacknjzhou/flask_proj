#!-*-encoding:utf8-*-

"""
@function:包装执行git获取分支文件更新内容的逻辑
"""
import traceback

from mgr_host import extra_config
from mgr_host import file_opt


class GitCmd(object):
    def __init__(self):
        pass

    def list_branch_list(self, module="", relative_dir=""):
        """function:列出指定分支目录下的文件夹/文件"""
        try:
            git_path = extra_config.module_git_path_conf.get(module)
            info_list, msg = file_opt.local_list_dir_info(git_path, relative_dir)
            result = True

        except Exception as e:
            print traceback.format_exc()
            msg = str(e)
            result = False
        return result, info_list, msg

    def fetch_branch_name_list(self,module=""):
        """function:获取指定项目的分支列表"""

        def _parse_resp(r_info=""):
            """对执行的命令返回的结果串进行解析"""
            try:
                r_list = [item.strip() for item in r_info.split('\n')]
                r_list = list(set([item.strip('*').strip().split('/')[-1] for item in r_list]))
                return r_list

            except Exception as e:
                print str(e)
                print traceback.format_exc()
                return []

        try:
            result = True
            r_list = []
            msg = "OK"
            if not module:
                result =False
                msg = "[GitCmd][fetch_branch_name_list]input info error,module info is null."
                return result, r_list, msg
            #需执行的命令
            git_cmd = "git fetch;git branch -a"
            #执行的路径
            git_path = extra_config.module_git_path_conf.get(module)
            if not git_path:
                result = False
                msg = "[GitCmd][fetch_branch_name_list]can not get module [%s] local git path config info." % (git_path,)
                return result, r_list, msg
            #组合并执行命令(若是新建分支,现在执行)
            #cmd_str = "cd %s;git fetch " % (git_path, git_cmd)
            #result, msg = file_opt.local_cmd_opt(cmd_str)

            cmd_str = "cd %s;%s" % (git_path, git_cmd)
            result, msg = file_opt.local_cmd_opt(cmd_str)
            #解析返回的结果
            if result:
                r_list = _parse_resp(msg)

        except Exception as e:
            print traceback.format_exc()
            msg = str(e)
            result = False
        return result, r_list, msg

    def fetch_branch_update(self, module="",branch=""):
        """function:获取指定模块/环境 分支下的文件更新"""
        try:
            result = True
            msg = "OK"
            if not module:
                result = False
                msg = "[GitCmd][fetch_branch_update]input info error,module info is null."
                return result, msg
            # 获取设设定的分支需要执行的命令(如果输入分支名字,则按照此分支去进行更新,否则按照默认配置去做update)
            if not branch:
                git_cmd = extra_config.branch_cmd_info.get(extra_config.branch_info)
            else:
                git_cmd = extra_config.freedom_branch_cmd_info.format(**{"branch":branch})

            # fetch git path
            git_path = extra_config.module_git_path_conf.get(module)
            if not git_path:
                result = False
                msg = "[GitCmd][fetch_branch_update]can not get module [%s] local git path config info." % (git_path,)
                return result, msg
            # git command str
            cmd_str = "cd %s;%s" % (git_path, git_cmd)
            result, msg = file_opt.local_cmd_opt(cmd_str)

        except Exception as e:
            print traceback.format_exc()
            msg = str(e)
            result = False
        return result, msg
