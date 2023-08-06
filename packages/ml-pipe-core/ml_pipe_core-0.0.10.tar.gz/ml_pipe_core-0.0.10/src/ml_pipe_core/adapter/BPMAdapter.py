import numpy as np
import time
import csv
from typing import Dict, Tuple

from ml_pipe_core.adapter.bpm_fit import correct_bpm
from ml_pipe_core.logger import logging


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class BPM:
    def __init__(self, bpm_type, path_to_calibr_files):
        bpm_file = bpm_type+'.par'
        calibr_file = path_to_calibr_files / "common" / bpm_file
        colmat = np.loadtxt(calibr_file)
        self.cx = [r[0] for r in colmat]
        self.cy = [r[1] for r in colmat]

    def correct_x(self, x):
        x_ = 0.0
        for i in range(len(self.cx)):
            x_ += self.cx[i] * x**i
        return x_

    def correct_y(self, y):
        y_ = 0.0
        for i in range(len(self.cy)):
            y_ += self.cy[i] * y**i
        return y_


class BPMAdapter:
    def __init__(self, read, path_to_calibr_files, path_to_constants_file, units='mm'):
        # self.bpm_names = ['bpm_swr_13', 'bpm_swr_31', 'bpm_swr_46', 'bpm_swr_61', 'bpm_swr_75', 'bpm_swr_90', 'bpm_swr_104', 'bpm_swr_118', 'bpm_swr_133', 'bpm_wl_140', 'bpm_wl_126', 'bpm_wl_111', 'bpm_wl_97', 'bpm_wl_82', 'bpm_wl_68', 'bpm_wl_53', 'bpm_wl_36', 'bpm_wl_30', 'bpm_wl_24', 'bpm_wl_18', 'bpm_wl_12', 'bpm_wl_6', 'bpm_wr_0', 'bpm_wr_7', 'bpm_wr_13', 'bpm_wr_19', 'bpm_wr_25', 'bpm_wr_31', 'bpm_wr_37', 'bpm_wr_56', 'bpm_wr_68', 'bpm_wr_82', 'bpm_wr_97', 'bpm_wr_111', 'bpm_wr_126', 'bpm_wr_140', 'bpm_nwl_133', 'bpm_nwl_118', 'bpm_nwl_104', 'bpm_nwl_90', 'bpm_nwl_75', 'bpm_nwl_61', 'bpm_nwl_46', 'bpm_nwl_31', 'bpm_nwl_13', 'bpm_nwl_1', 'bpm_nwr_13', 'bpm_nwr_31', 'bpm_nwr_46', 'bpm_nwr_61', 'bpm_nwr_75', 'bpm_nwr_90', 'bpm_nwr_104', 'bpm_nwr_118', 'bpm_nwr_133', 'bpm_nl_140', 'bpm_nl_126', 'bpm_nl_111', 'bpm_nl_97', 'bpm_nl_82', 'bpm_nl_68', 'bpm_nl_53', 'bpm_nl_36', 'bpm_nl_30', 'bpm_nl_24', 'bpm_nl_18', 'bpm_nl_12', 'bpm_nl_6', 'bpm_nr_0', 'bpm_nr_7', 'bpm_nr_13', 'bpm_nr_19', 'bpm_nr_25', 'bpm_nr_31', 'bpm_nr_37', 'bpm_nr_56', 'bpm_nr_62', 'bpm_nr_65', 'bpm_nr_69', 'bpm_nr_74', 'bpm_nr_79', 'bpm_nr_83', 'bpm_nr_87', 'bpm_nr_90', 'bpm_nr_96', 'bpm_nr_100', 'bpm_nr_104', 'bpm_nr_111', 'bpm_nr_126', 'bpm_nr_140', 'bpm_nol_133', 'bpm_nol_118', 'bpm_nol_104', 'bpm_nol_90', 'bpm_nol_75', 'bpm_nol_61', 'bpm_nol_46', 'bpm_nol_31', 'bpm_nol_10', 'bpm_nor_6', 'bpm_nor_11', 'bpm_nor_23', 'bpm_nor_32', 'bpm_nor_39', 'bpm_nor_40', 'bpm_nor_44', 'bpm_nor_47', 'bpm_nor_50', 'bpm_nor_52', 'bpm_nor_55', 'bpm_nor_58', 'bpm_nor_62', 'bpm_nor_63', 'bpm_nor_67', 'bpm_nor_70', 'bpm_nor_73', 'bpm_nor_78', 'bpm_nor_81', 'bpm_nor_85', 'bpm_nor_86', 'bpm_nor_90', 'bpm_nor_93', 'bpm_nor_96',
        #                  'bpm_nor_98', 'bpm_nor_101', 'bpm_nor_104', 'bpm_nor_108', 'bpm_nor_109', 'bpm_nor_113', 'bpm_nor_116', 'bpm_nor_119', 'bpm_nor_124', 'bpm_nor_127', 'bpm_nor_131', 'bpm_nor_132', 'bpm_ol_152', 'bpm_ol_149', 'bpm_ol_146', 'bpm_ol_144', 'bpm_ol_141', 'bpm_ol_138', 'bpm_ol_134', 'bpm_ol_133', 'bpm_ol_129', 'bpm_ol_126', 'bpm_ol_123', 'bpm_ol_118', 'bpm_ol_115', 'bpm_ol_111', 'bpm_ol_110', 'bpm_ol_106', 'bpm_ol_103', 'bpm_ol_100', 'bpm_ol_98', 'bpm_ol_95', 'bpm_ol_92', 'bpm_ol_88', 'bpm_ol_87', 'bpm_ol_83', 'bpm_ol_80', 'bpm_ol_77', 'bpm_ol_75', 'bpm_ol_72', 'bpm_ol_69', 'bpm_ol_65', 'bpm_ol_64', 'bpm_ol_60', 'bpm_ol_58', 'bpm_ol_48', 'bpm_ol_37', 'bpm_ol_24', 'bpm_ol_13', 'bpm_ol_0', 'bpm_or_8', 'bpm_or_17', 'bpm_or_22', 'bpm_or_26', 'bpm_or_32', 'bpm_or_37', 'bpm_or_44', 'bpm_or_53', 'bpm_or_62', 'bpm_or_65', 'bpm_or_69', 'bpm_or_74', 'bpm_or_79', 'bpm_or_83', 'bpm_or_87', 'bpm_or_90', 'bpm_or_96', 'bpm_or_100', 'bpm_or_104', 'bpm_or_111', 'bpm_or_126', 'bpm_or_140', 'bpm_sol_133', 'bpm_sol_118', 'bpm_sol_104', 'bpm_sol_90', 'bpm_sol_75', 'bpm_sol_61', 'bpm_sol_54', 'bpm_sol_46', 'bpm_sol_31', 'bpm_sol_13', 'bpm_sol_1', 'bpm_sor_13', 'bpm_sor_31', 'bpm_sor_46', 'bpm_sor_61', 'bpm_sor_75', 'bpm_sor_90', 'bpm_sor_104', 'bpm_sor_118', 'bpm_sor_133', 'bpm_sl_140', 'bpm_sl_126', 'bpm_sl_111', 'bpm_sl_97', 'bpm_sl_82', 'bpm_sl_68', 'bpm_sl_53', 'bpm_sl_36', 'bpm_sl_24', 'bpm_sl_6', 'bpm_sr_6', 'bpm_sr_24', 'bpm_sr_36', 'bpm_sr_53', 'bpm_sr_68', 'bpm_sr_82', 'bpm_sr_97', 'bpm_sr_111', 'bpm_sr_126', 'bpm_sr_140', 'bpm_swl_133', 'bpm_swl_118', 'bpm_swl_104', 'bpm_swl_90', 'bpm_swl_75', 'bpm_swl_61', 'bpm_swl_46', 'bpm_swl_39', 'bpm_swl_31', 'bpm_swl_13', 'bpm_swl_1']

        self.bpm_names = ['BPM_SWR_13', 'BPM_SWR_31', 'BPM_SWR_46', 'BPM_SWR_61', 'BPM_SWR_75', 'BPM_SWR_90', 'BPM_SWR_104', 'BPM_SWR_118', 'BPM_SWR_133', 'BPM_WL_140', 'BPM_WL_126', 'BPM_WL_111', 'BPM_WL_97', 'BPM_WL_82', 'BPM_WL_68', 'BPM_WL_53', 'BPM_WL_36', 'BPM_WL_30', 'BPM_WL_24', 'BPM_WL_18', 'BPM_WL_12', 'BPM_WL_6', 'BPM_WR_0', 'BPM_WR_7', 'BPM_WR_13', 'BPM_WR_19', 'BPM_WR_25', 'BPM_WR_31', 'BPM_WR_37', 'BPM_WR_56', 'BPM_WR_68', 'BPM_WR_82', 'BPM_WR_97', 'BPM_WR_111', 'BPM_WR_126', 'BPM_WR_140', 'BPM_NWL_133', 'BPM_NWL_118', 'BPM_NWL_104', 'BPM_NWL_90', 'BPM_NWL_75', 'BPM_NWL_61', 'BPM_NWL_46', 'BPM_NWL_31', 'BPM_NWL_13', 'BPM_NWL_1', 'BPM_NWR_13', 'BPM_NWR_31', 'BPM_NWR_46', 'BPM_NWR_61', 'BPM_NWR_75', 'BPM_NWR_90', 'BPM_NWR_104', 'BPM_NWR_118', 'BPM_NWR_133', 'BPM_NL_140', 'BPM_NL_126', 'BPM_NL_111', 'BPM_NL_97', 'BPM_NL_82', 'BPM_NL_68', 'BPM_NL_53', 'BPM_NL_36', 'BPM_NL_30', 'BPM_NL_24', 'BPM_NL_18', 'BPM_NL_12', 'BPM_NL_6', 'BPM_NR_0', 'BPM_NR_7', 'BPM_NR_13', 'BPM_NR_19', 'BPM_NR_25', 'BPM_NR_31', 'BPM_NR_37', 'BPM_NR_56', 'BPM_NR_62', 'BPM_NR_65', 'BPM_NR_69', 'BPM_NR_74', 'BPM_NR_79', 'BPM_NR_83', 'BPM_NR_87', 'BPM_NR_90', 'BPM_NR_96', 'BPM_NR_100', 'BPM_NR_104', 'BPM_NR_111', 'BPM_NR_126', 'BPM_NR_140', 'BPM_NOL_133', 'BPM_NOL_118', 'BPM_NOL_104', 'BPM_NOL_90', 'BPM_NOL_75', 'BPM_NOL_61', 'BPM_NOL_46', 'BPM_NOL_31', 'BPM_NOL_10', 'BPM_NOR_6', 'BPM_NOR_11', 'BPM_NOR_23', 'BPM_NOR_32', 'BPM_NOR_39', 'BPM_NOR_40', 'BPM_NOR_44', 'BPM_NOR_47', 'BPM_NOR_50', 'BPM_NOR_52', 'BPM_NOR_55', 'BPM_NOR_58', 'BPM_NOR_62', 'BPM_NOR_63', 'BPM_NOR_67', 'BPM_NOR_70', 'BPM_NOR_73', 'BPM_NOR_78', 'BPM_NOR_81', 'BPM_NOR_85', 'BPM_NOR_86', 'BPM_NOR_90', 'BPM_NOR_93', 'BPM_NOR_96',
                          'BPM_NOR_98', 'BPM_NOR_101', 'BPM_NOR_104', 'BPM_NOR_108', 'BPM_NOR_109', 'BPM_NOR_113', 'BPM_NOR_116', 'BPM_NOR_119', 'BPM_NOR_124', 'BPM_NOR_127', 'BPM_NOR_131', 'BPM_NOR_132', 'BPM_OL_152', 'BPM_OL_149', 'BPM_OL_146', 'BPM_OL_144', 'BPM_OL_141', 'BPM_OL_138', 'BPM_OL_134', 'BPM_OL_133', 'BPM_OL_129', 'BPM_OL_126', 'BPM_OL_123', 'BPM_OL_118', 'BPM_OL_115', 'BPM_OL_111', 'BPM_OL_110', 'BPM_OL_106', 'BPM_OL_103', 'BPM_OL_100', 'BPM_OL_98', 'BPM_OL_95', 'BPM_OL_92', 'BPM_OL_88', 'BPM_OL_87', 'BPM_OL_83', 'BPM_OL_80', 'BPM_OL_77', 'BPM_OL_75', 'BPM_OL_72', 'BPM_OL_69', 'BPM_OL_65', 'BPM_OL_64', 'BPM_OL_60', 'BPM_OL_58', 'BPM_OL_48', 'BPM_OL_37', 'BPM_OL_24', 'BPM_OL_13', 'BPM_OL_0', 'BPM_OR_8', 'BPM_OR_17', 'BPM_OR_22', 'BPM_OR_26', 'BPM_OR_32', 'BPM_OR_37', 'BPM_OR_44', 'BPM_OR_53', 'BPM_OR_62', 'BPM_OR_65', 'BPM_OR_69', 'BPM_OR_74', 'BPM_OR_79', 'BPM_OR_83', 'BPM_OR_87', 'BPM_OR_90', 'BPM_OR_96', 'BPM_OR_100', 'BPM_OR_104', 'BPM_OR_111', 'BPM_OR_126', 'BPM_OR_140', 'BPM_SOL_133', 'BPM_SOL_118', 'BPM_SOL_104', 'BPM_SOL_90', 'BPM_SOL_75', 'BPM_SOL_61', 'BPM_SOL_54', 'BPM_SOL_46', 'BPM_SOL_31', 'BPM_SOL_13', 'BPM_SOL_1', 'BPM_SOR_13', 'BPM_SOR_31', 'BPM_SOR_46', 'BPM_SOR_61', 'BPM_SOR_75', 'BPM_SOR_90', 'BPM_SOR_104', 'BPM_SOR_118', 'BPM_SOR_133', 'BPM_SL_140', 'BPM_SL_126', 'BPM_SL_111', 'BPM_SL_97', 'BPM_SL_82', 'BPM_SL_68', 'BPM_SL_53', 'BPM_SL_36', 'BPM_SL_24', 'BPM_SL_6', 'BPM_SR_6', 'BPM_SR_24', 'BPM_SR_36', 'BPM_SR_53', 'BPM_SR_68', 'BPM_SR_82', 'BPM_SR_97', 'BPM_SR_111', 'BPM_SR_126', 'BPM_SR_140', 'BPM_SWL_133', 'BPM_SWL_118', 'BPM_SWL_104', 'BPM_SWL_90', 'BPM_SWL_75', 'BPM_SWL_61', 'BPM_SWL_46', 'BPM_SWL_39', 'BPM_SWL_31', 'BPM_SWL_13', 'BPM_SWL_1']#, 'BPM_SOR_67', 'BPM_SOL_24']
        self.bpm_names = [p.upper() for p in self.bpm_names]
        # self.bpm_names = [name for name in self.bpm_names if name not in ['BPM_NR_9','BPM_NOR_52','BPM_NOR_98','BPM_OL_144','BPM_OL_98', "BPM_OL_75", "BPM_OR_74", "BPM_NOR_104"]] # BPM_OR_74 was broken on 18.8.2021
        self.units = units
        scales = {'nm': 1, 'mum': 1e-3, 'mm': 1e-6, 'm': 1e-9}
        self.scale = scales[units]
        self.path_to_calibr_files = path_to_calibr_files
        self.read = read

        # Constants to calculate the bpm beam current
        self.constants: Dict[str, Tuple[int, int]] = {}
        if path_to_constants_file:
            with open(path_to_constants_file) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.constants[row['name']] = (row['c0'], row['c1'])
            _logger.debug(f"Constants loaded: length {len(self.constants)}")

        with open(self.path_to_calibr_files / "BPMsettings.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            devices = []
            bpm_types = []
            for row in reader:
                devices.append(row['Device'])
                bpm_types.append(row['BPMTYP'])

        self.bpm_info = {device: bpm_type for device, bpm_type in zip(devices, bpm_types)}

        self.load_calibration(set(bpm_types))

    def load_calibration(self, bpm_types):
        self.PQ = {}

        for bpm_t in bpm_types:
            bpm = BPM(bpm_t, path_to_calibr_files=self.path_to_calibr_files)
            self.PQ[bpm_t] = (bpm.cx, bpm.cy)

        return

    def get_names(self, start_with):
        start_i = self.bpm_names.index(start_with)
        names = self.bpm_names[start_i:]+self.bpm_names[:start_i]  # realign names to start from start_with
        return start_i, names

    def _read(self, n_turns=10, start_with="BPM_SOR_61", is_corrected=True):
        start_i, names = self.get_names(start_with)

        res = np.zeros((len(names), n_turns, 2))

        for i, name in enumerate(names):
            for k in range(3):
                try:
                    res[i, :, 0] = np.array(self.read('/PETRA/LBRENV', name, 'DD_X', size=n_turns, mode='SYNC'))
                    res[i, :, 1] = np.array(self.read('/PETRA/LBRENV', name, 'DD_Y', size=n_turns, mode='SYNC'))
                    break
                except Exception as e:
                    print(f'attempt {k}:', e)
                    time.sleep(1)

        if is_corrected:
            res = self.correct(res, names)
        return res, names

    def read_sum(self, n_turns=10, start_with="BPM_SOR_61", is_corrected=True):
        start_i, names = self.get_names(start_with)

        res = np.zeros((len(names), n_turns, 1))

        for i, name in enumerate(names):
            for k in range(3):
                try:
                    res[i, :, 0] = np.array(self.read('/PETRA/LBRENV', name, 'DD_SUM', size=n_turns, mode='SYNC'))
                    break
                except Exception as e:
                    print(f'attempt {k}:', e)
                    time.sleep(1)

        return res, names

    def correct(self, res, names, scale=1e-6):
        res *= scale
        print(res.shape)
        res_cor = np.empty_like(res)
        for i, name in enumerate(names):
            PQ = self.PQ[self.bpm_info[name]]
            x, y = correct_bpm(res[i, :, 0], res[i, :, 1], PQ[0], PQ[1])
            res_cor[i, :, 0] = x
            res_cor[i, :, 1] = y
        return res_cor/scale

    def get_reference(self, start_with="BPM_SOR_61"):
        # start_with = "BPM_SWR_13"
        name0 = self.bpm_names[0]
        x = np.array(self.read('/PETRA/REFORBIT/', name0, 'SA_X'))
        y = np.array(self.read('/PETRA/REFORBIT/', name0, 'SA_Y'))
        res = np.vstack((x, y)).T
        res = res[:-2]

        start_i, names = self.get_names(start_with)
        return np.roll(res, -start_i, axis=0)*self.scale, names

    def get_offsets(self, start_with="BPM_SOR_61"):
        name0 = self.bpm_names[0]
        x = np.array(self.read('/PETRA/REFORBIT', name0, 'CORR_X_BBA'))
        y = np.array(self.read('/PETRA/REFORBIT/', name0, 'CORR_Y_BBA'))
        res = np.vstack((x, y)).T
        res = res[:-2]

        start_i, names = self.get_names(start_with)
        return np.roll(res, -start_i, axis=0)*self.scale, names

    def get_offsets_go(self, start_with="BPM_SOR_61"):
        name0 = self.bpm_names[0]
        # x = np.array(self.read('/PETRA/REFORBIT/', name0,'SA_X')['data'])*self.scale
        x = np.array(self.read('/PETRA/REFORBIT', name0, 'CORR_X_BBAGO'))
        y = np.array(self.read('/PETRA/REFORBIT', name0, 'CORR_Y_BBAGO'))
        res = np.vstack((x, y)).T
        res = res[:-2]
        start_i, names = self.get_names(start_with)
        return np.roll(res, -start_i, axis=0)*self.scale, names

    def get_orbit(self, start_with="BPM_SOR_61"):
        name0 = self.bpm_names[0]
        # x = np.array(self.read('/PETRA/REFORBIT/', name0,'SA_X')['data'])*self.scale
        x = np.array(self.read('/PETRA/LBRENV', name0, 'SA_X'))
        y = np.array(self.read('/PETRA/LBRENV', name0, 'SA_Y'))
        res = np.vstack((x, y)).T
        res = res[:-2]
        start_i, names = self.get_names(start_with)
        return np.roll(res, -start_i, axis=0)*self.scale, names

    def get_bpm_beam_currents(self, n_turns=10):
        if self.c0 == None or self.c1 == None:
            _logger.error(f"Constants c0, c1 are not set. c0={self.c0} and c1={self.c1}")
            return None, None
        sum_signal, names = self.read_sum(n_turns=n_turns)
        n_bpms = len(names)
        currents = np.zeros([n_bpms, n_turns])

        for i, name in enumerate(names):
            c0, c1 = self.constants.get(name)
            currents[i] = c0 + c1 * sum_signal[i, :, 0]
        return currents, names


if __name__ == "__main__":
    adapter = BPMAdapter()
    data, names = adapter.get_orbit()
