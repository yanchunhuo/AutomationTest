#!-*- coding:utf8 -*-
import os
import paramiko

class SSHClient:
    def __init__(self,ip,username='root',port=22,password='Hstest2014'):
        self._ip=ip
        self._port=port
        self._username=username
        self._password=password
        self._setSSHClient()

    def _setSSHClient(self):
        self._sshclient = paramiko.SSHClient()
        self._sshclient.load_system_host_keys()
        self._sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self._sshclient.connect(hostname=self._ip, port=self._port, username=self._username, password=self._password)

        sftp = paramiko.Transport(self._ip+':'+str(self._port))
        sftp.connect(username=self._username, password=self._password)
        self._sftpclient = paramiko.SFTP.from_transport(sftp)

    def _getSSHClient(self):
        return self._sshclient

    def _getSFTPClient(self):
        return self._sftpclient

    def ssh_exec_command(self,command,timeout=60,is_source_profile=1):
        if int(is_source_profile)==1:
            command='source /etc/profile;'+command
        stdin, stdout, stderr=self._sshclient.exec_command(command=command,timeout=timeout)
        channel = stdout.channel
        exit_code = channel.recv_exit_status()
        return stdin, stdout, stderr, exit_code

    def sftp_get(self,remote_path,local_path):
        self._sftpclient.get(remote_path,local_path)

    def sftp_put(self, local_path, remote_path):
        self._sftpclient.put(local_path, remote_path)

    def _get_all_files_in_local_path(self, local_path):
        all_files = []
        files = os.listdir(local_path)
        for x in files:
            filename = os.path.join(local_path, x)
            if os.path.isdir(filename):
                all_files.extend(self._get_all_files_in_local_path(filename))
            else:
                all_files.append(filename)
        return all_files

    def sftp_put_dir(self, local_path, remote_path):
        if remote_path[-1] == '/':
            remote_path = remote_path[0:-1]
        all_files = self._get_all_files_in_local_path(local_path)
        for x in all_files:
            filename = os.path.split(x)[-1]
            remote_filename = remote_path + '/' + filename
            self._sftpclient.put(x, remote_filename)

    def closeSSHAndSFTP(self):
        self._sshclient.close()
        self._sftpclient.close()

