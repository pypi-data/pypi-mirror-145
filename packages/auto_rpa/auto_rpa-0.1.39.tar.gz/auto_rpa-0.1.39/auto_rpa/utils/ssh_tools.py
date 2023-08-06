import paramiko
import os

def upload_to_server(server_ip, user_name, user_pass, local_dir, remote_dir):

    """
    上传文件到服务器
    :param server_ip: str
    :param user_name: str
    :param user_pass: str
    :param local_path: str
    :param remote_path: str
    :return:
    """

    remote_dir = remote_dir.replace('\\', '/')
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(server_ip, 22, user_name, user_pass)
    s.exec_command('mkdir -p ' + remote_dir)
    file_list = os.listdir(local_dir)
    for file_name in file_list:
        local_path = os.path.join(local_dir, file_name)
        remote_path = os.path.join(remote_dir, file_name)
        remote_path = remote_path.replace('\\', '/')
        sftp = paramiko.SFTPClient.from_transport(s.get_transport())
        sftp.put(local_path, remote_path)
    s.close()