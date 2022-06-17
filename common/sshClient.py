#!-*- coding:utf8 -*-
# 作者 yanchunhuo
# 创建时间 2018/01/19 22:36
# github https://github.com/yanchunhuo

import os
import paramiko
import stat

class SSHClient:
    def __init__(self,ip,username,port=22,password=None,is_windows=False,pkey_file=None):
        self.ip=ip
        self.port=port
        self.username=username
        self.password=password
        self.is_windows=is_windows
        self.pkey_file=pkey_file
        self._setSSHClient()

    def _setSSHClient(self):
        self.sshclient = paramiko.SSHClient()
        self.sshclient.load_system_host_keys()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        if self.pkey_file:
            key=paramiko.RSAKey.from_private_key_file(self.pkey_file)
            self.sshclient.connect(hostname=self.ip, port=self.port, username=self.username, pkey=key)
            sftp = paramiko.Transport(self.ip+':'+str(self.port))
            sftp.connect(username=self.username,pkey=key)
        else:
            self.sshclient.connect(hostname=self.ip, port=self.port, username=self.username, password=self.password)
            sftp = paramiko.Transport(self.ip+':'+str(self.port))
            sftp.connect(username=self.username, password=self.password)
        self.sftpclient = paramiko.SFTP.from_transport(sftp)

    def ssh_exec_command(self,command,timeout=60,is_source_profile=1):
        if int(is_source_profile)==1 and not self.is_windows:
            command='source /etc/profile;'+command
        stdin, stdout, stderr=self.sshclient.exec_command(command=command,timeout=timeout)
        channel = stdout.channel
        exit_code = channel.recv_exit_status()
        return stdin, stdout, stderr, exit_code

    def sftp_get(self,remote_path,local_path):
        self.sftpclient.get(remote_path,local_path)

    def sftp_put(self, local_path, remote_path):
        self.sftpclient.put(local_path, remote_path)

    def sftp_put_dir(self, local_dir_path, remote_dir_path):
        local_dir_path=local_dir_path.replace('\\','/')
        if not local_dir_path[-1] == '/':
            local_dir_path += '/'
        remote_dir_path=remote_dir_path.replace('\\','/')
        if not remote_dir_path[-1] == '/':
            remote_dir_path += '/'
        for dirpath,dirnames,filenames in os.walk(local_dir_path):
            dirpath=dirpath.replace('\\','/')
            if not dirpath[-1] == '/':
                dirpath += '/'                
            # 创建当前路径目录
            for dirname in dirnames:
                local_next_dirpath=dirpath+dirname
                remote_next_sub_dirpath=local_next_dirpath.replace(local_dir_path,'')
                if remote_next_sub_dirpath[0] == '/':
                    remote_next_sub_dirpath = remote_next_sub_dirpath[1:]
                if self.is_windows:
                    mkdir_remote_command='mkdir "%s"'%(remote_dir_path+remote_next_sub_dirpath)
                else:
                    mkdir_remote_command='mkdir -p "%s"'%(remote_dir_path+remote_next_sub_dirpath)
                stdin,stdout,stderr,exit_code=self.ssh_exec_command(mkdir_remote_command)
                if not exit_code == 0:
                    if self.is_windows:
                        raise Exception(stderr.read().decode('gbk'))
                    else:
                        raise Exception(stderr.read().decode('utf-8'))
            #上传当前路径文件
            for filename in filenames:
                remote_sub_dirpath=dirpath.replace(local_dir_path,'')
                remote_sub_dirpath=remote_sub_dirpath.replace('\\','/')
                if len(remote_sub_dirpath)>0:
                    if remote_sub_dirpath[0] == '/':
                        remote_sub_dirpath = remote_sub_dirpath[1:]
                    if not remote_sub_dirpath[-1] == '/':
                        remote_sub_dirpath+='/'
                else:
                    remote_sub_dirpath='/'
                self.sftpclient.put(local_dir_path+remote_sub_dirpath+filename,remote_dir_path+remote_sub_dirpath+filename)

    def sftp_get_dir(self, remote_dir_path, local_dir_path):
        local_dir_path=local_dir_path.replace('\\','/')
        if not local_dir_path[-1] == '/':
            local_dir_path += '/'
        remote_dir_path=remote_dir_path.replace('\\','/')
        if not remote_dir_path[-1] == '/':
            remote_dir_path += '/'
        remote_dir_files=self.sftpclient.listdir_attr(remote_dir_path)
        for remote_file in remote_dir_files:
            if stat.S_ISDIR(remote_file.st_mode):
                self.sftp_get_dir(remote_dir_path=remote_dir_path+remote_file.filename+'/',
                                  local_dir_path=local_dir_path+remote_file.filename+'/')
            else:
                if not os.path.exists(local_dir_path):
                    os.makedirs(local_dir_path)
                self.sftp_get(remote_dir_path+remote_file.filename,local_dir_path+remote_file.filename)

    def closeSSHAndSFTP(self):
        self.sshclient.close()
        self.sftpclient.close()