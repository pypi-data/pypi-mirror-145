# -*- coding: utf-8 -*-
# ftp相关命令操作
# ftp.cwd(pathname)                 #设置FTP当前操作的路径
# ftp.dir()                         #显示目录下所有目录信息
# ftp.nlst()                        #获取目录下的文件
# ftp.mkd(pathname)                 #新建远程目录
# ftp.pwd()                         #返回当前所在位置
# ftp.rmd(dirname)                  #删除远程目录
# ftp.delete(filename)              #删除远程文件
# ftp.rename(fromname, toname)#将fromname修改名称为toname。
# ftp.storbinaly("STOR filename.txt",file_handel,bufsize)  #上传目标文件
# ftp.retrbinary("RETR filename.txt",file_handel,bufsize)  #下载FTP文件

import os
from ftplib import FTP

class FtpClient():

    def __init__(self,ip,user,passwd):
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.connect()

    def connect(self):

        ftp = FTP()
        ftp.encoding = 'gbk'
        ftp.set_debuglevel(0)
        ftp.connect(self.ip)
        ftp.login(self.user, self.passwd)
        print(ftp.getwelcome())
        print('当前目录:{}'.format(ftp.pwd()))
        self.ftp = ftp

    def check_remote_path_valid(self, remote_path):

        if remote_path is None or remote_path == '':
            raise Exception('该远程路径不合法，远程路径根目录不能为空')
        if remote_path[0] != '/':
            raise Exception('该远程路径不合法，远程路径根目录为/')
        return True

    def check_remote_path_exists(self,remote_path):

        try:
            self.ftp.nlst(remote_path)
            return True
        except:
            return False

    def check_remote_path_is_dir(self, remote_path):

        file_list = self.ftp.nlst(remote_path)
        if len(file_list) == 1:
            try:
                self.ftp.nlst(file_list[0])
            except:
                return False
        return True

    def rm_dir(self,remote_path):

        if self.check_remote_path_is_dir(remote_path):
            for file_path in self.ftp.nlst(remote_path):
                if self.check_remote_path_is_dir(file_path):
                    self.rm_dir(file_path)
                else:
                    self.ftp.delete(file_path)

    def upload_file(self, local_path, remote_path):

        '''

        @param local_path: 本地文件
        @param remote_path: 远程文件
        @return:
        '''

        bufsize = 1024
        if not os.path.exists(local_path):
            raise Exception('{}本地文件不存在'.format(local_path))
        try:
            fp = open(local_path, 'rb')
            self.ftp.storbinary('STOR {}'.format(remote_path), fp, bufsize)
            if not self.check_remote_path_exists(remote_path):
                raise Exception('文件不存在')
            fp.close()
        except Exception as e:
            raise Exception('{}-上传失败:{}'.format(local_path,str(e)))
        print('{}上传成功，关闭连接'.format(local_path))

    def download_file(self, local_path, remote_path):

        bufsize = 1024
        try:
            fp = open(local_path, 'wb')
            self.ftp.retrbinary('RETR ' + remote_path, fp.write, bufsize)
            if not os.path.exists(local_path):
                raise Exception('文件不存在')
            fp.close()
        except Exception as e:
            raise Exception('{}-下载失败:{}'.format(remote_path,str(e)))

        print('{}下载成功，关闭连接'.format(remote_path))

    def upload_dir(self, local_dir, remote_dir, ex_file=[]):

        if not os.path.exists(local_dir):
            raise Exception('{}该本地路径不存在'.format(local_dir))

        self.check_remote_path_valid(remote_dir)
        if not self.check_remote_path_exists(remote_dir):
            self.ftp.mkd(remote_dir)

        for file_name in os.listdir(local_dir):
            if file_name in ex_file:
                continue
            tmp_local_path = os.path.join(local_dir, file_name)
            tmp_remote_path = os.path.join(remote_dir, file_name)
            if os.path.isdir(tmp_local_path):
                self.upload_dir(tmp_local_path,tmp_remote_path)
            else:
                self.upload_file(tmp_local_path, tmp_remote_path)
        pass

    def download_dir(self, local_dir, remote_dir):

        self.check_remote_path_valid(remote_dir)
        if not self.check_remote_path_exists(remote_dir):
            raise Exception('{}该远程路径不存在'.format(remote_dir))

        if not os.path.exists(local_dir):
            os.mkdir(local_dir)

        for file_path in self.ftp.nlst(remote_dir):
            file_name = file_path.split('/')[-1]
            tmp_local_path = os.path.join(local_dir, file_name)
            tmp_remote_path = file_path
            if self.check_remote_path_is_dir(tmp_remote_path):
                self.download_dir(tmp_local_path,tmp_remote_path)
            else:
                self.download_file(tmp_local_path, tmp_remote_path)


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='手动执行脚本，注意区分文件夹上传和文件上传参数不同')
    parser.add_argument('-ls', '--login_infos', type=str, default=None, help='ip-user-pawssd使用空格隔开，批量操作时多条登录信息使用,隔开', required=True, metavar='')
    parser.add_argument('-t', '--oprate_type', type=str, default=None, help='处理类型，up文件上传，dw文件下载，ups文件夹上传，dws文件夹下载',
                        required=True, metavar='',choices=['up','dw','ups','dws'])
    parser.add_argument('-l', '--local_path', type=str, default=None, help='文件夹，文件本地文件全路径，为文件时包括文件名', required=False, metavar='')
    parser.add_argument('-r', '--remote_path', type=str, default=None, help='文件夹，文件远程服务器文件全路径，为文件包括文件名', required=False, metavar='')
    args = parser.parse_args()

    login_infos = args.login_infos.split(',')
    oprate_type = args.oprate_type
    local_path = args.local_path
    remote_path = args.remote_path

    for login_info in login_infos:
        login_info = login_info.split('-')
        print('ftp服务器信息:ip:{},user:{},passwd{}'.format(login_info[0], login_info[1], login_info[2]))
        if len(login_info) != 3:
            raise Exception('服务器信息格式错误')
        else:
            ftp_client = FtpClient(login_info[0], login_info[1], login_info[2])
            if oprate_type == 'up':
                ftp_client.upload_file(local_path,remote_path)
            elif oprate_type == 'dw':
                ftp_client.download_file(local_path, remote_path)
            elif oprate_type == 'ups':
                ftp_client.upload_dir(local_path, remote_path)
            elif oprate_type == 'dws':
                ftp_client.download_dir(local_path, remote_path)
            else:
                raise Exception('未知的操作')

    # ftp_client = FtpClient(ip, user, passwd)
    # ftp_client.download_dir(local_path, remote_path)
    # ftp_client.ftp.close()




