#!-*-coding:utf8-*-
"""
@function:对指定的文件进行copy,并保留原始的目录结构
@ srcDir  '/Volumes/data/devProj/OSS_Push_Svr/'  对应模块所在目录
@ srcFile   'mgr_host/file_opt.py' 模块主目录开始 的文件 相对路径
@ destFile  'mgr_host/file_opt.py'
@ destDir '/tmp/module_name_%s/'%(time.time())   模块所属临时目录
"""
import commands
import os
import shutil
import traceback


def local_tmp_dir_reset(destDir=""):
    """function:清空本地作为缓存的文件夹"""
    try:
        result = True
        msg = "OK"
        print "start reset local temp dir [%s]" % (destDir)
        shutil.rmtree(destDir)
        os.makedirs(destDir)
    except OSError as e:
        print "not exist dir[%s],create it" % (destDir,)
        os.makedirs(destDir)
    except Exception as e:
        print traceback.format_exc()
        msg = str(e)
        result = False
    return result, msg


def local_copy_tree_file(srcDir="/tmp/", srcFile="", destDir="/tmp/"):
    """function:在本地指定 保持目录结构进行copy文件"""
    try:
        result = True
        msg = "OK"
        relative_dir_info, file_name = os.path.split(srcFile)
        dest_path = os.path.join(destDir, relative_dir_info)
        print "start check dest path [%s] exist..." % (dest_path)
        if not os.path.exists(dest_path):
            print "create dest path [%s]..." % (dest_path)
            os.makedirs(dest_path)
        print "start local copy file [%s]..." % (srcFile)
        shutil.copy(os.path.join(srcDir, srcFile), dest_path)
    except Exception as e:
        print traceback.format_exc()
        msg = str(e)
        result = False
    return result, msg


def local_tar_tree_file(destDir="", tar_file_name=""):
    """function:对本地/本次所copy的文件进行压缩"""
    try:
        result = True
        msg = "OK"
        status, r_output = commands.getstatusoutput('cd %s;tar zcvf %s.tar.gz *' % (destDir, tar_file_name))
        print r_output
        if status != 0:
            result = False
            msg = "tar file fail."

    except Exception as e:
        msg = str(e)
        print traceback.format_exc()
        result = False
    return result, msg


def local_cmd_opt(cmd_str):
    """function:执行本地命令"""
    try:
        result = True
        msg = "OK"
        print cmd_str
        status, r_output = commands.getstatusoutput(cmd_str)
        if status != 0:
            print "local execute commands fail."
            msg = r_output
            result = False
        else:
            msg = r_output

    except Exception as e:
        print traceback.format_exc()
        msg = str(e)
        result = False
    return result, msg


def local_list_dir_info(init_dir="/tmp/", relative_dir=""):
    """function:列出本地指定目录所辖的文件夹/文件列表"""
    try:
        info = []
        # step-1:
        # 分别为 主目录,子目录列表,文件列表
        dn, dns, fns = os.walk(init_dir + relative_dir).next()
        tmp = {}
        tmp['curDir'] = relative_dir
        tmp['subDir'] = [relative_dir +'/'+ item for item in dns]
        tmp['fileList'] = [relative_dir +'/'+ item for item in fns]

        info.append(tmp)
        msg = "OK"

    except Exception as e:
        print traceback.format_exc()
        info = []
        msg = str(e)
    return info, msg


if __name__ == '__main__':
    local_tmp_dir_reset('/tmp/dest_test/')
    local_copy_tree_file('/tmp/', 'test1/test2/test3/test4/test5/test.php', '/tmp/dest_test/')
    local_copy_tree_file('/tmp/', 'test1/test2/test.php', '/tmp/dest_test/')
    local_tar_tree_file('/tmp/dest_test/', 'dest_test')
