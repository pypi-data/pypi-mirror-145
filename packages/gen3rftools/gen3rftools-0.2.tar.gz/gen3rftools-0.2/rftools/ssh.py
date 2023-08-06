import re
import time
from typing import Optional
import paramiko
from PyQt6.QtCore import pyqtSignal
import logging


class SshConnection:
    # 三种模式，内部使用
    COMMON = 1
    RFSW = 2
    AASHELL = 3

    def __init__(self, hostname: str, username: str, password: str, port: int,
                 logger: Optional[logging.Logger], sg: Optional[pyqtSignal] = None,
                 send_interval: float = 0.5, read_interval: float = 0.5):
        """
        :param hostname: ip地址
        :param username: 用户名
        :param password: 密码
        :param port: 端口号
        :param logger: log模块
        :param sg: 用于Qt信号发射，默认禁用
        :param send_interval: 命令发送间隔，默认为0.5s
        :param read_interval: 命令读取间隔，默认为0.5s
        """
        self.logger = logger
        self.send_interval = send_interval
        self.read_interval = read_interval
        self.sg = sg
        self._typ = SshConnection.COMMON
        self.cmd_list = []

        self._transport = paramiko.Transport((hostname, port))
        self._transport.connect(username=username, password=password)
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh._transport = self._transport
        self._channel = self._transport.open_session()
        self._channel.get_pty()
        self._channel.invoke_shell()
        self._read_until("toor4nsn@.+# ")

    def _read_until(self, endre: str) -> str:
        """
        通过寻找接收的协议数据中的尾标识符，获取完整的数据报文
        :param endre: 尾标识符的正则表达式
        :return: 返回的数据报文
        """
        total_out = ""
        while True:
            if self._channel.recv_ready():
                output = self._channel.recv(1024)
                total_out += output.decode("utf-8", "ignore").replace('\r', '')
                self.log(output.decode("utf-8", "ignore").replace('\r', ''))
            else:
                time.sleep(self.read_interval)
            if re.search(endre, total_out):
                break
        time.sleep(self.send_interval)
        return total_out

    def common_cmd(self, command: str) -> str:
        """
        普通命令
        :param command:
        :return:
        """
        if self._typ == SshConnection.RFSW:
            self._channel.send("exit \n")
            self._read_until("toor4nsn@.+# ")
        elif self._typ == SshConnection.AASHELL:
            self._channel.send("quit \n")
            self._read_until("toor4nsn@.+# ")
        self._typ = SshConnection.COMMON
        self._channel.send(command + " \n")
        return self._read_until("toor4nsn@.+# ")

    def rfsw_cmd(self, command: str) -> str:
        """
        rfsw命令
        :param command:
        :return:
        """
        if self._typ == SshConnection.COMMON:
            self._channel.send("rfsw_cli \n")
            self._read_until("rfsw> ")
        elif self._typ == SshConnection.AASHELL:
            self._channel.send("quit \n")
            self._channel.send("rfsw_cli \n")
            self._read_until("rfsw> ")
        self._typ = SshConnection.RFSW
        self._channel.send(command + " \n")
        return self._read_until("rfsw> ")

    def aashell_cmd(self, command: str) -> str:
        """
        aashell命令
        :param command:
        :return:
        """
        if self._typ == SshConnection.COMMON:
            self._channel.send("telnet localhost 15007 \n")
            self._read_until("AaShell> ")
        elif self._typ == SshConnection.RFSW:
            self._channel.send("exit \n")
            self._read_until("toor4nsn@.+# ")
            self._channel.send("telnet localhost 15007 \n")
            self._read_until("AaShell> ")
        self._typ = SshConnection.AASHELL
        self._channel.send(command + " \n")
        return self._read_until("AaShell> ")

    def reboot(self) -> None:
        """
        重启，注意重启后会失去连接
        :return:
        """
        if self._typ == SshConnection.AASHELL:
            self._channel.send("exit \n")
            self._read_until("toor4nsn@.+# ")
        else:
            self._channel.send("reboot \n")
        self.log("rebooting!... \n")

    def log(self, message: str) -> None:
        """
        存储日志，两种方式，logger或者pyqtSignal
        :param message:
        :return:
        """
        if self.logger is not None:
            self.logger.info(message)
        if self.sg is not None:
            self.sg.emit(message)

    def close(self):
        self._ssh.close()

    def load_cmd_file(self, file_path: str):
        """
        通过文本方式执行命令
        :param file_path:
        :return:
        """
        with open(file_path) as file:
            self.cmd_list = file.readlines()

    def send_by_file(self, param_dict: Optional[dict] = None,
                     start_mark: Optional[str] = None, stop_mark: Optional[str] = None,
                     common_prefix: str = "`", rfsw_prefix: str = "", aashell_prefix: str = "``") -> str:
        """
        可以指定执行起始标记符与截止标记符之间的命令行，默认为rfsw_cli模式
        关于标记符：
        start_mark如果为None或者找不到，则默认为文件开头
        stop_mark如果为None，则默认为下一个<xxx>，如果找不到，则默认为文件尾部
        :param param_dict: 传入字典进行format赋值
        :param start_mark: 起始标记符，默认<xxx>形式
        :param stop_mark: 截止标记符，默认<xxx>形式
        :param common_prefix: 通用命令符前缀为`
        :param rfsw_prefix: 通用命令符前缀为
        :param aashell_prefix: aashell命令符前缀为``
        :return: 最后一行命令的返回结果
        """
        res = ""
        start_row = 0
        stop_row = len(self.cmd_list)
        for index, cmd in enumerate(self.cmd_list):
            if cmd.strip() == start_mark:
                start_row = index + 1
                break
        for index, cmd in enumerate(self.cmd_list):
            if index >= start_row and (cmd.strip() == stop_mark or (stop_mark is None and re.match("<.*>", cmd))):
                stop_row = index
                break

        for cmd in self.cmd_list[start_row: stop_row]:
            if cmd == '\n' or re.match("<.*>", cmd):
                pass
            else:
                if cmd.startswith(common_prefix):
                    res = self.common_cmd(
                        cmd.lstrip(common_prefix).rstrip() if param_dict is None else cmd.rstrip().format(**param_dict))
                elif cmd.startswith(rfsw_prefix):
                    res = self.rfsw_cmd(
                        cmd.lstrip(rfsw_prefix).rstrip() if param_dict is None else cmd.rstrip().format(**param_dict))
                elif cmd.startswith(aashell_prefix):
                    res = self.aashell_cmd(
                        cmd.lstrip(aashell_prefix).rstrip() if param_dict is None else cmd.rstrip().format(**param_dict))
        return res
