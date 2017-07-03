#!-*-coding:utf8-*-
"""
function:执行增量代码发布
"""
from mgr_host import extra_config
from mgr_host import file_opt
#from mgr_host.remote_opt import RemoteOpt
from mgr_host.nopwd_remote_opt import NopwdRemote


class CodePublish(object):

    def __init__(self):
        pass

    def cache_selected_file(self, module_info="", selected_file_list=[]):
        """指定的模块文件进行缓存(并进行按照层级进行压缩)"""
        #
        if not module_info:
            msg = "[CodePublish][cache_selected_file]no input module info,return"
            result = False
            return result, msg
        src_dir = extra_config.module_git_path_conf.get(module_info)
        if not src_dir:
            result = False
            msg = "[CodePublish][cache_selected_file]can not find module [%s] local dir" % (src_dir,)
            return result, msg
        #
        dest_dir = extra_config.module_cache_dir_conf.get(module_info)
        if not dest_dir:
            result = False
            msg = "[CodePublish][cache_selected_file]can not find module [%s] cache dir" % (dest_dir,)
            return result, msg
        # step-1:reset cache dir
        result, msg = file_opt.local_tmp_dir_reset(dest_dir)
        if not result:
            return result, msg
        # step-2:copy file foreach
        if not selected_file_list:
            result = False
            msg = "[CodePublish][cache_selected_file]no input file info.return"
            return result, msg
        for item in selected_file_list:
            if item:
                (result, msg) = file_opt.local_copy_tree_file(src_dir, item, dest_dir)
                if not result:
                    return result, msg
        #step-3:tar file => tar.gz
        result, msg = file_opt.local_tar_tree_file(dest_dir,module_info)
        return result, msg

    def publish_selected_file(self,module_info="",ip_list =[]):
        """function:对已经打包的选择文件进行上传"""
        #step-1:fetch upload ip info
        if ip_list:
            dest_ip_list  = [ip_list] if isinstance(ip_list,(unicode,str)) else ip_list
        else:
            dest_ip_list = extra_config.module_deploy_ip_conf.get(module_info)
            if not dest_ip_list:
                msg = "[CodePublish][publish_selected_file]can not find module [%s] deploy ip info."%(module_info,)
                result = False
                return result, msg

        dest_deploy_dir = extra_config.module_deploy_dir_conf.get(module_info)
        if not dest_deploy_dir:
            result = False
            msg = "[CodePublish][publish_selected_file]can not find module [%s] dest deploy dir config info"%(module_info,)

        local_tar_dir = extra_config.module_cache_dir_conf.get(module_info)
        if not local_tar_dir:
            result = False
            msg = "[CodePublish][publish_selected_file]can not find module [%s] local cache dir config info"%(module_info,)
            return result, msg

        #step-2:
        for ip in dest_ip_list:
            #step-2-1:fetch ip basic info
            basic_info = extra_config.host_basic_conf.get(ip)
            if not basic_info:
                msg = "[CodePublish][publish_selected_file]can not find ip [%s] basic config info."%(ip)
                result = False
                return result, msg
            #re_obj = RemoteOpt(ip,basic_info.get("port"),
            #                   basic_info.get("name"),basic_info.get("pwd"))
            re_obj = NopwdRemote(ip,basic_info.get("port"),
                                 basic_info.get("name"),basic_info.get("pkey"))
            #step-2-2:upload cache file to remote ip
            result, msg = re_obj.upload_file(local_tar_dir+module_info+'.tar.gz',dest_deploy_dir+module_info+'.tar.gz')
            if not result:
                print "[CodePublish][publish_selected_file]upload file [%s.tar.gz] to [%s] fail"%(module_info,ip)
                return result, msg
            #step-2-3:unzip tar file
            cmd_str = "cd %s;tar zxf %s.tar.gz;"%(dest_deploy_dir,module_info)
            result, msg, error = re_obj.exe_command(cmd_str)
            if not result:
                return result,msg+error

        return True, "OK"