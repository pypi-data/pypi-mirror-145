import time
from typing import List, Optional, Union
from xml.etree import ElementTree
import numpy
from pywinauto import Application, mouse, clipboard, keyboard
from tools.tools import countdown
from windows.windows import show_hide_windows

ElementTree.register_namespace('SOAP-ENV', "http://schemas.xmlsoap.org/soap/envelope/")


class SoapTalker:
    """
    message_init --> tx_on --> tx_off ...
    """

    def __init__(self, path: str, struct_list: List[List[int]], order_list: List[Union[int, List[int]]]):
        """

        :param path:
        :param struct_list: 使用软件UISpy得到gui结构
        0   message
        1   text
        2   save
        3   clear
        :param order_list: 顺序从1开始
        0   int     根顺序
        1   list
        2   int     第一个dacc的顺序
        3   int     第一个activate顺序
        如下结构，则order_list = [2, [1, 2, 4], 5, 13]
        LTE_1
        LTE_2
            - DasAntennaDevices Subscribe True
            - DasAntennaMap Create
            - DasAntennaMap Delete
            - DasAntennaMap Subscribe
            - DownlinkAntennaCarrierContainer Tx1 Create
            - DownlinkAntennaCarrierContainer Tx1 Delete
            - DownlinkAntennaCarrierContainer Tx2 Create
            - DownlinkAntennaCarrierContainer Tx2 Delete
            - DownlinkAntennaCarrierContainer Tx3 Create
            - DownlinkAntennaCarrierContainer Tx3 Delete
            - DownlinkAntennaCarrierContainer Tx4 Create
            - DownlinkAntennaCarrierContainer Tx4 Delete
            - Tx1 Activate
            - Tx1 Create
            - Tx1 Deactivate
            - Tx1 Delete
            ...
        LTE_3
        ...
        """
        self.order_list = order_list
        show_hide_windows('SoapTalker')
        app = Application(backend="uia").connect(path=path)
        self.soap_dlg = app.window(title="SoapTalker")
        frame_list = [self.soap_dlg] * 4
        for i in frame_list:
            for j in struct_list[i]:
                frame_list[i] = frame_list[i].children()[j]
        self.message, self.text, self.save, self.clear = frame_list

    def clear_message(self):
        self.clear.click_input()

    def show_elements(self, msg_color: str = 'red', text_color: str = 'blue', save_color: str = 'green',
                      thickness: int = 5):
        """
        debug方法，显示轮廓
        """
        self.soap_dlg.set_focus()
        time.sleep(2)
        self.message.draw_outline(colour=msg_color, thickness=thickness)
        time.sleep(1)
        self.text.draw_outline(colour=text_color, thickness=thickness)
        time.sleep(1)
        self.save.draw_outline(colour=save_color, thickness=thickness)

    def send_message(self, delay: int = 2, msg_begin: Optional[str] = None, msg_end: Optional[str] = None):
        """
        send the selected soap message
        :param delay:
        :param msg_begin: counting down message
        :param msg_end: count down over message
        :return:
        """
        keyboard.send_keys('{VK_APPS}')
        keyboard.send_keys('{DOWN}')
        keyboard.send_keys('{ENTER}')
        if delay >= 5:
            countdown(delay, msg_begin, msg_end)
        else:
            time.sleep(delay)

    def message_init(self, branch_list: List[int], dacc_create_params_list: List[List[Union[int, List[int]]]],
                     dacc_change_enable: bool = True):
        """

        :param branch_list:
        :param dacc_create_params_list:
        0   Tx1     对于单载波：[portNumber1, format1, S1, variableDelay1]
                    对于双载波：[[portNumber1, format1, S1, variableDelay1], [portNumber2, format2, S2, variableDelay2]]
                    对于三载波：[[portNumber1, format1, S1, variableDelay1], [portNumber2, format2, S2, variableDelay2],
                              [portNumber3, format3, S3, variableDelay3]]
        1   Tx2
        2   Tx3
        3   Tx4
        :param dacc_change_enable:
        :return:
        """
        self.restore_message_position()
        if dacc_change_enable:
            for br in branch_list:
                channel = br % 4
                keyboard.send_keys('{DOWN %d}' % (self.order_list[2] + channel * 2))
                self.change_dacc_tx_create(*dacc_create_params_list[channel % 4])
                self.restore_message_position()

        tmp1 = [self.order_list[1][0]]
        tmp1.extend(numpy.diff(self.order_list[1]))
        for i in tmp1:
            keyboard.send_keys('{DOWN} %d' % i)
            self.send_message()
        keyboard.send_keys(
            '{DOWN} %d' % (self.order_list[2] - self.order_list[1][-1]))  # cursor move to DACC Tx1 Create

        tmp2 = [branch_list[0]]
        tmp2.extend(numpy.diff(branch_list))
        for br in branch_list:  # DACC Tx Create
            channel = br % 4
            keyboard.send_keys('{DOWN} %d' % (channel * 2))
            self.send_message()

    def tx_on(self, car_num: int, branch: int, mode: str,
              freq1: float, freq2: float, freq3: float, bw1: float, bw2: float, bw3: float,
              pow1: float, pow2: float, pow3: float,
              create_delay_list: List[int], activate_delay_list: List[int]):
        """

        :param car_num:
        :param branch:
        :param mode:
        :param freq1:
        :param freq2:
        :param freq3:
        :param bw1:
        :param bw2:
        :param bw3:
        :param pow1:
        :param pow2:
        :param pow3:
        :param create_delay_list:
        0 Tx1 delay
        1 Tx2 delay
        2 Tx3 delay
        3 Tx4 delay
        :param activate_delay_list:
        0 Tx1 delay
        1 Tx2 delay
        2 Tx3 delay
        3 Tx4 delay
        :return:
        """
        channel = branch % 4
        self.restore_message_position()
        keyboard.send_keys('{DOWN %d}' % (self.order_list[3] + channel * 2 + 1))  # cursor move to Tx Create
        if car_num == 1:
            self.change_tx_create(mode, [freq1, bw1, pow1])
        elif car_num == 2:
            self.change_tx_create(mode, [freq1, bw1, pow1], [freq2, bw2, pow2])
        elif car_num == 3:
            self.change_tx_create(mode, [freq1, bw1, pow1], [freq2, bw2, pow2], [freq3, bw3, pow3])
        self.restore_message_position()
        # Tx on
        keyboard.send_keys('{DOWN %d}' % (self.order_list[3] + channel * 2 + 1))
        self.send_message(create_delay_list[channel], "to tx create", "Tx create complete!")  # Tx Create
        keyboard.send_keys('{UP}')
        self.send_message(activate_delay_list[channel], "to tx activate", "Tx activate complete!")  # Tx Activate

    def tx_off(self):
        """

        :return:
        """
        self.soap_dlg.set_focus()
        time.sleep(0.5)
        keyboard.send_keys('{DOWN 2}')
        self.send_message()  # Tx Deactivate
        keyboard.send_keys('{DOWN}')
        self.send_message()  # Tx Delete

    def restore_message_position(self):
        """
        消息树恢复到初始状态，每页都折叠
        :return:
        """
        x = self.message.rectangle().left
        y = self.message.rectangle().top
        self.soap_dlg.set_focus()
        for _ in range(10):
            mouse.scroll(coords=(x + 50, y + 50), wheel_dist=8)
        mouse.click(coords=(x + 40, y + 10))
        keyboard.send_keys('{LEFT}')
        for _ in range(4):
            keyboard.send_keys('{DOWN}')
            keyboard.send_keys('{LEFT}')
        time.sleep(0.5)
        mouse.click(coords=(x + 40, y + 10))
        keyboard.send_keys('{RIGHT}')
        time.sleep(0.5)
        mouse.click(coords=(x + 80, y + 40))
        keyboard.send_keys('{UP}')
        keyboard.send_keys('{LEFT}')
        keyboard.send_keys('{DOWN %d}' % (self.order_list[0] - 1))
        keyboard.send_keys('{RIGHT}')

    def change_tx_create(self, mode: str, *args: list):
        """

        :param mode:
        :param args:
        对于单载波：[freq1, bw1, pow1]
        对于双载波：[freq1, bw1, pow1], [freq2, bw2, pow2]
        对于三载波：[freq1, bw1, pow1], [freq2, bw2, pow2], [freq3, bw3, pow3]
        :return:
        """
        data_modul = """       <parameter>
                            <parameterName>modulationLevel</parameterName>
                            <newValue>1</newValue>
                            <prevValue/>
                        </parameter>"""
        x = self.text.rectangle().left
        y = self.text.rectangle().top
        mouse.click(coords=(x + 50, y + 50))
        keyboard.send_keys('^a')
        time.sleep(0.5)
        keyboard.send_keys('^c')
        time.sleep(0.5)
        keyboard.send_keys('{BACKSPACE}')
        data = clipboard.GetData()
        root = ElementTree.fromstring(data)
        for i, managedObject in enumerate(root.iter('managedObject')):
            managedObject.find("./parameter[parameterName='channels']").find('newValue').find('channel').find(
                'frequency').text = str(int(args[i][0] * 1e6))
            managedObject.find("./parameter[parameterName='channels']").find('newValue').find('channel').find(
                'bandwidth').text = str(int(args[i][1] * 1e6))
            managedObject.find("./parameter[parameterName='power']").find('newValue').text = f"{args[i][2]:g}"
            modul = managedObject.find("./parameter[parameterName='modulationLevel']")
            if modul is not None and mode.find('A') == -1:
                managedObject.remove(modul)
            elif modul is None and mode.find('A') > -1:
                managedObject.insert(5, ElementTree.fromstring(data_modul))
        new_data = ElementTree.tostring(root, encoding="unicode")
        keyboard.send_keys(new_data, pause=0, with_spaces=True, with_tabs=True, with_newlines=True)
        time.sleep(5)
        self.save.click_input()

    def change_dacc_tx_create(self, *args: list):
        """

        :param args:
        对于单载波：[portNumber1, S1, position1, variableDelay1]
        对于双载波：[portNumber1, S1, position1, variableDelay1], [portNumber2, S2, position2, variableDelay2]
        对于三载波：[portNumber1, S1, position1, variableDelay1], [portNumber2, S2, position2, variableDelay2],
                  [portNumber3, S3, position3, variableDelay3]
        :return:
        """
        x = self.text.rectangle().left
        y = self.text.rectangle().top
        mouse.click(coords=(x + 50, y + 50))
        keyboard.send_keys('^a')
        time.sleep(0.5)
        keyboard.send_keys('^c')
        time.sleep(0.5)
        keyboard.send_keys('{BACKSPACE}')
        data = clipboard.GetData()
        root = ElementTree.fromstring(data)
        for i, managedObject in enumerate(root.iter('managedObject')):
            managedObject.find("./parameter[parameterName='portNumber']").find('newValue').text = str(args[i][0])
            managedObject.find("./parameter[parameterName='S']").find('newValue').text = str(args[i][1])
            managedObject.find("./parameter[parameterName='position']").find('newValue').text = str(args[i][2])
            managedObject.find("./parameter[parameterName='variableDelay']").find('newValue').text = str(args[i][3])
        new_data = ElementTree.tostring(root, encoding="unicode")
        keyboard.send_keys(new_data, pause=0, with_spaces=True, with_tabs=True, with_newlines=True)
        time.sleep(5)
        self.save.click_input()
