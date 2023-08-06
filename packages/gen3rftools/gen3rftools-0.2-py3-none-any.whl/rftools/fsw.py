from typing import Optional, List
from goto import with_goto
from goto import goto, label
from tools.tools import countdown, hz2mhz, str2float
from visa.visa import VisaConnection
from collections import namedtuple

Obw = namedtuple('Obw', ('obw1', 'obw2', 'obw3'))
Ccdf = namedtuple('Ccdf', ('mean', 'peak', 'crest', 'p10', 'p1', 'p0d1', 'p0d01'))
SeRange = namedtuple('SeRange', ('range_no', 'range_low', 'range_up', 'rbw', 'frequency', 'power_abs', 'delta_limit'))
Se = namedtuple('Se', ('range1', 'range2', 'range3', 'range4', 'range5'))
Acp = namedtuple('Acp', ('chp1', 'chp2', 'chp3',
                         'sub_block_a_total', 'sub_block_b_total', 'sub_block_c_total',
                         'adj_lower', 'adj_upper', 'alt1_lower', 'alt1_upper',
                         'gap1l_aclr', 'gap1u_aclr', 'gap2l_aclr', 'gap2u_aclr',
                         'gap1l_caclr', 'gap1u_caclr', 'gap2l_caclr', 'gap2u_caclr'),
                 defaults=(None,) * 18)
EvmCase = namedtuple('EvmCase', ('mean', 'min', 'max'))
LteEvm = namedtuple('LteEvm', ('evm_pdsch_qpsk', 'evm_pdsch_16qam', 'evm_pdsch_64qam', 'evm_pdsch_256qam',
                               'evm_all', 'evm_phys_channel', 'evm_phys_signal',
                               'frequency_error', 'sampling_error',
                               'iq_offset', 'iq_gain_imbalance', 'iq_quadrature_error',
                               'rstp', 'ostp', 'rssi', 'power', 'crest_factor'))
MultiEvm = namedtuple('LteMultiEvm', ('evm1', 'evm2', 'evm3'), defaults=(None,) * 3)
SemRange = namedtuple('SemRange', ('range_no', 'start_freq_rel', 'stop_freq_rel', 'rbw',
                                   'frequency_at_delta_to_limit', 'power_abs', 'power_rel', 'delta_to_limit'))
Sem = namedtuple('Sem', ('tx_power1', 'tx_power2', 'tx_power3',
                         'range1', 'range2', 'range3', 'range4', 'range5', 'range6', 'range7', 'range8'),
                 defaults=(None,) * 11)
Nr5gEvm = namedtuple('Nr5gEvm', ('evm_pdsch_qpsk', 'evm_pdsch_16qam', 'evm_pdsch_64qam', 'evm_pdsch_256qam',
                                 'evm_all', 'evm_phys_channel', 'evm_phys_signal', 'frequency_error', 'sampling_error',
                                 'iq_offset', 'iq_gain_imbalance', 'iq_quadrature_error',
                                 'ostp', 'power', 'crest_factor'))


