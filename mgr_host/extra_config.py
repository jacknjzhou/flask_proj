#!-*-encoding:utf8-*-
"""
@ function:config extra info for support command line.
"""

"""function:define fetch code /which branch"""
branch_info = 'develop'

"""function:固定的方式"""
branch_cmd_info = {
    "develop": "git checkout develop;git pull",
    "master": "git checkout master;git pull"
}
"""functio:满足迁出不同分支的需求"""
freedom_branch_cmd_info = "git checkout {branch};git pull"


"""function:所有已经配置过相关信息的模块列表,供接口使用,前端展示"""
module_conf_list = ["oss_config_api","oss_log_api","oss_log_svr","oss_trans",
                    "oss_web","oss_push_svr","webadmin","oss_notify_api",
                    "oss_notify_svr"]

"""function:模块本地git所处路径目录"""
module_git_path_conf = {
    "oss_config_api": "/Volumes/data/gitProj/OSS_Config_API/",
    "oss_config_svr": "/Volumes/data/gitProj/OSS_Config_Svr/",
    "oss_log_api": "/Volumes/data/gitProj/OSS_Log_API/",
    "oss_log_svr": "/Volumes/data/gitProj/OSS_Log_Svr/",
    "oss_trans": "/Volumes/data/gitProj/OSS_Trans/",
    "oss_web": "/Volumes/data/gitProj/OSS_Web/",
    "oss_push_svr": "/Volumes/data/gitProj/OSS_Push_Svr/",
    "webadmin": "/Volumes/data/gitProj/webadmin/",
    "oss_notify_api": "/Volumes/data/gitProj/OSS_Notify_API/",
    "oss_notify_svr": "/Volumes/data/gitProj/OSS_Notify_Svr/"
}

"""function:模块所部署设备IP"""
module_deploy_ip_conf = {
    "oss_config_api": ["127.0.0.1"],
    "oss_config_svr": ["127.0.0.1"],
    "oss_log_api": ["127.0.0.1"],
    "oss_log_svr": ["127.0.0.1"],
    "oss_trans": ["127.0.0.1"],
    "oss_web": ["127.0.0.1"],
    "oss_push_svr": ["127.0.0.1"],
    "webadmin": ["127.0.0.1"],
    "oss_notify_api": ["127.0.0.1"],
    "oss_notify_svr": ["127.0.0.1"]
}

"""function:模块部署设备所在目录"""
module_deploy_dir_conf = {
    "oss_config_api": "/opt/OSS/OSS_Config_API/",
    "oss_config_svr": "/opt/OSS/OSS_Config_Svr/",
    "oss_log_api": "/opt/OSS/OSS_Log_API/",
    "oss_log_svr": "/opt/OSS/OSS_Log_Svr/",
    "oss_trans": "/opt/OSS/OSS_Trans/",
    "oss_web": "/opt/OSS/OSS_Web/",
    "oss_push_svr": "/opt/OSS/OSS_Push_Svr",
    "webadmin": "/opt/OSS/webadmin/",
    "oss_notify_api": "/opt/OSS/OSS_Notify_API/",
    "oss_notify_svr": "/opt/OSS/OSS_Notify_Svr/"
}

"""function:增量发布时的临时缓存目录"""
module_cache_dir_conf = {
    "oss_config_api": "/tmp/OSS/OSS_Config_API/",
    "oss_config_svr": "/tmp/OSS/OSS_Config_Svr/",
    "oss_log_api": "/tmp/OSS/OSS_Log_API/",
    "oss_log_svr": "/tmp/OSS/OSS_Log_Svr/",
    "oss_trans": "/tmp/OSS/OSS_Trans/",
    "oss_web": "/tmp/OSS/OSS_Web/",
    "oss_push_svr": "/tmp/OSS/OSS_Push_Svr",
    "webadmin": "/tmp/OSS/webadmin/",
    "oss_notify_api": "/tmp/OSS/OSS_Notify_API/",
    "oss_notify_svr": "/tmp/OSS/OSS_Notify_Svr/"
}

"""function:host basic info config"""
host_basic_conf = {
    "127.0.0.1": {
        "port": 2222,
        "name": "vagrant",
        "pwd": "",
        "pkey":"/Users/jackyzhou/.ssh/id_rsa"
    }
}
