import time
from typing import Optional, Union


def countdown(t: int, msg_begin: Optional[str] = None, msg_end: Optional[str] = None):
    """

    :param t:
    :param msg_begin:
    :param msg_end:
    :return:
    """
    if msg_begin is not None:
        print(msg_begin, flush=True)
    for i in range(t, 0, -1):
        print("\r{} seconds!".format(i), end='', flush=True)
        time.sleep(1)
    if msg_end is not None:
        print('\r' + msg_end, flush=True)


def str2float(s1: Union[str, float, int, list, tuple]):
    """
    把数字或者列表转换成float类型或者float类型的列表
    :param s1:
    :return:
    """
    def s2f(s2: Union[str, float, int]):
        if str(s2).count('.') == 0:
            return int(s2)
        elif str(s2).count('.') == 1:
            a, b = str(s2).split('.')
            if float(b) == 0:
                return int(a)
            else:
                if abs(float(s2)) <= 0.1:
                    f = f"{float(s2):.4f}"
                elif abs(float(s2)) < 1:
                    f = f"{float(s2):.3f}"
                else:
                    f = f"{float(s2):.2f}"
                return float(f)
        else:
            raise Exception('NOT A NUMBER!')

    if isinstance(s1, (str, float, int)):
        return s2f(s1)
    elif isinstance(s1, (list, tuple)):
        return [s2f(i) for i in s1]
    else:
        raise Exception("TYPE ERROR!")


def hz2mhz(h1: Union[str, float, int, list, tuple]):
    """
    把Hz转换成MHz或者MHz列表
    :param h1:
    :return:
    """
    def h2m(h2: Union[str, float, int]):
        if abs(float(h2) / 1e6) <= 0.1:
            m = "%.4f" % (float(h2) / 1e6)
        elif abs(float(h2) / 1e6) < 1:
            m = "%.3f" % (float(h2) / 1e6)
        else:
            m = "%.2f" % (float(h2) / 1e6)
        return float(m)

    if isinstance(h1, (str, float, int)):
        return h2m(h1)
    elif isinstance(h1, (list, tuple)):
        return [h2m(i) for i in h1]
    else:
        raise Exception("TYPE ERROR!")