class RsVisa:
    def __init__(self, v: VisaConnection):
        self.v = v

    def obw(self, freq1: float, bw1: float,
            loss: float, span: float, rel: float, att: int, rbw: int, count: int, point: int,
            is_exr: bool, is_ext: bool, delay: int,
            is_create: bool, create_name: str, current_name: str, rename: Optional[str], snap_path: str, is_hold: bool,
            gate_delay: Optional[float] = None, gate_length: Optional[float] = None
            ) -> Obw:
        """

        :param freq1:
        :param bw1:
        :param loss:
        :param span:
        :param rel:
        :param att:
        :param rbw:
        :param count:
        :param point:
        :param is_exr:
        :param is_ext:
        :param delay:
        :param is_create:
        :param create_name:
        :param current_name:
        :param rename:
        :param snap_path:
        :param is_hold:
        :param gate_delay:
        :param gate_length:
        :return:
        """
        if is_create:
            self.v.send_cmd(f"INST:CRE:NEW SANALYZER, {create_name!r}")
        else:
            self.v.send_cmd(f"INST {current_name!r}")
            if rename is not None:
                self.v.send_cmd(f"INST:REN {current_name!r},{rename!r}")
        if not is_hold:
            self.v.send_cmd("CALC:MARK:FUNC:POW:SEL OBW")
        if is_exr:
            self.v.send_cmd(":SENS:ROSC:SOUR E10")
        if is_ext:
            self.v.send_cmd("TRIG:SOUR EXT")
            self.v.send_cmd("SENS:SWE:EGAT ON")
            if gate_delay is not None:
                self.v.send_cmd(f"SENS:SWE:EGAT:HOLD {gate_delay}ms")
            if gate_length is not None:
                self.v.send_cmd(f"SENS:SWE:EGAT:LENG {gate_length}ms")

        self.v.send_cmd(f"FREQ:CENT {freq1} MHz")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
        self.v.send_cmd(f"INP:ATT {att}dB")
        self.v.send_cmd("DISP:TRAC1:MODE AVER")
        self.v.send_cmd("DET RMS")
        self.v.send_cmd(f"POW:ACH:BAND {bw1} MHz")
        self.v.send_cmd(f"FREQ:SPAN {span} MHz")
        self.v.send_cmd(f"BAND {rbw} kHz")
        self.v.send_cmd(f"SWE:COUN {count}")
        self.v.send_cmd(f"SWE:POIN {point}")

        # v.send_cmd("INIT:CONT OFF")
        # v.send_cmd("INIT;*WAI")
        # time.sleep(delay)
        countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

        if snap_path is not None:
            self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
            self.v.send_cmd("HCOP:DEV:LANG1 JPG")
            self.v.send_cmd("HCOP:CMAP:DEF4")
            self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
            self.v.send_cmd("HCOP:IMM1")

        res_obw = self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? OBW")
        return Obw(hz2mhz(res_obw), None, None)

    def multi_obw(self, car_num: int, freq1: float, freq2: float, bw1: float, bw2: float,
                  loss: float, span_list: List[float], rel: float, att: int, rbw: int,
                  count_list: List[int], point_list: List[int], is_exr: bool, is_ext: bool, delay_list: List[int],
                  is_create: bool, create_name_list: List[str], current_name_list: List[str],
                  rename_list: List[Optional[str]], snap_path_list: List[str], is_hold: bool,
                  gate_delay: Optional[float] = None, gate_length: Optional[float] = None,
                  freq3: float = None, bw3: float = None
                  ) -> Obw:
        """

        :param car_num:
        :param freq1:
        :param freq2:
        :param bw1:
        :param bw2:
        :param loss:
        :param span_list:
        :param rel:
        :param att:
        :param rbw:
        :param count_list:
        :param point_list:
        :param is_exr:
        :param is_ext:
        :param delay_list:
        :param is_create:
        :param create_name_list:
        :param current_name_list:
        :param rename_list:
        :param snap_path_list:
        :param is_hold:
        :param gate_delay:
        :param gate_length:
        :param freq3:
        :param bw3:
        :return:
        """
        if car_num == 2:
            span1, span2 = span_list
            count1, count2 = count_list
            point1, point2 = point_list
            current_name1, current_name2 = current_name_list
            delay1, delay2 = delay_list
            rename1, rename2 = rename_list
            snap_path1, snap_path2 = snap_path_list
            created_name1, created_name2 = create_name_list
            res1 = self.obw(freq1=freq1, bw1=bw1, loss=loss,
                            span=span1, rel=rel, att=att, rbw=rbw, count=count1, point=point1, is_exr=is_exr,
                            is_ext=is_ext,
                            delay=delay1, is_create=is_create, create_name=created_name1,
                            current_name=current_name1, rename=rename1, snap_path=snap_path1, is_hold=is_hold,
                            gate_delay=gate_delay, gate_length=gate_length)
            res2 = self.obw(freq1=freq2, bw1=bw2, loss=loss,
                            span=span2, rel=rel, att=att, rbw=rbw, count=count2, point=point2, is_exr=is_exr,
                            is_ext=is_ext,
                            delay=delay2, is_create=is_create, create_name=created_name2,
                            current_name=current_name2, rename=rename2, snap_path=snap_path2, is_hold=is_hold,
                            gate_delay=gate_delay, gate_length=gate_length)
            res_multi_obw = Obw(res1.obw1, res2.obw1, None)
            return res_multi_obw

        elif car_num == 3:
            span1, span2, span3 = span_list
            count1, count2, count3 = count_list
            point1, point2, point3 = point_list
            current_name1, current_name2, current_name3 = current_name_list
            delay1, delay2, delay3 = delay_list
            rename1, rename2, rename3 = rename_list
            snap_path1, snap_path2, snap_path3 = snap_path_list
            created_name1, created_name2, created_name3 = create_name_list
            res1 = self.obw(freq1=freq1, bw1=bw1, loss=loss,
                            span=span1, rel=rel, att=att, rbw=rbw, count=count1, point=point1, is_exr=is_exr,
                            is_ext=is_ext,
                            delay=delay1, is_create=is_create, create_name=created_name1,
                            current_name=current_name1, rename=rename1, snap_path=snap_path1, is_hold=is_hold)
            res2 = self.obw(freq1=freq2, bw1=bw2, loss=loss,
                            span=span2, rel=rel, att=att, rbw=rbw, count=count2, point=point2, is_exr=is_exr,
                            is_ext=is_ext,
                            delay=delay2, is_create=is_create, create_name=created_name2,
                            current_name=current_name2, rename=rename2, snap_path=snap_path2, is_hold=is_hold)
            res3 = self.obw(freq1=freq3, bw1=bw3, loss=loss,
                            span=span3, rel=rel, att=att, rbw=rbw, count=count3, point=point3, is_exr=is_exr,
                            is_ext=is_ext,
                            delay=delay3, is_create=is_create, create_name=created_name3,
                            current_name=current_name3, rename=rename3, snap_path=snap_path3, is_hold=is_hold)
            res_multi_obw = Obw(res1.obw1, res2.obw1, res3.obw1)
            return res_multi_obw

    def ccdf(self, cfreq: float,
             loss: float, rel: int, att: int, abw: int, samp_num: int, is_exr: bool, is_ext: bool, delay: int,
             is_create: bool, create_name: str, current_name: str, rename: Optional[str], snap_path: str, is_hold: bool
             ) -> Ccdf:
        """

        :param cfreq:
        :param loss:
        :param rel:
        :param att:
        :param abw:
        :param samp_num:
        :param is_exr:
        :param is_ext:
        :param delay:
        :param is_create:
        :param create_name:
        :param current_name:
        :param rename:
        :param snap_path:
        :param is_hold:
        :return:
        [Mean, Peak, Crest, 10%, 1%, 0.1%, 0.01%]
          0     1      2     3   4    5      6
        """
        if is_create:
            self.v.send_cmd(f"INST:CRE:NEW SANALYZER, {create_name!r}")
        else:
            self.v.send_cmd(f"INST {current_name!r}")
            if rename is not None:
                self.v.send_cmd(f"INST:REN {current_name!r},{rename!r}")

        if not is_hold:
            self.v.send_cmd("CALC:STAT:CCDF ON")

        if is_exr:
            self.v.send_cmd(":SENS:ROSC:SOUR E10")
        if is_ext:
            self.v.send_cmd("TRIG:SOUR EXT")
            self.v.send_cmd("SENS:SWE:EGAT ON")

        self.v.send_cmd(f"FREQ:CENT {cfreq} MHz")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
        self.v.send_cmd(f"INP:ATT {att}dB")
        self.v.send_cmd(f"BAND {abw} MHz")
        self.v.send_cmd(f"CALC1:STAT:NSAM {samp_num}")

        # v.send_cmd("INIT:CONT OFF")
        # v.send_cmd("INIT;*WAI")
        # time.sleep(delay)
        countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

        if snap_path is not None:
            self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
            self.v.send_cmd("HCOP:DEV:LANG1 JPG")
            self.v.send_cmd("HCOP:CMAP:DEF4")
            self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
            self.v.send_cmd("HCOP:IMM1")

        res = self.v.rec_cmd("CALC:STAT:RES1? ALL").split(";")
        res_ccdf = Ccdf(*(str2float(res)),
                        str2float(self.v.rec_cmd("CALC:STAT:CCDF:X1? P10")),
                        str2float(self.v.rec_cmd("CALC:STAT:CCDF:X1? P1")),
                        str2float(self.v.rec_cmd("CALC:STAT:CCDF:X1? P0_1")),
                        str2float(self.v.rec_cmd("CALC:STAT:CCDF:X1? P0_01"))
                        )
        return res_ccdf

    def se(self, freq_start: float, freq_stop: float, cfreq: float,
           loss: float, rel: float, att: int, is_exr: bool, is_ext: bool, delay: int,
           is_create: bool, create_name: str, current_name: str, rename: Optional[str], snap_path: str, is_hold: bool,
           gate_delay: Optional[float] = None, gate_length: Optional[float] = None
           ) -> Se:
        """

        :param loss:
        :param freq_start:
        :param freq_stop:
        :param cfreq:
        :param rel:
        :param att:
        :param is_exr:
        :param is_ext:
        :param delay:
        :param is_create:
        :param create_name:
        :param current_name:
        :param rename:
        :param snap_path:
        :param is_hold:
        :param gate_delay: ms
        :param gate_length: ms
        :return:
        [Range No, Range Low(MHz), Range Up(MHz), RBW(MHz), Frequency(MHz), Power Abs(dBm), Delta Limit(dB)]
        5 Ranges Totally
        """
        start = str(freq_start - 10)
        stop = str(freq_stop + 10)
        range_list = [
            ["9KHz", "150KHz", "1KHz", "-36", "-36", "701"],
            ["150KHz", "30MHz", "10KHz", "-36", "-36", "4001"],
            ["30MHz", "1GHz", "100KHz", "-36", "-36", "32001"],
            ["1GHz", "%sMHz" % start, "1MHz", "-30", "-30", "16001"],
            ["%sMHz" % stop, "12.75GHz", "1MHz", "-30", "-30", "16001"]
        ]

        if is_create:
            self.v.send_cmd(f"INST:CRE:NEW SANALYZER, {create_name!r}")
        else:
            self.v.send_cmd(f"INST {current_name!r}")
            if rename is not None:
                self.v.send_cmd(f"INST:REN {current_name!r},{rename!r}")

        if not is_hold:
            self.v.send_cmd("SWE:MODE LIST")

        if is_exr:
            self.v.send_cmd(":SENS:ROSC:SOUR E10")
        if is_ext:
            self.v.send_cmd("TRIG:SOUR EXT")
            self.v.send_cmd("SENS:SWE:EGAT ON")
            self.v.send_cmd("SENS:SWE:EGAT:CONT:STAT ON")
            if gate_delay is not None:
                self.v.send_cmd(f"SENS:SWE:EGAT:HOLD {gate_delay}ms")
            if gate_length is not None:
                self.v.send_cmd(f"SENS:SWE:EGAT:LENG {gate_length}ms")

        self.v.send_cmd(f"FREQ:CENT {cfreq} MHz")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
        self.v.send_cmd("INIT:CONT OFF")
        for i, r in enumerate(range_list, 1):
            self.v.send_cmd(f"LIST:RANG{i}:FREQ:STAR {r[0]}")
            self.v.send_cmd(f"LIST:RANG{i}:FREQ:STOP {r[1]}")
            self.v.send_cmd(f"LIST:RANG{i}:BAND:RES {r[2]}")
            self.v.send_cmd(f"LIST:RANG{i}:LIM:STAR {r[3]}")
            self.v.send_cmd(f"LIST:RANG{i}:LIM:STOP {r[4]}")
            self.v.send_cmd(f"LIST:RANG{i}:POIN {r[5]}")
            self.v.send_cmd(f"LIST:RANG{i}:INP:ATT:AUTO OFF")
            self.v.send_cmd(f"LIST:RANG{i}:INP:ATT {att}")
        self.v.send_cmd("SENS:LIST:XADJ;*WAI")
        self.v.send_cmd("INIT:SPUR;*WAI")
        # self.v.send_cmd(":INIT:CONM")

        countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

        if snap_path is not None:
            self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
            self.v.send_cmd("HCOP:DEV:LANG1 JPG")
            self.v.send_cmd("HCOP:CMAP:DEF4")
            self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
            self.v.send_cmd("HCOP:IMM1")

        res = self.v.rec_cmd("TRAC:DATA? LIST").split(",")
        res_se_range = []
        for i in range(5):
            res_se_range.append(SeRange(
                i + 1,
                hz2mhz(res[i * 11 * 25 + 1]),
                hz2mhz(res[i * 11 * 25 + 2]),
                hz2mhz(res[i * 11 * 25 + 3]),
                hz2mhz(res[i * 11 * 25 + 4]),
                str2float(res[i * 11 * 25 + 5]),
                str2float(res[i * 11 * 25 + 7])
            ))
        res_se = Se(*res_se_range)
        return res_se

    def lte_acp(self, mode: str, freq1: float, bw1: float,
                loss: float, rel: int, att: int, is_exr: bool, is_ext: bool, delay: int,
                is_create: bool, create_name: str, current_name: str, rename: Optional[str],
                snap_path: str, is_hold: bool,
                gate_delay: Optional[float] = None, gate_length: Optional[float] = None
                ) -> Acp:
        """

        :param mode:
        :param freq1:
        :param bw1:
        :param loss:
        :param rel:
        :param att:
        :param is_exr:
        :param is_ext:
        :param delay:
        :param is_create:
        :param create_name:
        :param current_name:
        :param rename:
        :param snap_path:
        :param is_hold:
        :param gate_delay:
        :param gate_length:
        :return:
        [TX Total(dBm),
            0
        ACLR Power
        Adj Lower(dBc), Adj Upper(dBc), Alt1 Lower(dBc), Alt1 Upper(dBc)]
            1               2               3               4
        """
        lte_t_mode = f"E-{mode}__{bw1:g}MHz"
        if is_create:
            self.v.send_cmd(f"INST:CRE:NEW LTE, {create_name!r}")
        else:
            self.v.send_cmd(f"INST {current_name!r}")
            if rename is not None:
                self.v.send_cmd(f"INST:REN {current_name!r},{rename!r}")

        if not is_hold:
            self.v.send_cmd("CONF:LTE:MEAS ACLR")
            self.v.send_cmd(f"MMEM:LOAD:CC:TMOD:DL {lte_t_mode!r}")
            self.v.send_cmd(":SENS:POW:NCOR ON")

        if is_exr:
            self.v.send_cmd(":SENS:ROSC:SOUR E10")
        if is_ext:
            self.v.send_cmd("TRIG:SOUR EXT")
            self.v.send_cmd("SENS:SWE:EGAT ON")
            if gate_delay is not None:
                self.v.send_cmd(f"SENS:SWE:EGAT:HOLD {gate_delay}ms")
            if gate_length is not None:
                self.v.send_cmd(f"SENS:SWE:EGAT:LENG {gate_length}ms")

        self.v.send_cmd(f"FREQ:CENT {freq1} MHz")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
        self.v.send_cmd(f"INP:ATT {att}dB")

        # v.send_cmd("INIT:CONT OFF")
        self.v.send_cmd("INIT;*WAI")
        # time.sleep(delay)
        countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

        if snap_path is not None:
            self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
            self.v.send_cmd("HCOP:DEV:LANG1 JPG")
            self.v.send_cmd("HCOP:CMAP:DEF4")
            self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
            self.v.send_cmd("HCOP:IMM1")

        res = str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? ACP").split(","))
        res_lte_acp = Acp(res[0], None, None, None, None, None, *res[-4:])
        return res_lte_acp

    def lte_multi_acp(self, mode: str, car_num: int, freq1: float, freq2: float, bw1: float, bw2: float,
                      loss: float, rel: int, att: int, is_exr: bool, is_ext: bool, delay: int,
                      is_create: bool, create_name: str, current_name: str, rename: Optional[str],
                      snap_path: str, is_hold: bool,
                      gate_delay: Optional[float] = None, gate_length: Optional[float] = None,
                      freq3: float = None, bw3: float = None
                      ) -> Acp:
        """

        :param mode:
        :param car_num:
        :param freq1:
        :param freq2:
        :param bw1:
        :param bw2:
        :param loss:
        :param rel:
        :param att:
        :param is_exr:
        :param is_ext:
        :param delay:
        :param is_create:
        :param create_name:
        :param current_name:
        :param rename:
        :param snap_path:
        :param is_hold:
        :param gate_delay: ms
        :param gate_length: ms
        :param freq3:
        :param bw3:
        :return:
        (1)acp_type == lte_two_carriers_s_gap_acp
        two continuous carriers and two carriers with gap < 15M:
        Power
        [CHP1(dBm), CHP2(dBm), Sub Block A Total(dBm),
            0           1           2
        ACLR Power
        Adj Lower(dBc), Adj Upper(dBc), Alt1 Lower(dBc), Alt1 Upper(dBc)]
            3               4               5               6

        (2)acp_type == lte_two_carriers_m_gap_acp
        two carriers with 15M <= gap < 20M:
        Power
        [CHP1(dBm), CHP2(dBm), Sub Block A Total(dBm), Sub Block B Total(dBm),
            0           1           2                       3
        ACLR Power
        Adj Lower(dBc), Adj Upper(dBc), Alt1 Lower(dBc), Alt1 Upper(dBc),
            4               5               6               7
        ACLR Power
        AB:Gap1L(dBc), AB:Gap1U(dBc)
            8               9
        CACLR Power
        AB:Gap1L(dBc), AB:Gap1U(dBc)
            10              11

        (3)acp_type == lte_two_carriers_l_gap_acp
        two carriers with gap >= 20M:
        Power
        [CHP1(dBm), CHP2(dBm), Sub Block A Total(dBm), Sub Block B Total(dBm),
            0           1           2                       3
        ACLR Power
        Adj Lower(dBc), Adj Upper(dBc), Alt1 Lower(dBc), Alt1 Upper(dBc),
            4               5               6               7
        ACLR Power
        AB:Gap1L(dBc), AB:Gap1U(dBc), AB:Gap2L(dBc), AB:Gap2U(dBc),
            8               9               10          11
        CACLR Power
        AB:Gap1L(dBc), AB:Gap1U(dBc), AB:Gap2L(dBc), AB:Gap2U(dBc)]
            12               13             14          15

        (4)acp_type == lte_three_carriers_acp
        three continuous carriers:
        Power
        [CHP1(dBm), CHP2(dBm), CHP3(dBm), Sub Block A Total(dBm),
            0           1           2           3
        ACLR Power
        Adj Lower(dBc), Adj Upper(dBc), Alt1 Lower(dBc), Alt1 Upper(dBc)]
            4               5               6               7
        """
        gap1 = freq2 - freq1 - bw1 / 2 - bw2 / 2
        if is_create:
            self.v.send_cmd(f"INST:CRE:NEW LTE, {create_name!r}")
        else:
            self.v.send_cmd(f"INST {current_name!r}")
            if rename is not None:
                self.v.send_cmd(f"INST:REN {current_name!r},{rename!r}")

        if car_num == 2:
            lte_t_mode1 = f"E-{mode}__{bw1:g}MHz"
            if not is_hold:
                self.v.send_cmd("CONF:LTE:MEAS MCAClr")
                self.v.send_cmd(f"MMEM:LOAD:CC:TMOD:DL {lte_t_mode1!r}")
                self.v.send_cmd("CONF:LTE:NOCC 2")
                self.v.send_cmd(f"CONF:LTE:DL:CC:BW BW{bw1:g}_00")
                self.v.send_cmd(f"CONF:LTE:DL:CC2:BW BW{bw2:g}_00")
                self.v.send_cmd(":SENS:POW:NCOR ON")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC {freq1} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC2 {freq2} MHz")
            self.v.send_cmd(":SENS:POW:ACH:REF:TXCH:AUTO LHIG")

            if is_exr:
                self.v.send_cmd(":SENS:ROSC:SOUR E10")
            if is_ext:
                self.v.send_cmd("TRIG:SOUR EXT")
                self.v.send_cmd("SENS:SWE:EGAT ON")
                if gate_delay is not None:
                    self.v.send_cmd(f"SENS:SWE:EGAT:HOLD {gate_delay}ms")
                if gate_length is not None:
                    self.v.send_cmd(f"SENS:SWE:EGAT:LENG {gate_length}ms")

            self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
            self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
            self.v.send_cmd(f"INP:ATT {att}dB")
            self.v.send_cmd("LAY:SPL 1,2,54")

            # v.send_cmd("INIT:CONT OFF")
            self.v.send_cmd("INIT;*WAI")
            # time.sleep(delay)
            countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

            if snap_path is not None:
                self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
                self.v.send_cmd("HCOP:DEV:LANG1 JPG")
                self.v.send_cmd("HCOP:CMAP:DEF4")
                self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
                self.v.send_cmd("HCOP:IMM1")

            res = str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? MCAC").split(","))
            if gap1 < 15:
                res_lte_multi_acp = Acp(res[0], res[1], None, res[2], None, None, *res[3:7])
            elif 15 <= gap1 < 20:
                res_lte_multi_acp = Acp(res[0], res[1], None, *res[2:4], None, *res[4:8],
                                        *str2float(
                                            self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? GACL").split(",")[0:2]),
                                        None, None,
                                        *str2float(
                                            self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? MACM").split(",")[0:2])
                                        )
            else:
                res_lte_multi_acp = Acp(res[0], res[1], None, *res[2:4], None, *res[4:8],
                                        *str2float(
                                            self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? GACL").split(",")),
                                        *str2float(
                                            self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? MACM").split(","))
                                        )
        # three continuous carriers
        else:
            lte_t_mode1 = f"E-{mode}__{bw1:g}MHz"
            if not is_hold:
                self.v.send_cmd("CONF:LTE:MEAS MCAClr")
                self.v.send_cmd(f"MMEM:LOAD:CC:TMOD:DL {lte_t_mode1!r}")
                self.v.send_cmd("CONF:LTE:NOCC 3")
                self.v.send_cmd(f"CONF:LTE:DL:CC:BW BW{bw1:g}_00")
                self.v.send_cmd(f"CONF:LTE:DL:CC2:BW BW{bw2:g}_00")
                self.v.send_cmd(f"CONF:LTE:DL:CC3:BW BW{bw3:g}_00")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC {freq1} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC2 {freq2} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC3 {freq3} MHz")
            self.v.send_cmd(":SENS:POW:ACH:REF:TXCH:AUTO LHIG")

            if is_exr:
                self.v.send_cmd(":SENS:ROSC:SOUR E10")
            if is_ext:
                self.v.send_cmd("TRIG:SOUR EXT")
                self.v.send_cmd("SENS:SWE:EGAT ON")
                if gate_delay is not None:
                    self.v.send_cmd(f"SENS:SWE:EGAT:HOLD {gate_delay}ms")
                if gate_length is not None:
                    self.v.send_cmd(f"SENS:SWE:EGAT:LENG {gate_length}ms")

            self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
            self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
            self.v.send_cmd(f"INP:ATT {att}dB")
            self.v.send_cmd("LAY:SPL 1,2,54")

            # v.send_cmd("INIT:CONT OFF")
            self.v.send_cmd("INIT;*WAI")
            # time.sleep(delay)
            countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

            if snap_path is not None:
                self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
                self.v.send_cmd("HCOP:DEV:LANG1 JPG")
                self.v.send_cmd("HCOP:CMAP:DEF4")
                self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
                self.v.send_cmd("HCOP:IMM1")

            res = str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? MCAC").split(","))
            res_lte_multi_acp = Acp(*res[0:4], None, None, *res[-4:])
        return res_lte_multi_acp

    @with_goto
    def lte_evm(self, mode: str, freq1: float, bw1: float,
                loss: float, rel: float, att: int, cell_id: int, is_exr: bool, is_ext: bool, delay: int,
                is_create: bool, created_name: str, current_name: str, rename: Optional[str],
                snap_path: str, is_hold: bool,
                evm_mode: int = 0
                ) -> Optional[LteEvm]:
        """

        :param mode:
        :param freq1:
        :param bw1:
        :param loss:
        :param rel:
        :param att:
        :param cell_id:
        :param is_exr:
        :param is_ext:
        :param delay:
        :param is_create:
        :param created_name:
        :param current_name:
        :param rename:
        :param snap_path:
        :param is_hold:
        :param evm_mode: 0默认，设置后抓取数据；1只设置不抓数据；2不设置只抓数据
        :return:
        [EVM PDSCH QPSK(%), EVM PDSCH 16QAM(%), EVM PDSCH 64QAM(%), EVM PDSCH 256QAM(%),
            0                   1                   2                   3
        EVM ALL(%), EVM Phys Channel(%), EVM Phys Signal(%),
            4           5                   6
        Frequency Error(Hz), Sampling Error(ppm),
            7                   8
        I/Q Offset(dB), I/Q Gain Imbalance(dB), I/Q Quadrature Error(°),
            9               10                      11
        RSTP(dBm), OSTP(dBm), RSSI(dBm),
            12      13          14
        Power(dBm), Crest Factor(dB)]
            15          16
        """
        if evm_mode == 2:
            goto.res
        lte_t_mode = f"E-{mode}__{bw1:g}MHz"
        if is_create:
            self.v.send_cmd(f"INST:CRE:NEW LTE, {created_name!r}")
        else:
            self.v.send_cmd(f"INST {current_name!r}")
            if rename is not None:
                self.v.send_cmd(f"INST:REN {current_name!r},{rename!r}")

        if not is_hold:
            self.v.send_cmd("CONF:LTE:MEAS EVM")
            self.v.send_cmd(f"MMEM:LOAD:CC:TMOD:DL {lte_t_mode!r}")
            self.v.send_cmd(f"CONF:LTE:DL:CC:PLC:CID {cell_id}")
            self.v.send_cmd("LAY:REM:WIND '3'")
            self.v.send_cmd("LAY:ADD:WIND? '5',LEFT,EVSY")

        if is_exr:
            self.v.send_cmd(":SENS:ROSC:SOUR E10")
        if is_ext:
            self.v.send_cmd("TRIG:SOUR EXT")
        self.v.send_cmd(f"FREQ:CENT {freq1} MHz")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
        self.v.send_cmd(f"INP:ATT {att}dB")

        # v.send_cmd("INIT:CONT OFF")
        # v.send_cmd("INIT;*WAI")
        # time.sleep(delay)
        if evm_mode == 1:
            return
        label.res
        countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

        if snap_path is not None:
            self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
            self.v.send_cmd("HCOP:DEV:LANG1 JPG")
            self.v.send_cmd("HCOP:CMAP:DEF4")
            self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
            self.v.send_cmd("HCOP:IMM1")

        evm_qpsk = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSQP:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSQP:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSQP:MAX?")))
        evm_16qam = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSST:AVER?")),
                            str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSST:MIN?")),
                            str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSST:MAX?")))
        evm_64qam = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSSF:AVER?")),
                            str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSSF:MIN?")),
                            str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSSF:MAX?")))
        evm_256qam = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSTS:AVER?")),
                             str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSTS:MIN?")),
                             str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSTS:MAX?")))
        evm_all = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:AVER?")),
                          str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:MIN?")),
                          str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:MAX?")))
        evm_pch = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:PCH:AVER?")),
                          str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:PCH:MIN?")),
                          str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:PCH:MAX?")))
        evm_psig = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:PSIG:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:PSIG:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:PSIG:MAX?")))
        evm_ferr = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:FERR:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:FERR:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:FERR:MAX?")))
        evm_serr = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:SERR:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:SERR:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:SERR:MAX?")))
        evm_iqof = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:IQOF:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:IQOF:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:IQOF:MAX?")))
        evm_gimb = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:GIMB:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:GIMB:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:GIMB:MAX?")))
        evm_quad = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:QUAD:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:QUAD:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:QUAD:MAX?")))
        evm_rstp = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:RSTP:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:RSTP:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:RSTP:MAX?")))
        evm_ostp = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:OSTP:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:OSTP:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:OSTP:MAX?")))
        evm_rssi = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:RSSI:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:RSSI:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:RSSI:MAX?")))
        evm_pow = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:POW:AVER?")),
                          str2float(self.v.rec_cmd("FETC:CC1:SUMM:POW:MIN?")),
                          str2float(self.v.rec_cmd("FETC:CC1:SUMM:POW:MAX?")))
        evm_cres = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:CRES:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:CRES:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:CRES:MAX?")))
        res_lte_evm = LteEvm(evm_qpsk, evm_16qam, evm_64qam, evm_256qam, evm_all, evm_pch, evm_psig, evm_ferr, evm_serr,
                             evm_iqof, evm_gimb, evm_quad, evm_rstp, evm_ostp, evm_rssi, evm_pow, evm_cres)
        return res_lte_evm

    @with_goto
    def lte_multi_evm(self, mode: str, car_num: int, freq1: float, freq2: float, bw1: float, bw2: float,
                      loss: float, rel: float, att: int, cell_id_list: List[int],
                      is_exr: bool, is_ext: bool, delay: int,
                      is_create: bool, create_name: str, current_name: str, rename: Optional[str],
                      snap_path: str, is_hold: bool,
                      evm_mode: int = 0,
                      freq3: float = None, bw3: float = None
                      ) -> Optional[MultiEvm]:
        """

        :param mode:
        :param car_num:
        :param freq1:
        :param freq2:
        :param bw1:
        :param bw2:
        :param loss:
        :param rel:
        :param att:
        :param cell_id_list:
        :param is_exr:
        :param is_ext:
        :param delay:
        :param is_create:
        :param create_name:
        :param current_name:
        :param rename:
        :param snap_path:
        :param is_hold:
        :param evm_mode: 0默认，设置后抓取数据；1只设置不抓数据；2不设置只抓数据
        :param freq3:
        :param bw3:
        :return:
        [CC1_EVM, CC2_EVM (, CC3_EVM)]
        [EVM PDSCH QPSK(%), EVM PDSCH 16QAM(%), EVM PDSCH 64QAM(%), EVM PDSCH 256QAM(%),
            0                   1                   2                   3
        EVM ALL(%), EVM Phys Channel(%), EVM Phys Signal(%),
            4           5                   6
        Frequency Error(Hz), Sampling Error(ppm),
            7                   8
        I/Q Offset(dB), I/Q Gain Imbalance(dB), I/Q Quadrature Error(¡ã),
            9               10                      11
        RSTP(dBm), OSTP(dBm), RSSI(dBm),
            12      13          14
        Power(dBm), Crest Factor(dB)]
            15          16
        """
        if evm_mode == 2:
            goto.res
        if is_create:
            self.v.send_cmd(f"INST:CRE:NEW LTE, {create_name!r}")
        else:
            self.v.send_cmd(f"INST {current_name!r}")
            if rename is not None:
                self.v.send_cmd(f"INST:REN {current_name!r},{rename!r}")

        if car_num == 2:
            lte_t_mode1 = f"E-{mode}__{bw1:g}MHz"
            lte_t_mode2 = f"E-{mode}__{bw2:g}MHz"
            cell_id1, cell_id2 = cell_id_list if cell_id_list is not None else [1, 2]

            if not is_hold:
                self.v.send_cmd("CONF:LTE:MEAS EVM")
                self.v.send_cmd("CONF:LTE:NOCC 2")
                self.v.send_cmd(f"MMEM:LOAD:CC:TMOD:DL {lte_t_mode1!r}")
                self.v.send_cmd(f"CONF:LTE:DL:CC:PLC:CID {cell_id1}")
                self.v.send_cmd(f"MMEM:LOAD:CC2:TMOD:DL {lte_t_mode2!r}")
                self.v.send_cmd(f"CONF:LTE:DL:CC2:PLC:CID {cell_id2}")
                self.v.send_cmd("LAY:REM:WIND '3'")
                self.v.send_cmd("LAY:ADD:WIND? '5',LEFT,EVSY")

            self.v.send_cmd(f"SENS:FREQ:CENT:CC {freq1} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC2 {freq2} MHz")
            self.v.send_cmd("SENS:LTE:DL:DEM:MCF ON")
        # three carriers
        else:
            lte_t_mode1 = f"E-{mode}__{bw1:g}MHz"
            lte_t_mode2 = f"E-{mode}__{bw2:g}MHz"
            lte_t_mode3 = f"E-{mode}__{bw3:g}MHz"
            cell_id1, cell_id2, cell_id3 = cell_id_list if cell_id_list is not None else [1, 2, 3]
            if not is_hold:
                self.v.send_cmd("CONF:LTE:MEAS EVM")
                self.v.send_cmd("CONF:LTE:NOCC 3")
                self.v.send_cmd(f"MMEM:LOAD:CC:TMOD:DL {lte_t_mode1!r}")
                self.v.send_cmd(f"CONF:LTE:DL:CC:PLC:CID {cell_id1}")
                self.v.send_cmd(f"MMEM:LOAD:CC2:TMOD:DL {lte_t_mode2!r}")
                self.v.send_cmd(f"CONF:LTE:DL:CC2:PLC:CID {cell_id2}")
                self.v.send_cmd(f"MMEM:LOAD:CC3:TMOD:DL {lte_t_mode3!r}")
                self.v.send_cmd(f"CONF:LTE:DL:CC3:PLC:CID {cell_id3}")
                self.v.send_cmd("LAY:REM:WIND '3'")
                self.v.send_cmd("LAY:ADD:WIND? '5',LEFT,EVSY")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC {freq1} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC2 {freq2} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC3 {freq3} MHz")
            self.v.send_cmd("SENS:LTE:DL:DEM:MCF ON")

        if is_exr:
            self.v.send_cmd(":SENS:ROSC:SOUR E10")
        if is_ext:
            self.v.send_cmd("TRIG:SOUR EXT")

        self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
        self.v.send_cmd(f"INP:ATT {att}dB")

        # v.send_cmd("INIT:CONT OFF")
        # v.send_cmd("INIT;*WAI")
        # time.sleep(delay)
        if evm_mode == 1:
            return
        label.res
        countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

        if snap_path is not None:
            self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
            self.v.send_cmd("HCOP:DEV:LANG1 JPG")
            self.v.send_cmd("HCOP:CMAP:DEF4")
            self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
            self.v.send_cmd("HCOP:IMM1")

        res_lte_evm_list = []
        for i in range(1, car_num + 1):
            evm_qpsk = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSQP:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSQP:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSQP:MAX?")))
            evm_16qam = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSST:AVER?")),
                                str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSST:MIN?")),
                                str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSST:MAX?")))
            evm_64qam = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSSF:AVER?")),
                                str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSSF:MIN?")),
                                str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSSF:MAX?")))
            evm_256qam = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSTS:AVER?")),
                                 str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSTS:MIN?")),
                                 str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSTS:MAX?")))
            evm_all = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:AVER?")),
                              str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:MIN?")),
                              str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:MAX?")))
            evm_pch = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:PCH:AVER?")),
                              str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:PCH:MIN?")),
                              str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:PCH:MAX?")))
            evm_psig = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:PSIG:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:PSIG:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:PSIG:MAX?")))
            evm_ferr = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:FERR:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:FERR:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:FERR:MAX?")))
            evm_serr = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:SERR:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:SERR:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:SERR:MAX?")))
            evm_iqof = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:IQOF:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:IQOF:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:IQOF:MAX?")))
            evm_gimb = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:GIMB:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:GIMB:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:GIMB:MAX?")))
            evm_quad = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:QUAD:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:QUAD:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:QUAD:MAX?")))
            evm_rstp = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:RSTP:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:RSTP:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:RSTP:MAX?")))
            evm_ostp = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:OSTP:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:OSTP:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:OSTP:MAX?")))
            evm_rssi = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:RSSI:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:RSSI:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:RSSI:MAX?")))
            evm_pow = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:POW:AVER?")),
                              str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:POW:MIN?")),
                              str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:POW:MAX?")))
            evm_cres = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:CRES:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:CRES:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:CRES:MAX?")))
            res_lte_evm_list.append(
                LteEvm(evm_qpsk, evm_16qam, evm_64qam, evm_256qam, evm_all, evm_pch, evm_psig, evm_ferr, evm_serr,
                       evm_iqof, evm_gimb, evm_quad, evm_rstp, evm_ostp, evm_rssi, evm_pow, evm_cres))
        res_lte_multi_evm = MultiEvm(*res_lte_evm_list)
        return res_lte_multi_evm

    def lte_sem(self, mode: str, freq1: float, bw1: float,
                loss: float, rel: float, att: int, is_exr: bool, is_ext: bool, delay: int,
                is_create: bool, create_name: str, current_name: str, rename: Optional[str],
                snap_path: str, is_hold: bool,
                gate_delay: Optional[float] = None, gate_length: Optional[float] = None,
                ) -> Sem:
        """

        :param mode:
        :param freq1:
        :param bw1:
        :param loss:
        :param rel:
        :param att:
        :param is_exr:
        :param is_ext:
        :param delay:
        :param is_create:
        :param create_name:
        :param current_name:
        :param rename:
        :param snap_path:
        :param is_hold:
        :param gate_delay: ms
        :param gate_length: ms
        :param stime_index: ms / MHz
        :return:
        [TxPower(dBm), Range No, Start Freq Rel(MHz), Stop Freq Rel(MHz), RBW(MHz),
        Frequency at Delta to Limit(MHz), Power Abs(dBm), Power Rel(dB), Delta to Limit(dB), ...]
        4 Ranges Totally
        """
        lte_t_mode = f"E-{mode}__{bw1:g}MHz"
        if is_create:
            self.v.send_cmd(f"INST:CRE:NEW LTE, {create_name!r}")
        else:
            self.v.send_cmd(f"INST {current_name!r}")
            if rename is not None:
                self.v.send_cmd(f"INST:REN {current_name!r},{rename!r}")

        if not is_hold:
            self.v.send_cmd("CONF:LTE:MEAS ESP")
            self.v.send_cmd(f"MMEM:LOAD:CC:TMOD:DL {lte_t_mode!r}")
            self.v.send_cmd("SENS:POW:SEM:CAT LARE")

        if is_exr:
            self.v.send_cmd(":SENS:ROSC:SOUR E10")
        if is_ext:
            self.v.send_cmd("TRIG:SOUR EXT")
            self.v.send_cmd("SENS:SWE:EGAT ON")
            if gate_delay is not None:
                self.v.send_cmd(f"SENS:SWE:EGAT:HOLD {gate_delay}ms")
            if gate_length is not None:
                self.v.send_cmd(f"SENS:SWE:EGAT:LENG {gate_length}ms")

        self.v.send_cmd(f"FREQ:CENT {freq1} MHz")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
        # v.send_cmd("INIT:CONT OFF")

        self.v.send_cmd(
            f"SENS:ESP1:PRES:STAN 'C:\R_S\Instr\sem_std\EUTRA-LTE\LTE_SEM_DL_BW{bw1:g}_00_LocalArea_FSW.xml'")
        self.v.send_cmd("SENS:ESP1:RANG2:DEL")
        self.v.send_cmd("SENS:ESP1:RANG5:DEL")
        self.v.send_cmd(f"SENS:ESP1:RANG1:FREQ:STOP -{bw1 / 2 + 5.05} MHz")
        self.v.send_cmd(f"SENS:ESP1:RANG5:FREQ:STAR {bw1 / 2 + 5.05} MHz")
        self.v.send_cmd(f"SENS:ESP1:RANG3:FREQ:STAR -{bw1 / 2 + 0.05} MHz")
        for i in range(1, 6):
            self.v.send_cmd(f"SENS:ESP1:RANG{i}:INP:ATT {att}")
            # st = abs(float(self.v.rec_cmd(f":SENS:ESP1:RANG{i}:FREQ:STAR?")) - float(
            #     self.v.rec_cmd(f":SENS:ESP1:RANG{i}:FREQ:STOP?"))) * 1e-6 * stime_index
            # self.v.send_cmd(f":SENS:ESP1:RANG{i}:SWE:TIME {st}ms")
        self.v.send_cmd("SENS:ESP1:RANG2:LIM1:ABS:STAR -37")
        self.v.send_cmd("SENS:ESP1:RANG2:LIM1:ABS:STOP -30")
        self.v.send_cmd("SENS:ESP1:RANG4:LIM1:ABS:STAR -30")
        self.v.send_cmd("SENS:ESP1:RANG4:LIM1:ABS:STOP -37")

        # v.send_cmd("INIT:CONT OFF")
        self.v.send_cmd("INIT;*WAI")
        # time.sleep(delay)
        countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

        if snap_path is not None:
            self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
            self.v.send_cmd("HCOP:DEV:LANG1 JPG")
            self.v.send_cmd("HCOP:CMAP:DEF4")
            self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
            self.v.send_cmd("HCOP:IMM1")

        res = str2float(self.v.rec_cmd("TRAC:DATA? LIST").split(","))
        res_sem_range = []
        for i in range(4):
            res[1 + 11 * i: 5 + 11 * i] = hz2mhz(res[1 + 11 * i: 5 + 11 * i])
        while 0.0 in res:
            res.remove(0.0)
        for j in range(4):
            res_sem_range.append(SemRange(*res[8 * j: 8 * j + 8]))
        res_sem = Sem(str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? CPOW")),
                      None, None,
                      *res_sem_range)
        return res_sem

    def lte_multi_sem(self, mode: str, car_num: int, freq1: float, freq2: float, bw1: float, bw2: float,
                      loss: float, rel: float, att: int, is_exr: bool, is_ext: bool, delay: int,
                      is_create: bool, created_name: str, current_name: str, rename: Optional[str],
                      snap_path: str, is_hold: bool,
                      gate_delay: Optional[float] = None, gate_length: Optional[float] = None,
                      stime_index: float = 0.1,
                      freq3: float = None, bw3: float = None
                      ) -> Sem:
        """

        :param mode:
        :param car_num:
        :param freq1:
        :param freq2:
        :param bw1:
        :param bw2:
        :param loss:
        :param rel:
        :param att:
        :param is_exr:
        :param is_ext:
        :param delay:
        :param is_create:
        :param created_name:
        :param current_name:
        :param rename:
        :param snap_path:
        :param is_hold:
        :param gate_delay: ms
        :param gate_length: ms
        :param stime_index: ms / MHz
        :param freq3:
        :param bw3:
        :return:
        (1)sem_type == lte_two_carriers_s_gap_sem
        two continuous carriers and two carriers with gap <= 0.1M:
        [TxPower1(dBm), TxPower2(dBm), Range No, Start Freq Rel(MHz), Stop Freq Rel(MHz), RBW(MHz),
        Frequency at Delta to Limit(MHz), Power Abs(dBm), Power Rel(dB), Delta to Limit(dB), ...]
        4 Ranges Totally

        (2)sem_type == lte_two_carriers_m_gap_sem
        two carriers with 0.1M < gap <= 10.1M:
        6 Ranges Totally

        (3)sem_type == lte_two_carriers_l_gap_sem
        two carriers with gap > 10.1M:
        8 Ranges Totally

        (4)sem_type == lte_three_carriers_sem
        three continuous carriers:
        [TxPower1(dBm), TxPower2(dBm), TxPower3(dBm), Range No, Start Freq Rel(MHz), Stop Freq Rel(MHz), RBW(MHz),
        Frequency at Delta to Limit(MHz), Power Abs(dBm), Power Rel(dB), Delta to Limit(dB), ...]
        4 Ranges Totally
        """
        gap1 = freq2 - freq1 - bw1 / 2 - bw2 / 2
        if is_create:
            self.v.send_cmd(f"INST:CRE:NEW LTE, {created_name!r}")
        else:
            self.v.send_cmd(f"INST {current_name!r}")
            if rename is not None:
                self.v.send_cmd(f"INST:REN {current_name!r},{rename!r}")

        if car_num == 2:
            lte_t_mode1 = f"E-{mode}__{bw1:g}MHz"
            if not is_hold:
                self.v.send_cmd("CONF:LTE:MEAS MCESpectrum")
                self.v.send_cmd("CONF:LTE:NOCC 2")
                self.v.send_cmd(f"MMEM:LOAD:CC:TMOD:DL {lte_t_mode1!r}")
                self.v.send_cmd("SENS:POW:SEM:CAT LARE")
                self.v.send_cmd(f"CONF:LTE:DL:CC:BW BW{bw1:g}_00")
                self.v.send_cmd(f"CONF:LTE:DL:CC2:BW BW{bw2:g}_00")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC {freq1} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC2 {freq2} MHz")

            if is_exr:
                self.v.send_cmd(":SENS:ROSC:SOUR E10")
            if is_ext:
                self.v.send_cmd("TRIG:SOUR EXT")
                self.v.send_cmd("SENS:SWE:EGAT ON")
                if gate_delay is not None:
                    self.v.send_cmd(f"SENS:SWE:EGAT:HOLD {gate_delay}ms")
                if gate_length is not None:
                    self.v.send_cmd(f"SENS:SWE:EGAT:LENG {gate_length}ms")

            self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
            self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
            # v.send_cmd("INIT:CONT OFF")

            for i, bw in enumerate((bw1, bw2), 1):
                self.v.send_cmd(
                    f"SENS:ESP{i}:PRES:STAN 'C:\R_S\Instr\sem_std\EUTRA-LTE\LTE_SEM_DL_BW{bw:g}_00_LocalArea_FSW.xml'")
                self.v.send_cmd(f"SENS:ESP{i}:RANG2:DEL")
                self.v.send_cmd(f"SENS:ESP{i}:RANG5:DEL")
                self.v.send_cmd(f"SENS:ESP{i}:RANG1:FREQ:STOP -{bw / 2 + 5.05} MHz")
                self.v.send_cmd(f"SENS:ESP{i}:RANG5:FREQ:STAR {bw / 2 + 5.05} MHz")
                # self.v.send_cmd(f"SENS:ESP{i}:RANG3:FREQ:STAR -{bw / 2 + 5.05} MHz")
                for j in range(1, 6):
                    self.v.send_cmd(f"SENS:ESP{i}:RANG{j}:INP:ATT {att}")
                self.v.send_cmd(f"SENS:ESP{i}:RANG2:LIM1:ABS:STAR -37")
                self.v.send_cmd(f"SENS:ESP{i}:RANG2:LIM1:ABS:STOP -30")
                self.v.send_cmd(f"SENS:ESP{i}:RANG4:LIM1:ABS:STAR -30")
                self.v.send_cmd(f"SENS:ESP{i}:RANG4:LIM1:ABS:STOP -37")
            if gap1 <= 0.1:
                num = 4
            elif 0.1 < gap1 <= 10.1:
                num = 6
                self.v.send_cmd("SENS:ESP1:RANG5:DEL")
                self.v.send_cmd(f"SENS:ESP1:RANG4:FREQ:STOP {bw1 / 2 + gap1 / 2} MHz")
                self.v.send_cmd("SENS:ESP2:RANG1:DEL")
                self.v.send_cmd(f"SENS:ESP2:RANG1:FREQ:STAR -{bw2 / 2 + gap1 / 2} MHz")
            # gap1 > 10.2
            else:
                num = 8
                self.v.send_cmd(f"SENS:ESP1:RANG5:FREQ:STOP {bw1 / 2 + gap1 / 2} MHz")
                self.v.send_cmd(f"SENS:ESP2:RANG1:FREQ:STAR -{bw2 / 2 + gap1 / 2} MHz")

            # for n in range(1, 3):
            #     for m in range(1, 5 if num == 6 else 6):
            #         st = abs(float(self.v.rec_cmd(f":SENS:ESP{n}:RANG{m}:FREQ:STAR?")) - float(
            #             self.v.rec_cmd(f":SENS:ESP{n}:RANG{m}:FREQ:STOP?"))) * 1e-6 * stime_index
            #         self.v.send_cmd(f":SENS:ESP{n}:RANG{m}:SWE:TIME {st}ms")

            # v.send_cmd("INIT:CONT OFF")
            self.v.send_cmd("LAY:SPL 1,2,54")
            self.v.send_cmd("INIT;*WAI")
            # time.sleep(delay)
            countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

            if snap_path is not None:
                self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
                self.v.send_cmd("HCOP:DEV:LANG1 JPG")
                self.v.send_cmd("HCOP:CMAP:DEF4")
                self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
                self.v.send_cmd("HCOP:IMM1")

            res = str2float(self.v.rec_cmd("TRAC:DATA? LIST").split(","))
            res_sem_range = []
            for i in range(num):
                res[1 + 11 * i:5 + 11 * i] = hz2mhz(res[1 + 11 * i:5 + 11 * i])
            while 0.0 in res:
                res.remove(0.0)
            for j in range(num):
                res_sem_range.append(SemRange(*res[8 * j: 8 * j + 8]))
            res_lte_multi_sem = Sem(str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW1:RES? CPOW")),
                                    str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW2:RES? CPOW")),
                                    None,
                                    *res_sem_range)

        # three carriers
        else:
            lte_t_mode1 = f"E-{mode}__{bw1:g}MHz"
            if not is_hold:
                self.v.send_cmd("CONF:LTE:MEAS MCESpectrum")
                self.v.send_cmd("CONF:LTE:NOCC 3")
                self.v.send_cmd(f"MMEM:LOAD:CC:TMOD:DL {lte_t_mode1!r}")
                self.v.send_cmd("SENS:POW:SEM:CAT LARE")
                self.v.send_cmd(f"CONF:LTE:DL:CC:BW BW{bw1:g}_00")
                self.v.send_cmd(f"CONF:LTE:DL:CC2:BW BW{bw2:g}_00")
                self.v.send_cmd(f"CONF:LTE:DL:CC3:BW BW{bw3:g}_00")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC {freq1} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC2 {freq2} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC3 {freq3} MHz")

            if is_exr:
                self.v.send_cmd(":SENS:ROSC:SOUR E10")
            if is_ext:
                self.v.send_cmd("TRIG:SOUR EXT")
                self.v.send_cmd("SENS:SWE:EGAT ON")
                if gate_delay is not None:
                    self.v.send_cmd(f"SENS:SWE:EGAT:HOLD {gate_delay}ms")
                if gate_length is not None:
                    self.v.send_cmd(f"SENS:SWE:EGAT:LENG {gate_length}ms")

            self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
            self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")

            for i, bw in enumerate((bw1, bw2, bw3), 1):
                self.v.send_cmd(
                    f"SENS:ESP{i}:PRES:STAN 'C:\R_S\Instr\sem_std\EUTRA-LTE\LTE_SEM_DL_BW{bw:g}_00_LocalArea_FSW.xml'")
                self.v.send_cmd(f"SENS:ESP{i}:RANG2:DEL")
                self.v.send_cmd(f"SENS:ESP{i}:RANG5:DEL")
                self.v.send_cmd(f"SENS:ESP{i}:RANG1:FREQ:STOP -{bw / 2 + 5.05} MHz")
                self.v.send_cmd(f"SENS:ESP{i}:RANG5:FREQ:STAR {bw / 2 + 5.05} MHz")
                self.v.send_cmd(f"SENS:ESP{i}:RANG3:FREQ:STAR -{bw / 2 + 0.05} MHz")
                for j in range(1, 6):
                    self.v.send_cmd(f"SENS:ESP{i}:RANG{j}:INP:ATT {att}")
                self.v.send_cmd(f"SENS:ESP{i}:RANG2:LIM1:ABS:STAR -37")
                self.v.send_cmd(f"SENS:ESP{i}:RANG2:LIM1:ABS:STOP -30")
                self.v.send_cmd(f"SENS:ESP{i}:RANG4:LIM1:ABS:STAR -30")
                self.v.send_cmd(f"SENS:ESP{i}:RANG4:LIM1:ABS:STOP -37")
            num = 4

            for n in range(1, 4):
                for m in range(1, 6):
                    st = abs(float(self.v.rec_cmd(f":SENS:ESP{n}:RANG{m}:FREQ:STAR?")) - float(
                        self.v.rec_cmd(f":SENS:ESP{n}:RANG{m}:FREQ:STOP?"))) * 1e-6 * stime_index
                    self.v.send_cmd(f":SENS:ESP{n}:RANG{m}:SWE:TIME {st}ms")

            self.v.send_cmd("LAY:SPL 1,2,54")
            self.v.send_cmd("INIT;*WAI")
            # time.sleep(delay)
            countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

            if snap_path is not None:
                self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
                self.v.send_cmd("HCOP:DEV:LANG1 JPG")
                self.v.send_cmd("HCOP:CMAP:DEF4")
                self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
                self.v.send_cmd("HCOP:IMM1")

            res = str2float(self.v.rec_cmd("TRAC:DATA? LIST").split(","))
            res_sem_range = []
            for i in range(num):
                res[1 + 11 * i:5 + 11 * i] = hz2mhz(res[1 + 11 * i:5 + 11 * i])
            while 0.0 in res:
                res.remove(0.0)
            for j in range(num):
                res_sem_range.append(SemRange(*res[8 * j: 8 * j + 8]))
            res_lte_multi_sem = Sem(str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW1:RES? CPOW")),
                                    str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW2:RES? CPOW")),
                                    str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW3:RES? CPOW")),
                                    *res_sem_range)
        return res_lte_multi_sem

    def nr5g_acp(self, mode: str, freq1: float, bw1: float,
                 loss: float, rel: int, att: int, is_exr: bool, is_ext: bool, delay: int,
                 is_create: bool, create_name: str, current_name: str, rename: Optional[str],
                 snap_path: str, is_hold: bool,
                 gate_delay: Optional[float] = None, gate_length: Optional[float] = None
                 ) -> Acp:
        """

        :param mode:
        :param freq1:
        :param bw1:
        :param loss:
        :param rel:
        :param att:
        :param is_exr:
        :param is_ext:
        :param delay:
        :param is_create:
        :param create_name:
        :param current_name:
        :param rename:
        :param snap_path:
        :param is_hold:
        :param gate_delay: ms
        :param gate_length: ms
        :return:
        Power
        [TX Total(dBm),
            0
        ACLR Power
        Adj Lower(dBc), Adj Upper(dBc), Alt1 Lower(dBc), Alt1 Upper(dBc)]
            1               2               3               4
        """
        nr5g_t_mode = f"NR-FR1-{mode}__TDD_{bw1:g}MHz_30kHz"
        if is_create:
            self.v.send_cmd(f"INST:CRE:NEW NR5G, {create_name!r}")
        else:
            self.v.send_cmd(f"INST {current_name!r}")
            if rename is not None:
                self.v.send_cmd(f"INST:REN {current_name!r},{rename!r}")

        if not is_hold:
            self.v.send_cmd("CONF:NR5G:MEAS ACLR")
            self.v.send_cmd("CONF:NR5G:DL:CC1:DFR MIDD")
            self.v.send_cmd(f"MMEM:LOAD:TMOD:CC1 {nr5g_t_mode!r}")
            self.v.send_cmd(":SENS:POW:NCOR ON")

        if is_exr:
            self.v.send_cmd(":SENS:ROSC:SOUR E10")
        if is_ext:
            self.v.send_cmd("TRIG:SOUR EXT")
            self.v.send_cmd("SENS:SWE:EGAT ON")
            if gate_delay is not None:
                self.v.send_cmd(f"SENS:SWE:EGAT:HOLD {gate_delay}ms")
            if gate_length is not None:
                self.v.send_cmd(f"SENS:SWE:EGAT:LENG {gate_length}ms")

        self.v.send_cmd(f"FREQ:CENT {freq1} MHz")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
        self.v.send_cmd(f"INP:ATT {att}dB")
        self.v.send_cmd("SENS:SWE:OPT SPE")
        self.v.send_cmd("SENS:SWE:TIME 0.005")

        # self._v.send_cmd("INIT:CONT OFF")
        self.v.send_cmd("INIT;*WAI")
        # time.sleep(delay)
        countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

        if snap_path is not None:
            self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
            self.v.send_cmd("HCOP:DEV:LANG1 JPG")
            self.v.send_cmd("HCOP:CMAP:DEF4")
            self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
            self.v.send_cmd("HCOP:IMM1")

        res = str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? ACP").split(","))
        res_nr5g_acp = Acp(res[0], None, None, None, None, None, *res[-4:])
        return res_nr5g_acp

    def nr5g_multi_acp(self, mode: str, car_num: int, freq1: float, freq2: float, bw1: float, bw2: float,
                       loss: float, rel: int, att: int, is_exr: bool, is_ext: bool, delay: int,
                       is_create: bool, create_name: str, current_name: str, rename: Optional[str],
                       snap_path: str, is_hold: bool,
                       gate_delay: Optional[float] = None, gate_length: Optional[float] = None,
                       freq3: float = None, bw3: float = None
                       ) -> Acp:
        """

        :param mode:
        :param car_num:
        :param freq1:
        :param freq2:
        :param bw1:
        :param bw2:
        :param loss:
        :param rel:
        :param att:
        :param is_exr:
        :param is_ext:
        :param delay:
        :param is_create:
        :param create_name:
        :param current_name:
        :param rename:
        :param snap_path:
        :param is_hold:
        :param gate_delay: ms
        :param gate_length: ms
        :param freq3:
        :param bw3:
        :return:
        (1)acp_type == nr5g_two_carriers_s_gap_acp
        two continuous carriers and two carriers with gap < 10M:
        Power
        [CHP1(dBm), CHP2(dBm), Sub Block A Total(dBm),
            0           1           2
        ACLR Power
        Adj Lower(dBc), Adj Upper(dBc), Alt1 Lower(dBc), Alt1 Upper(dBc)]
            3               4               5               6

        (2)acp_type == nr5g_two_carriers_m_gap_acp
        two carriers with 10M <= gap < 20M:
        Power
        [CHP1(dBm), CHP2(dBm), Sub Block A Total(dBm), Sub Block B Total(dBm),
            0           1           2                       3
        ACLR Power
        Adj Lower(dBc), Adj Upper(dBc), Alt1 Lower(dBc), Alt1 Upper(dBc),
            4               5               6               7
        ACLR Power
        AB:Gap1L(dBc), AB:Gap1U(dBc),
            8               9
        CACLR Power
        AB:Gap1L(dBc), AB:Gap1U(dBc)]
            10              11

        (3)acp_type == nr5g_two_carriers_l_gap_acp
        two carriers with gap >= 20M:
        Power
        [CHP1(dBm), CHP2(dBm), Sub Block A Total(dBm), Sub Block B Total(dBm),
            0           1           2                       3
        ACLR Power
        Adj Lower(dBc), Adj Upper(dBc), Alt1 Lower(dBc), Alt1 Upper(dBc),
            4               5               6               7
        ACLR Power
        AB:Gap1L(dBc), AB:Gap1U(dBc), AB:Gap2L(dBc), AB:Gap2U(dBc),
            8               9               10          11
        CACLR Power
        AB:Gap1L(dBc), AB:Gap1U(dBc), AB:Gap2L(dBc), AB:Gap2U(dBc)]
            12              13              14          15

        (4)acp_type == nr5g_three_carriers_acp
        three continuous carriers:
        Power
        [CHP1(dBm), CHP2(dBm), CHP3(dBm), Sub Block A Total(dBm),
            0           1           2           3
        ACLR Power
        Adj Lower(dBc), Adj Upper(dBc), Alt1 Lower(dBc), Alt1 Upper(dBc)]
            4               5               6               7
        """
        gap1 = freq2 - freq1 - bw1 / 2 - bw2 / 2
        if is_create:
            self.v.send_cmd(f"INST:CRE:NEW NR5G, {create_name!r}")
        else:
            self.v.send_cmd(f"INST {current_name!r}")
            if rename is not None:
                self.v.send_cmd(f"INST:REN {current_name!r},{rename!r}")

        if car_num == 2:
            nr5g_t_mode1 = f"NR-FR1-{mode}__TDD_{bw1:g}MHz_30kHz"
            nr5g_t_mode2 = f"NR-FR1-{mode}__TDD_{bw2:g}MHz_30kHz"
            if not is_hold:
                self.v.send_cmd("CONF:NR5G:MEAS MCAClr")
                self.v.send_cmd("CONF:NR5G:NOCC 2")
                self.v.send_cmd("CONF:NR5G:DL:CC1:DFR MIDD")
                self.v.send_cmd("CONF:NR5G:DL:CC2:DFR MIDD")
                self.v.send_cmd(f"MMEM:LOAD:TMOD:CC1 {nr5g_t_mode1!r}")
                self.v.send_cmd(f"MMEM:LOAD:TMOD:CC2 {nr5g_t_mode2!r}")
                self.v.send_cmd(":SENS:POW:NCOR ON")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC1 {freq1} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC2 {freq2} MHz")
            self.v.send_cmd(":SENS:POW:ACH:REF:TXCH:AUTO LHIG")

            if is_exr:
                self.v.send_cmd(":SENS:ROSC:SOUR E10")
            if is_ext:
                self.v.send_cmd("TRIG:SOUR EXT")
                self.v.send_cmd("SENS:SWE:EGAT ON")
                if gate_delay is not None:
                    self.v.send_cmd(f"SENS:SWE:EGAT:HOLD {gate_delay}ms")
                if gate_length is not None:
                    self.v.send_cmd(f"SENS:SWE:EGAT:LENG {gate_length}ms")

            self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
            self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
            self.v.send_cmd(f"INP:ATT {att}dB")

            self.v.send_cmd("SENS:SWE:OPT SPE")
            self.v.send_cmd("SENS:SWE:TIME 0.005")
            self.v.send_cmd("LAY:SPL 1,2,55")

            # v.send_cmd("INIT:CONT OFF")
            self.v.send_cmd("INIT;*WAI")
            # time.sleep(delay)
            countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

            if snap_path is not None:
                self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
                self.v.send_cmd("HCOP:DEV:LANG1 JPG")
                self.v.send_cmd("HCOP:CMAP:DEF4")
                self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
                self.v.send_cmd("HCOP:IMM1")

            res = str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? MCAC").split(","))
            if (bw1 <= 20 and bw2 <= 20 and gap1 < 15) or (bw1 > 20 and bw2 > 20 and gap1 < 60) or (
                    bw1 <= 20 and bw2 > 20 and gap1 < 30) or (bw1 > 20 and bw2 <= 20 and gap1 < 30):
                res_nr5g_multi_acp = Acp(res[0], res[1], None, *res[2:4], None, *res[4:8])
            elif bw1 <= 20 and bw2 > 20 and 30 <= gap1 < 45:
                res_nr5g_multi_acp = Acp(res[0], res[1], None, *res[2:4], None, *res[4:8],
                                         None,
                                         str2float(
                                             self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? GACL").split(","))[1],
                                         None, None, None,
                                         str2float(
                                             self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? MACM").split(","))[1],
                                         )
            elif bw1 > 20 and bw2 <= 20 and 30 <= gap1 < 45:
                res_nr5g_multi_acp = Acp(res[0], res[1], None, *res[2:4], None, *res[4:8],
                                         str2float(
                                             self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? GACL").split(","))[0],
                                         None, None, None,
                                         str2float(
                                             self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? MACM").split(","))[0],
                                         )
            elif (bw1 <= 20 and bw2 <= 20 and 15 <= gap1 < 20) or (bw1 > 20 and bw2 > 20 and 60 <= gap1 < 80) or (
                    bw1 <= 20 and bw2 > 20 and 45 <= gap1 < 50) or (bw1 > 20 and bw2 <= 20 and 45 <= gap1 < 50):
                res_nr5g_multi_acp = Acp(res[0], res[1], None, *res[2:4], None, *res[4:8],
                                         *str2float(
                                             self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? GACL").split(","))[0:2],
                                         None, None,
                                         *str2float(
                                             self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? MACM").split(","))[0:2],
                                         )
            else:
                res_nr5g_multi_acp = Acp(res[0], res[1], None, *res[2:4], None, *res[4:8],
                                         *str2float(
                                             self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? GACL").split(",")),
                                         *str2float(
                                             self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? MACM").split(",")),
                                         )
        # three continuous carriers
        else:
            nr5g_t_mode1 = f"NR-FR1-{mode}__TDD_{bw1:g}MHz_30kHz"
            nr5g_t_mode2 = f"NR-FR1-{mode}__TDD_{bw2:g}MHz_30kHz"
            nr5g_t_mode3 = f"NR-FR1-{mode}__TDD_{bw3:g}MHz_30kHz"
            if not is_hold:
                self.v.send_cmd("CONF:NR5G:MEAS MCAClr")
                self.v.send_cmd("CONF:NR5G:NOCC 2")
                self.v.send_cmd("CONF:NR5G:DL:CC1:DFR MIDD")
                self.v.send_cmd("CONF:NR5G:DL:CC2:DFR MIDD")
                self.v.send_cmd("CONF:NR5G:DL:CC3:DFR MIDD")
                self.v.send_cmd(f"MMEM:LOAD:TMOD:CC1 {nr5g_t_mode1!r}")
                self.v.send_cmd(f"MMEM:LOAD:TMOD:CC2 {nr5g_t_mode2!r}")
                self.v.send_cmd(f"MMEM:LOAD:TMOD:CC3 {nr5g_t_mode3!r}")
                self.v.send_cmd(":SENS:POW:NCOR ON")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC1 {freq1} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC2 {freq2} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC3 {freq3} MHz")
            self.v.send_cmd(":SENS:POW:ACH:REF:TXCH:AUTO LHIG")

            if is_exr:
                self.v.send_cmd(":SENS:ROSC:SOUR E10")
            if is_ext:
                self.v.send_cmd("TRIG:SOUR EXT")
                self.v.send_cmd("SENS:SWE:EGAT ON")
                if gate_delay is not None:
                    self.v.send_cmd(f"SENS:SWE:EGAT:HOLD {gate_delay}ms")
                if gate_length is not None:
                    self.v.send_cmd(f"SENS:SWE:EGAT:LENG {gate_length}ms")

            self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
            self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
            self.v.send_cmd(f"INP:ATT {att}dB")

            self.v.send_cmd("SENS:SWE:OPT SPE")
            self.v.send_cmd("SENS:SWE:TIME 0.005")
            self.v.send_cmd("LAY:SPL 1,2,55")

            # v.send_cmd("INIT:CONT OFF")
            self.v.send_cmd("INIT;*WAI")
            # time.sleep(delay)
            countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

            if snap_path is not None:
                self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
                self.v.send_cmd("HCOP:DEV:LANG1 JPG")
                self.v.send_cmd("HCOP:CMAP:DEF4")
                self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
                self.v.send_cmd("HCOP:IMM1")

            res = str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? MCAC").split(","))
            res_nr5g_multi_acp = Acp(*res[0:10])
        return res_nr5g_multi_acp

    @with_goto
    def nr5g_evm(self, mode: str, freq1: float, bw1: float,
                 loss: float, rel: float, att: int, cell_id: int, is_exr: bool, is_ext: bool, delay: int,
                 is_create: bool, create_name: str, current_name: str, rename: Optional[str],
                 snap_path: str, is_hold: bool,
                 evm_mode: int = 0
                 ) -> Optional[Nr5gEvm]:
        """

        :param mode:
        :param freq1:
        :param bw1:
        :param loss:
        :param rel:
        :param att:
        :param cell_id:
        :param is_exr:
        :param is_ext:
        :param delay:
        :param is_create:
        :param create_name:
        :param current_name:
        :param rename:
        :param snap_path:
        :param is_hold:
        :param hub:
        :param timing:
        :param limit:
        :param max_time:
        :param step:
        :param evm_mode: 0默认，设置后抓取数据；1只设置不抓数据；2不设置只抓数据
        :return:
        [EVM PDSCH QPSK(%), EVM PDSCH 16QAM(%), EVM PDSCH 64QAM(%), EVM PDSCH 256QAM(%),
            0                   1                   2                   3
        EVM ALL(%), EVM Phys Channel(%), EVM Phys Signal(%),
            4           5                   6
        Frequency Error(Hz), Sampling Error(ppm),
            7                   8
        I/Q Offset(dB), I/Q Gain Imbalance(dB), I/Q Quadrature Error(°),
            9               10                      11
        OSTP(dBm),
            12
        Power(dBm), Crest Factor(dB)]
            13          14
        """
        if evm_mode == 2:
            goto.res
        nr5g_t_mode = f"NR-FR1-{mode}__TDD_{bw1:g}MHz_30kHz"
        if is_create:
            self.v.send_cmd(f"INST:CRE:NEW NR5G, {create_name!r}")
        else:
            self.v.send_cmd(f"INST {current_name!r}")
            if rename is not None:
                self.v.send_cmd(f"INST:REN {current_name!r},{rename!r}")

        if not is_hold:
            self.v.send_cmd("CONF:NR5G:MEAS EVM")
            self.v.send_cmd("CONF:NR5G:DL:CC1:DFR MIDD")
            self.v.send_cmd(f"MMEM:LOAD:TMOD:CC1 {nr5g_t_mode!r}")
            self.v.send_cmd(f"CONF:NR5G:DL:CC1:PLC:CID {cell_id}")
            self.v.send_cmd("CONF:NR5G:DL:CC1:RFUC:STAT OFF")
            self.v.send_cmd("CONF:NR5G:DL:CC1:IDC ON")
            self.v.send_cmd("LAY:REM:WIND '3'")
            self.v.send_cmd("LAY:ADD:WIND? '4',LEFT,EVSY")

        if is_exr:
            self.v.send_cmd(":SENS:ROSC:SOUR E10")
        if is_ext:
            self.v.send_cmd("TRIG:SOUR EXT")

        self.v.send_cmd(f"FREQ:CENT {freq1} MHz")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
        self.v.send_cmd(f"INP:ATT {att}dB")

        if evm_mode == 1:
            return
        label.res

        self.v.send_cmd("INIT:IMM;*WAI")

        # v.send_cmd("INIT:CONT OFF")
        # v.send_cmd("INIT;*WAI")
        # time.sleep(delay)
        countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

        if snap_path is not None:
            self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
            self.v.send_cmd("HCOP:DEV:LANG1 JPG")
            self.v.send_cmd("HCOP:CMAP:DEF4")
            self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
            self.v.send_cmd("HCOP:IMM1")

        evm_qpsk = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSQP:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSQP:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSQP:MAX?")))
        evm_16qam = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSST:AVER?")),
                            str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSST:MIN?")),
                            str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSST:MAX?")))
        evm_64qam = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSSF:AVER?")),
                            str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSSF:MIN?")),
                            str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSSF:MAX?")))
        evm_256qam = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSTS:AVER?")),
                             str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSTS:MIN?")),
                             str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:DSTS:MAX?")))
        evm_all = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:AVER?")),
                          str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:MIN?")),
                          str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:MAX?")))
        evm_pch = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:PCH:AVER?")),
                          str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:PCH:MIN?")),
                          str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:PCH:MAX?")))
        evm_psig = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:PSIG:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:PSIG:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:EVM:PSIG:MAX?")))
        evm_ferr = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:FERR:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:FERR:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:FERR:MAX?")))
        evm_serr = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:SERR:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:SERR:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:SERR:MAX?")))
        evm_iqof = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:IQOF:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:IQOF:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:IQOF:MAX?")))
        evm_gimb = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:GIMB:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:GIMB:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:GIMB:MAX?")))
        evm_quad = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:QUAD:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:QUAD:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:QUAD:MAX?")))
        evm_ostp = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:OSTP:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:OSTP:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:OSTP:MAX?")))
        evm_pow = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:POW:AVER?")),
                          str2float(self.v.rec_cmd("FETC:CC1:SUMM:POW:MIN?")),
                          str2float(self.v.rec_cmd("FETC:CC1:SUMM:POW:MAX?")))
        evm_cres = EvmCase(str2float(self.v.rec_cmd("FETC:CC1:SUMM:CRES:AVER?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:CRES:MIN?")),
                           str2float(self.v.rec_cmd("FETC:CC1:SUMM:CRES:MAX?")))
        res_nr5g_evm = Nr5gEvm(evm_qpsk, evm_16qam, evm_64qam, evm_256qam, evm_all, evm_pch, evm_psig, evm_ferr,
                               evm_serr, evm_iqof, evm_gimb, evm_quad, evm_ostp, evm_pow, evm_cres)
        return res_nr5g_evm

    @with_goto
    def nr5g_multi_evm(self, mode: str, car_num: int, freq1: float, freq2: float, bw1: float, bw2: float,
                       loss: float, rel: float, att: int, cell_id_list: List[int],
                       is_exr: bool, is_ext: bool, delay: int,
                       is_create: bool, create_name: str, current_name: str, rename: Optional[str],
                       snap_path: str, is_hold: bool,
                       evm_mode: int = 0,
                       freq3: float = None, bw3: float = None
                       ) -> Optional[MultiEvm]:
        """

        :param mode:
        :param car_num:
        :param freq1:
        :param freq2:
        :param bw1:
        :param bw2:
        :param loss:
        :param rel:
        :param att:
        :param cell_id_list:
        :param is_exr:
        :param is_ext:
        :param delay:
        :param is_create:
        :param create_name:
        :param current_name:
        :param rename:
        :param snap_path:
        :param is_hold:
        :param hub:
        :param timing:
        :param limit:
        :param max_time:
        :param step:
        :param evm_mode: 0默认，设置后抓取数据；1只设置不抓数据；2不设置只抓数据
        :param freq3:
        :param bw3:
        :return:
        [CC1_EVM, CC2_EVM (, CC3_EVM)]
        [EVM PDSCH QPSK(%), EVM PDSCH 16QAM(%), EVM PDSCH 64QAM(%), EVM PDSCH 256QAM(%),
            0                   1                   2                   3
        EVM ALL(%), EVM Phys Channel(%), EVM Phys Signal(%),
            4           5                   6
        Frequency Error(Hz), Sampling Error(ppm),
            7                   8
        I/Q Offset(dB), I/Q Gain Imbalance(dB), I/Q Quadrature Error(¡ã),
            9               10                      11
        OSTP(dBm),
            12
        Power(dBm), Crest Factor(dB)]
            13          14
        """
        if evm_mode == 2:
            goto.res
        if is_create:
            self.v.send_cmd(f"INST:CRE:NEW NR5G, {create_name!r}")
        else:
            self.v.send_cmd(f"INST {current_name!r}")
            if rename is not None:
                self.v.send_cmd(f"INST:REN {current_name!r},{rename!r}")

        if car_num == 2:
            nr5g_t_mode1 = f"NR-FR1-{mode}__TDD_{bw1:g}MHz_30kHz"
            nr5g_t_mode2 = f"NR-FR1-{mode}__TDD_{bw2:g}MHz_30kHz"
            cell_id1, cell_id2 = cell_id_list if cell_id_list is not None else [1, 2]
            if not is_hold:
                self.v.send_cmd("CONF:NR5G:MEAS EVM")
                self.v.send_cmd("CONF:NR5G:NOCC 2")
                self.v.send_cmd("CONF:NR5G:DL:CC1:DFR MIDD")
                self.v.send_cmd("CONF:NR5G:DL:CC2:DFR MIDD")
                self.v.send_cmd(f"MMEM:LOAD:TMOD:CC1 {nr5g_t_mode1!r}")
                self.v.send_cmd(f"CONF:NR5G:DL:CC1:PLC:CID {cell_id1}")
                self.v.send_cmd(f"MMEM:LOAD:TMOD:CC2 {nr5g_t_mode2!r}")
                self.v.send_cmd(f"CONF:NR5G:DL:CC2:PLC:CID {cell_id2}")
                self.v.send_cmd("LAY:REM:WIND '3'")
                self.v.send_cmd("LAY:ADD:WIND? '4',LEFT,EVSY")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC1 {freq1} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC2 {freq2} MHz")
            self.v.send_cmd("CONF:NR5G:DL:CC1:RFUC:STAT OFF")
            self.v.send_cmd("CONF:NR5G:DL:CC2:RFUC:STAT OFF")
            self.v.send_cmd("CONF:NR5G:DL:CC1:IDC ON")
            self.v.send_cmd("CONF:NR5G:DL:CC2:IDC ON")
            self.v.send_cmd("SENS:NR5G:DEM:MCF ON")
        # three carriers
        else:
            nr5g_t_mode1 = f"NR-FR1-{mode}__TDD_{bw1:g}MHz_30kHz"
            nr5g_t_mode2 = f"NR-FR1-{mode}__TDD_{bw2:g}MHz_30kHz"
            nr5g_t_mode3 = f"NR-FR1-{mode}__TDD_{bw3:g}MHz_30kHz"
            cell_id1, cell_id2, cell_id3 = cell_id_list if cell_id_list is not None else [1, 2, 3]
            if not is_hold:
                self.v.send_cmd("CONF:NR5G:MEAS EVM")
                self.v.send_cmd("CONF:NR5G:NOCC 2")
                self.v.send_cmd("CONF:NR5G:DL:CC1:DFR MIDD")
                self.v.send_cmd("CONF:NR5G:DL:CC2:DFR MIDD")
                self.v.send_cmd("CONF:NR5G:DL:CC3:DFR MIDD")
                self.v.send_cmd(f"MMEM:LOAD:TMOD:CC1 {nr5g_t_mode1!r}")
                self.v.send_cmd(f"CONF:NR5G:DL:CC1:PLC:CID {cell_id1}")
                self.v.send_cmd(f"MMEM:LOAD:TMOD:CC2 {nr5g_t_mode2!r}")
                self.v.send_cmd(f"CONF:NR5G:DL:CC2:PLC:CID {cell_id2}")
                self.v.send_cmd(f"MMEM:LOAD:TMOD:CC3 {nr5g_t_mode3!r}")
                self.v.send_cmd(f"CONF:NR5G:DL:CC3:PLC:CID {cell_id3}")
                self.v.send_cmd("LAY:REM:WIND '3'")
                self.v.send_cmd("LAY:ADD:WIND? '4',LEFT,EVSY")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC1 {freq1} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC2 {freq2} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC3 {freq3} MHz")
            self.v.send_cmd("CONF:NR5G:DL:CC1:RFUC:STAT OFF")
            self.v.send_cmd("CONF:NR5G:DL:CC2:RFUC:STAT OFF")
            self.v.send_cmd("CONF:NR5G:DL:CC3:RFUC:STAT OFF")
            self.v.send_cmd("CONF:NR5G:DL:CC1:IDC ON")
            self.v.send_cmd("CONF:NR5G:DL:CC2:IDC ON")
            self.v.send_cmd("CONF:NR5G:DL:CC3:IDC ON")
            self.v.send_cmd("SENS:NR5G:DEM:MCF ON")

        if is_exr:
            self.v.send_cmd(":SENS:ROSC:SOUR E10")
        if is_ext:
            self.v.send_cmd("TRIG:SOUR EXT")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
        self.v.send_cmd(f"INP:ATT {att}dB")

        if evm_mode == 1:
            return
        label.res

        self.v.send_cmd("INIT:IMM;*WAI")

        # v.send_cmd("INIT:CONT OFF")
        # v.send_cmd("INIT;*WAI")
        # time.sleep(delay)
        countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

        if snap_path is not None:
            self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
            self.v.send_cmd("HCOP:DEV:LANG1 JPG")
            self.v.send_cmd("HCOP:CMAP:DEF4")
            self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
            self.v.send_cmd("HCOP:IMM1")

        res_nr5g_evm_list = []
        for i in range(1, car_num + 1):
            evm_qpsk = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSQP:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSQP:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSQP:MAX?")))
            evm_16qam = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSST:AVER?")),
                                str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSST:MIN?")),
                                str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSST:MAX?")))
            evm_64qam = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSSF:AVER?")),
                                str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSSF:MIN?")),
                                str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSSF:MAX?")))
            evm_256qam = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSTS:AVER?")),
                                 str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSTS:MIN?")),
                                 str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:DSTS:MAX?")))
            evm_all = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:AVER?")),
                              str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:MIN?")),
                              str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:MAX?")))
            evm_pch = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:PCH:AVER?")),
                              str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:PCH:MIN?")),
                              str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:PCH:MAX?")))
            evm_psig = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:PSIG:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:PSIG:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:EVM:PSIG:MAX?")))
            evm_ferr = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:FERR:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:FERR:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:FERR:MAX?")))
            evm_serr = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:SERR:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:SERR:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:SERR:MAX?")))
            evm_iqof = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:IQOF:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:IQOF:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:IQOF:MAX?")))
            evm_gimb = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:GIMB:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:GIMB:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:GIMB:MAX?")))
            evm_quad = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:QUAD:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:QUAD:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:QUAD:MAX?")))
            evm_ostp = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:OSTP:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:OSTP:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:OSTP:MAX?")))
            evm_pow = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:POW:AVER?")),
                              str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:POW:MIN?")),
                              str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:POW:MAX?")))
            evm_cres = EvmCase(str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:CRES:AVER?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:CRES:MIN?")),
                               str2float(self.v.rec_cmd(f"FETC:CC{i}:SUMM:CRES:MAX?")))
            res_nr5g_evm_list.append(
                Nr5gEvm(evm_qpsk, evm_16qam, evm_64qam, evm_256qam, evm_all, evm_pch, evm_psig, evm_ferr, evm_serr,
                        evm_iqof, evm_gimb, evm_quad, evm_ostp, evm_pow, evm_cres))
        res_nr5g_multi_evm = MultiEvm(*res_nr5g_evm_list)
        return res_nr5g_multi_evm

    def nr5g_sem(self, mode: str, freq1: float, bw1: float,
                 loss: float, rel: float, att: int, is_exr: bool, is_ext: bool, delay: int,
                 is_create: bool, create_name: str, current_name: str, rename: Optional[str],
                 snap_path: str, is_hold: bool,
                 gate_delay: Optional[float] = None, gate_length: Optional[float] = None,
                 stime_index: float = 0.1
                 ) -> Sem:
        """

        :param mode:
        :param freq1:
        :param bw1:
        :param loss:
        :param rel:
        :param att:
        :param is_exr:
        :param is_ext:
        :param delay:
        :param is_create:
        :param create_name:
        :param current_name:
        :param rename:
        :param snap_path:
        :param is_hold:
        :param gate_delay: ms
        :param gate_length: ms
        :param stime_index: ms / MHz
        :return:
        [TxPower(dBm), Range No, Start Freq Rel(MHz), Stop Freq Rel(MHz), RBW(MHz),
        Frequency at Delta to Limit(MHz), Power Abs(dBm), Power Rel(dB), Delta to Limit(dB), ...]
        4 Ranges Totally
        """
        nr5g_t_mode = f"NR-FR1-{mode}__TDD_{bw1:g}MHz_30kHz"
        if is_create:
            self.v.send_cmd(f"INST:CRE:NEW NR5G, {create_name!r}")
        else:
            self.v.send_cmd(f"INST {current_name!r}")
            if rename is not None:
                self.v.send_cmd(f"INST:REN {current_name!r},{rename!r}")

        if not is_hold:
            self.v.send_cmd("CONF:NR5G:MEAS ESP")
            self.v.send_cmd(f"MMEM:LOAD:TMOD:CC1 {nr5g_t_mode!r}")
            self.v.send_cmd("SENS:POW:CAT LARE")

        if is_exr:
            self.v.send_cmd(":SENS:ROSC:SOUR E10")
        if is_ext:
            self.v.send_cmd("TRIG:SOUR EXT")
            self.v.send_cmd("SENS:SWE:EGAT ON")
            self.v.send_cmd("SENS:SWE:EGAT:CONT:STAT ON")
            if gate_delay is not None:
                self.v.send_cmd(f"SENS:SWE:EGAT:HOLD {gate_delay}ms")
            if gate_length is not None:
                self.v.send_cmd(f"SENS:SWE:EGAT:LENG {gate_length}ms")

        self.v.send_cmd(f"FREQ:CENT {freq1} MHz")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
        self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
        # self.v.send_cmd("INIT:CONT OFF")

        self.v.send_cmd(
            "SENS:ESP1:PRES:STAN "
            fr"'C:\R_S\Instr\sem_std\NR5G\NR5G_SEM_DL_LocalArea_BW{bw1:g}_BASESTATIONTYPE_1_C_FSW.xml'")

        self.v.send_cmd("SENS:ESP1:RANG2:DEL")
        self.v.send_cmd("SENS:ESP1:RANG5:DEL")
        self.v.send_cmd(f"SENS:ESP1:RANG1:FREQ:STOP -{bw1 / 2 + 5.05} MHz")
        self.v.send_cmd(f"SENS:ESP1:RANG5:FREQ:STAR {bw1 / 2 + 5.05} MHz")
        for i in range(1, 6):
            self.v.send_cmd(f"SENS:ESP1:RANG{i}:INP:ATT {att}")
            st = abs(float(self.v.rec_cmd(f":SENS:ESP1:RANG{i}:FREQ:STAR?")) - float(
                self.v.rec_cmd(f":SENS:ESP1:RANG{i}:FREQ:STOP?"))) * 1e-6 * stime_index
            self.v.send_cmd(f":SENS:ESP1:RANG{i}:SWE:TIME {st}ms")
        self.v.send_cmd("SENS:ESP1:RANG2:LIM1:ABS:STAR -37")
        self.v.send_cmd("SENS:ESP1:RANG2:LIM1:ABS:STOP -30")
        self.v.send_cmd("SENS:ESP1:RANG4:LIM1:ABS:STAR -30")
        self.v.send_cmd("SENS:ESP1:RANG4:LIM1:ABS:STOP -37")

        # self.v.send_cmd("INIT:CONT OFF")
        self.v.send_cmd("INIT;*WAI")
        # time.sleep(delay)
        countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

        if snap_path is not None:
            self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
            self.v.send_cmd("HCOP:DEV:LANG1 JPG")
            self.v.send_cmd("HCOP:CMAP:DEF4")
            self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
            self.v.send_cmd("HCOP:IMM1")

        res_sem_range = []
        res = str2float(self.v.rec_cmd("TRAC:DATA? LIST").split(","))
        for i in range(4):
            res[1 + 11 * i: 5 + 11 * i] = hz2mhz(res[1 + 11 * i: 5 + 11 * i])
        while 0.0 in res:
            res.remove(0.0)
        for j in range(4):
            res_sem_range.append(SemRange(*res[8 * j: 8 * j + 8]))
        res_sem = Sem(str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW:RES? CPOW")),
                      None, None,
                      *res_sem_range)
        return res_sem

    def nr5g_multi_sem(self, mode: str, car_num: int, freq1: float, freq2: float, bw1: float, bw2: float,
                       loss: float, rel: float, att: int, is_exr: bool, is_ext: bool, delay: int,
                       is_create: bool, create_name: str, current_name: str, rename: Optional[str],
                       snap_path: str, is_hold: bool,
                       gate_delay: Optional[float] = None, gate_length: Optional[float] = None,
                       stime_index: float = 0.1,
                       freq3: float = None, bw3: float = None
                       ) -> Sem:
        """

        :param mode:
        :param car_num:
        :param freq1:
        :param freq2:
        :param bw1:
        :param bw2:
        :param loss:
        :param rel:
        :param att:
        :param is_exr:
        :param is_ext:
        :param delay:
        :param is_create:
        :param create_name:
        :param current_name:
        :param rename:
        :param snap_path:
        :param is_hold:
        :param gate_delay: ms
        :param gate_length: ms
        :param stime_index: ms / MHz
        :param freq3:
        :param bw3:
        :return:
        (1)sem_type == nr5g_two_carriers_s_gap_sem
        two continuous carriers and two carriers with gap <= 0.1M:
        [TxPower1(dBm), TxPower2(dBm), Range No, Start Freq Rel(MHz), Stop Freq Rel(MHz), RBW(MHz),
        Frequency at Delta to Limit(MHz), Power Abs(dBm), Power Rel(dB), Delta to Limit(dB), ...]
        4 Ranges Totally

        (2)sem_type == nr5g_two_carriers_m_gap_sem
        two carriers with 0.1M < gap <= 10.1M:
        6 Ranges Totally

        (3)sem_type == nr5g_two_carriers_l_gap_sem
        two carriers with gap > 10.1M:
        8 Ranges Totally

        (2)sem_type == nr5g_three_carriers_sem
        three continuous carriers:
        [TxPower1(dBm), TxPower2(dBm), TxPower3(dBm), Range No, Start Freq Rel(MHz), Stop Freq Rel(MHz), RBW(MHz),
        Frequency at Delta to Limit(MHz), Power Abs(dBm), Power Rel(dB), Delta to Limit(dB), ...]
        4 Ranges Totally
        """
        gap1 = freq2 - freq1 - bw1 / 2 - bw2 / 2
        if is_create:
            self.v.send_cmd(f"INST:CRE:NEW NR5G, {create_name!r}")
        else:
            self.v.send_cmd(f"INST {current_name!r}")
            if rename is not None:
                self.v.send_cmd(f"INST:REN {current_name!r},{rename!r}")

        if car_num == 2:
            nr5g_t_mode1 = f"NR-FR1-{mode}__TDD_{bw1:g}MHz_30kHz"
            nr5g_t_mode2 = f"NR-FR1-{mode}__TDD_{bw2:g}MHz_30kHz"
            if not is_hold:
                self.v.send_cmd("CONF:NR5G:MEAS MCESpectrum")
                self.v.send_cmd(f"MMEM:LOAD:TMOD:CC1 {nr5g_t_mode1!r}")
                self.v.send_cmd(f"MMEM:LOAD:TMOD:CC2 {nr5g_t_mode2!r}")
                self.v.send_cmd("SENS:POW:CAT LARE")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC1 {freq1} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC2 {freq2} MHz")

            if is_exr:
                self.v.send_cmd(":SENS:ROSC:SOUR E10")
            if is_ext:
                self.v.send_cmd("TRIG:SOUR EXT")
                self.v.send_cmd("SENS:SWE:EGAT ON")
                self.v.send_cmd("SENS:SWE:EGAT:CONT:STAT ON")
                if gate_delay is not None:
                    self.v.send_cmd(f"SENS:SWE:EGAT:HOLD {gate_delay}ms")
                if gate_length is not None:
                    self.v.send_cmd(f"SENS:SWE:EGAT:LENG {gate_length}ms")

            self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
            self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
            # self.v.send_cmd("INIT:CONT OFF")

            for i, bw in enumerate((bw1, bw2), 1):
                self.v.send_cmd(
                    f"SENS:ESP{i}:PRES:STAN "
                    fr"'C:\R_S\Instr\sem_std\NR5G\NR5G_SEM_DL_LocalArea_BW{bw:g}_BASESTATIONTYPE_1_C_FSW.xml'")
                self.v.send_cmd(f"SENS:ESP{i}:RANG2:DEL")
                self.v.send_cmd(f"SENS:ESP{i}:RANG5:DEL")
                self.v.send_cmd(f"SENS:ESP{i}:RANG1:FREQ:STOP -{bw / 2 + 5.05} MHz")
                self.v.send_cmd(f"SENS:ESP{i}:RANG5:FREQ:STAR {bw / 2 + 5.05} MHz")

                for j in range(1, 6):
                    self.v.send_cmd(f"SENS:ESP{i}:RANG{j}:INP:ATT {att}")
                self.v.send_cmd(f"SENS:ESP{i}:RANG2:LIM1:ABS:STAR -37")
                self.v.send_cmd(f"SENS:ESP{i}:RANG2:LIM1:ABS:STOP -30")
                self.v.send_cmd(f"SENS:ESP{i}:RANG4:LIM1:ABS:STAR -30")
                self.v.send_cmd(f"SENS:ESP{i}:RANG4:LIM1:ABS:STOP -37")
            if gap1 <= 0.1:
                num = 4
            elif 0.1 < gap1 <= 10.1:
                num = 6
                self.v.send_cmd("SENS:ESP1:RANG5:DEL")
                self.v.send_cmd(f"SENS:ESP1:RANG4:FREQ:STOP {bw1 / 2 + gap1 / 2} MHz")
                self.v.send_cmd("SENS:ESP2:RANG1:DEL")
                self.v.send_cmd(f"SENS:ESP2:RANG1:FREQ:STAR -{bw2 / 2 + gap1 / 2} MHz")
            # gap1 > 10.1
            else:
                num = 8
                self.v.send_cmd(f"SENS:ESP1:RANG5:FREQ:STOP {bw1 / 2 + gap1 / 2} MHz")
                self.v.send_cmd(f"SENS:ESP2:RANG1:FREQ:STAR -{bw2 / 2 + gap1 / 2} MHz")

            for n in range(1, 3):
                for m in range(1, 5 if num == 6 else 6):
                    st = abs(float(self.v.rec_cmd(f":SENS:ESP{n}:RANG{m}:FREQ:STAR?")) - float(
                        self.v.rec_cmd(f":SENS:ESP{n}:RANG{m}:FREQ:STOP?"))) * 1e-6 * stime_index
                    self.v.send_cmd(f":SENS:ESP{n}:RANG{m}:SWE:TIME {st}ms")
            # self.v.send_cmd("INIT:CONT OFF")
            self.v.send_cmd("LAY:SPL 1,2,54")
            self.v.send_cmd("INIT;*WAI")
            # time.sleep(delay)
            countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

            if snap_path is not None:
                self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
                self.v.send_cmd("HCOP:DEV:LANG1 JPG")
                self.v.send_cmd("HCOP:CMAP:DEF4")
                self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
                self.v.send_cmd("HCOP:IMM1")

            res = str2float(self.v.rec_cmd("TRAC:DATA? LIST").split(","))
            res_sem_range = []
            for i in range(num):
                res[1 + 11 * i: 5 + 11 * i] = hz2mhz(res[1 + 11 * i: 5 + 11 * i])
            while 0.0 in res:
                res.remove(0.0)
            for j in range(num):
                res_sem_range.append(SemRange(*res[8 * j: 8 * j + 8]))
            res_nr5g_multi_sem = Sem(str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW1:RES? CPOW")),
                                     str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW2:RES? CPOW")),
                                     None,
                                     *res_sem_range)

        # three carriers
        else:
            nr5g_t_mode1 = f"NR-FR1-{mode}__TDD_{bw1:g}MHz_30kHz"
            nr5g_t_mode2 = f"NR-FR1-{mode}__TDD_{bw2:g}MHz_30kHz"
            nr5g_t_mode3 = f"NR-FR1-{mode}__TDD_{bw3:g}MHz_30kHz"
            if not is_hold:
                self.v.send_cmd("CONF:NR5G:MEAS MCESpectrum")
                self.v.send_cmd(f"MMEM:LOAD:TMOD:CC1 {nr5g_t_mode1!r}")
                self.v.send_cmd(f"MMEM:LOAD:TMOD:CC2 {nr5g_t_mode2!r}")
                self.v.send_cmd(f"MMEM:LOAD:TMOD:CC3 {nr5g_t_mode3!r}")
                self.v.send_cmd("SENS:POW:CAT LARE")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC1 {freq1} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC2 {freq2} MHz")
            self.v.send_cmd(f"SENS:FREQ:CENT:CC3 {freq3} MHz")

            if is_exr:
                self.v.send_cmd(":SENS:ROSC:SOUR E10")
            if is_ext:
                self.v.send_cmd("TRIG:SOUR EXT")
                self.v.send_cmd("SENS:SWE:EGAT ON")
                self.v.send_cmd("SENS:SWE:EGAT:CONT:STAT ON")
                if gate_delay is not None:
                    self.v.send_cmd(f"SENS:SWE:EGAT:HOLD {gate_delay}ms")
                if gate_length is not None:
                    self.v.send_cmd(f"SENS:SWE:EGAT:LENG {gate_length}ms")

            self.v.send_cmd(f"DISP:TRAC:Y:RLEV:OFFS {loss}dB")
            self.v.send_cmd(f"DISP:TRAC:Y:RLEV {rel}dBm")
            # self.v.send_cmd("INIT:CONT OFF")

            for i, bw in enumerate((bw1, bw2, bw3), 1):
                self.v.send_cmd(
                    f"SENS:ESP{i}:PRES:STAN "
                    fr"'C:\R_S\Instr\sem_std\NR5G\NR5G_SEM_DL_LocalArea_BW{bw:g}_BASESTATIONTYPE_1_C_FSW.xml'")
                self.v.send_cmd(f"SENS:ESP{i}:RANG2:DEL")
                self.v.send_cmd(f"SENS:ESP{i}:RANG5:DEL")
                self.v.send_cmd(f"SENS:ESP{i}:RANG1:FREQ:STOP -{float(bw) / 2 + 5.05} MHz")
                self.v.send_cmd(f"SENS:ESP{i}:RANG5:FREQ:STAR {float(bw) / 2 + 5.05} MHz")

                for j in range(1, 6):
                    self.v.send_cmd(f"SENS:ESP{i}:RANG{j}:INP:ATT {att}")
                self.v.send_cmd(f"SENS:ESP{i}:RANG2:LIM1:ABS:STAR -37")
                self.v.send_cmd(f"SENS:ESP{i}:RANG2:LIM1:ABS:STOP -30")
                self.v.send_cmd(f"SENS:ESP{i}:RANG4:LIM1:ABS:STAR -30")
                self.v.send_cmd(f"SENS:ESP{i}:RANG4:LIM1:ABS:STOP -37")
            num = 4

            for n in range(1, 4):
                for m in range(1, 6):
                    st = abs(float(self.v.rec_cmd(f":SENS:ESP{n}:RANG{m}:FREQ:STAR?")) - float(
                        self.v.rec_cmd(f":SENS:ESP{n}:RANG{m}:FREQ:STOP?"))) * 1e-6 * stime_index
                    self.v.send_cmd(f":SENS:ESP{n}:RANG{m}:SWE:TIME {st}ms")
            # self.v.send_cmd("INIT:CONT OFF")
            self.v.send_cmd("LAY:SPL 1,2,54")
            self.v.send_cmd("INIT;*WAI")
            # time.sleep(delay)
            countdown(delay, f"Waiting to get {current_name} result", f"{current_name} Testing complete!")

            if snap_path is not None:
                self.v.send_cmd("HCOP:DEST 'SYST:COMM:MMEM'")
                self.v.send_cmd("HCOP:DEV:LANG1 JPG")
                self.v.send_cmd("HCOP:CMAP:DEF4")
                self.v.send_cmd(f"MMEM:NAME {snap_path!r}")
                self.v.send_cmd("HCOP:IMM1")

            res = str2float(self.v.rec_cmd("TRAC:DATA? LIST").split(","))
            res_sem_range = []
            for i in range(num):
                res[1 + 11 * i: 5 + 11 * i] = hz2mhz(res[1 + 11 * i: 5 + 11 * i])
            while 0.0 in res:
                res.remove(0.0)
            for j in range(num):
                res_sem_range.append(SemRange(*res[8 * j: 8 * j + 8]))
            res_nr5g_multi_sem = Sem(str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW1:RES? CPOW")),
                                     str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW2:RES? CPOW")),
                                     str2float(self.v.rec_cmd("CALC:MARK:FUNC:POW3:RES? CPOW")),
                                     *res_sem_range)
        return res_nr5g_multi_sem
