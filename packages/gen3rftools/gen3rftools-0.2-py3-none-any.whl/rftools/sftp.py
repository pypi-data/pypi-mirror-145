import paramiko


class SftpConnection:
    def __init__(self, hostname: str, username: str, password: str, port: int):
        """
        :param hostname: ip地址
        :param username: 用户名
        :param password: 密码
        :param port: 端口号
        """
        self._transport = paramiko.Transport((hostname, port))
        self._transport.connect(username=username, password=password)
        self._sftp = paramiko.SFTPClient.from_transport(self._transport)

    def get_file(self, remote_path: str, local_path: str):
        """
        下载文件
        :param remote_path: 远程主机文件目录
        :param local_path: 本地主机文件目录
        :return:
        """
        self._sftp.get(remote_path, local_path)

    def upload_file(self, local_path: str, remote_path: str):
        """
        上传文件
        :param local_path: 本地主机文件目录
        :param remote_path: 远程主机文件目录
        :return:
        """
        self._sftp.put(local_path, remote_path)

    def mkdir(self, remote_path: str):
        """
        创建文件夹
        :param remote_path: 远程主机文件夹目录
        :return:
        """
        self._sftp.mkdir(remote_path)

    def rename(self, remote_old_path: str, remote_new_path: str):
        """

        :param remote_old_path:
        :param remote_new_path:
        :return:
        """
        self._sftp.rename(remote_old_path, remote_new_path)

    def close(self):
        self._sftp.close()
