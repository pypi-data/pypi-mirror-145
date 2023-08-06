import re
import time
from typing import Optional
import logging
import pyvisa as visa
from PyQt6.QtCore import pyqtSignal


class VisaConnection:
    def __init__(self, address: str, logger: Optional[logging.Logger], sg: Optional[pyqtSignal] = None,
                 timeout: int = 10000, send_interval: float = 0.5):
        """
        :param address:
        :param logger:
        :param sg:
        :param timeout: milliseconds
        :param send_interval: seconds
        """
        self._rm = visa.ResourceManager()
        self._tcp_inst = self._rm.open_resource(address)
        self._tcp_inst.timeout = timeout
        self._tcp_inst.write_termination = '\n'
        self.logger = logger
        self.sg = sg
        self.send_interval = send_interval

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

    def send_cmd(self, command: str) -> None:
        """

        :param command:
        :param delay:
        :return:
        """
        self.log(command)
        self._tcp_inst.write(command)
        time.sleep(self.send_interval)

    def rec_cmd(self, command: str) -> str:
        """

        :param command:
        :return:
        """
        self.log(command)
        self.log(res := self._tcp_inst.query(command))
        return res

    def load_cmd_file(self, file_path: str):
        """
        通过文本方式执行命令
        :param file_path:
        :return:
        """
        with open(file_path) as file:
            self.cmd_list = file.readlines()

    def send_by_file(self, param_dict: Optional[dict] = None,
                     start_mark: Optional[str] = None, stop_mark: Optional[str] = None):
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
        :return:
        """
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
                self.send_cmd(cmd.rstrip() if param_dict is None else cmd.rstrip().format(**param_dict))
