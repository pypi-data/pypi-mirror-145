from pathlib import Path

from typing import List, Tuple, Optional, Dict, Any

import numpy as np

from .BPMAdapter import BPMAdapter
from ..config import PATH_TO_ML_PIPE_SERVICES_ROOT
from ..logger import init_logger
from ..adapter.simulation_db_types import TABLE_NAMES
from ..adapter.MsgBusWriter import MessageBusWriter


_logger = init_logger(__name__)


def find_index_in_list(l: List[str], elements: List[str]) -> Tuple[bool, Optional[int]]:
    """[summary]
    Iterates over elements and yield a Tuple with element, True and index in list , if the current element is l. If not is returns (None, False, None)
        Example:
            find_index_in_list(['a','c','b'], ['a', 'b', 'c', 'd'])
            (('a', True, 0), ('b', True, 2), ('c', True, 1), ('d', False, None))
    :param l: List in which the elements will be searched. Have to be a subset of elements
    :type l: List[str]
    :param elements: elements that should be find.
    :type elements: List[str]
    :raises ValueError: If l is not a subset of elements
    :return: Yields a tuple at each step. The first element is a boolean which is True if the current element is in in_l, the second
            element is the index of the current element in in_l. If the current element is not in in_l (False, None) is yield.
    :rtype: Tuple[str, bool, Optional[int]]
    :yield: Yields a tuple at each step. The first element is the element which should be found, the second a boolean which is True if the current element is in the list, the third
            element is the index of the element in the list. If the current element is not in in_l (element, False, None) is yield.
    :rtype: Iterator[str, Tuple[bool, Optional[int]]]
    """
    names_indices = {k: v for v, k in enumerate(l)}
    found_idx_count = 0
    for name in elements:
        found_idx = names_indices.get(name)
        if found_idx != None:
            found_idx_count += 1
            yield name, True, found_idx
        else:
            yield name, False, None
    if found_idx_count != len(l):
        raise ValueError("l is not a subset of elements")


class PetraMachineAdapter():
    def __init__(self, write, read, energy=6.063, bpm_unit='mm'):

        rpath_to_bpm_calibr_files = Path(PATH_TO_ML_PIPE_SERVICES_ROOT) / Path("adapter/petra/config")
        path_to_bpm_calibr_files = rpath_to_bpm_calibr_files / "bpm_settings"
        filepath_to_constants_file = rpath_to_bpm_calibr_files / "constants.csv"
        self.bpm_adapter = BPMAdapter(read=read, units=bpm_unit, path_to_calibr_files=path_to_bpm_calibr_files, path_to_constants_file=filepath_to_constants_file)
        self.debug_mode = False
        self.energy = energy
        self.get_property = 'Strength.Soll'
        self.read = read
        self.write = write

    @classmethod
    def create_for_agent(cls, is_simulation=True, energy=6.063, bpm_unit='mm'):
        if is_simulation:
            from .TineSimAdapter import TineSimReader, PetraSimDatabase
            return cls(write=MessageBusWriter(PetraSimDatabase()), read=TineSimReader(PetraSimDatabase()), energy=energy, bpm_unit=bpm_unit)
        else:
            from .TineAdapter import TineReader
            return cls(write=MessageBusWriter(), read=TineReader(), energy=energy, bpm_unit=bpm_unit)

    @classmethod
    def create_for_simulation(cls, energy=6.063, bpm_unit='mm'):
        from .TineSimAdapter import TineSimReader, TineSimWriter, PetraSimDatabase
        return cls(write=TineSimWriter(PetraSimDatabase()), read=TineSimReader(PetraSimDatabase()), energy=energy, bpm_unit=bpm_unit)

    @classmethod
    def create_for_machine(cls, energy=6.063, bpm_unit='mm'):
        from .TineAdapter import TineReader, TineWriter
        return cls(write=TineWriter(), read=TineReader(), energy=energy, bpm_unit=bpm_unit)

    def get_bpm_device_names(self):
        # TODO: This has to be implemented with tine channels
        return self.bpm_adapter.bpm_names

    def get_values_by_group(self, group: str):
        group_res = self.read("/PETRA/Cms.PsGroup", group, self.get_property, size=self.get_hcor_device_names() if 'PeCorH' else self.get_vcor_device_names())
        print(f'read {group}: {len(group_res)} values')
        return group_res

    def get_value(self, name):
        return self.read("/PETRA/Cms.MagnetPs", name, self.get_property)

    def get_values_by_names(self, names):
        result = []
        for name in names:
            try:
                res = self.get_value(name)
                result.append(res)
            except Exception as e:
                print(name, e)
        return result

    def get_hcor_device_names(self, apply_filter=True) -> List[str]:
        device = 'PeCorH'
        cor_group_size = self.read("/PETRA/Cms.PsGroup", device, "GroupSize")
        names = self.read("/PETRA/Cms.PsGroup", device, "GroupDevices", size=cor_group_size)
        return names

    def get_vcor_device_names(self, apply_filter=True):
        device = 'PeCorV'
        cor_group_size = self.read("/PETRA/Cms.PsGroup", device, "GroupSize")
        names = self.read("/PETRA/Cms.PsGroup", device, "GroupDevices", size=cor_group_size)
        return names

    def _sort_by_hash_table(self, names: List[str], hash: Dict[str, int]):
        """[summary]
        Sorts a list of names by a index hash table.
        :param names: List of names in uppercase. Note: The names have to be in the hash table
        :type names: List[str]
        :param hash: name to idx hash table
        :type hash: Dict[str, int]
        :raises KeyError: If names are not in the group
        :return: A list of indices
        :rtype: [type]
        """
        indices = []
        for name in names:
            found_idx = hash.get(name)
            if found_idx == None:
                raise KeyError(f"name {name} is not in {hash} group.")
            indices.append(found_idx)
        return indices

    def get_cor_parallel(self, names: List[str], group='PeCorH') -> List[float]:
        all_corr_names = self.get_hcor_device_names() if group == 'PeCorH' else self.get_vcor_device_names()
        indices = self._sort_by_hash_table(names=names, hash={name: idx for idx, name in enumerate(all_corr_names)})

        currents = self.get_values_by_group(group)
        filtered_currents = [currents[idx] for idx in indices]
        print(f"names: len {len(names)} curr len {len(filtered_currents)}")
        return filtered_currents

    def get_cor_serial(self, names: List[str]) -> List[float]:
        currents = []
        for name in names:
            currents.append(self.get_value(name))
        return currents

    def get_hcors(self, names: List[str], is_group_call=True) -> List[float]:
        strengths = []
        if is_group_call:
            strengths = self.get_cor_parallel(names, group='PeCorH')
        else:
            strengths = self.get_cor_serial(names)

        return strengths

    def get_vcors(self, names: List[str], is_group_call=True) -> List[float]:
        strengths = []
        if is_group_call:
            strengths = self.get_cor_parallel(names, group='PeCorV')
        else:
            strengths = self.get_cor_serial(names)
        return strengths

    def set_group_values(self, name, values):
        if self.debug_mode:
            print(f"Debug Mode set_group_value: name: {name} values: {values}")
        else:
            address = f"/PETRA/Cms.PsGroup/{name}"
            print(address)
            print(len(values))
            print(type(values))
            print(self.get_property)
            self.write("/PETRA/Cms.PsGroup", name, self.get_property,
                       input=values,
                       format='FLOAT',
                       size=len(values),
                       mode='WRITE')

        return

    def set_value(self, name, value):
        if self.debug_mode:
            print(f"Debug Mode set_value: name: {name} value: {value}")
        else:
            self.write(f"/PETRA/Cms.MagnetPs", name, self.get_property, index=value)

    def set_cor_parallel(self, names: List[str], in_strenghts: List[float], current_offsets: List[float] = None, group='PeCorV'):
        strenghts_of_all_magnets = []
        print(f"names: len {len(names)} current len {len(in_strenghts)}")

        for name, is_ele_in_list, found_idx in find_index_in_list(l=names, elements=self.get_vcor_device_names() if group == 'PeCorV' else self.get_hcor_device_names()):
            if is_ele_in_list:
                strenghts_of_all_magnets.append(in_strenghts[found_idx])
                print(f"name: {name}, current: {in_strenghts[found_idx]}. use new value")
            else:  # magnet is not set
                curr = self.get_value(name)
                strenghts_of_all_magnets.append(curr)  # use current value of magnet
                print(f"name: {name}, current: {curr}. use old value")
        self.set_group_values(group, strenghts_of_all_magnets)

    def set_cor_serial(self, names: List[str], in_strenghts: List[float], current_offsets: List[float] = None):

        for name, current in zip(names, in_strenghts):
            print(f"name: {name}, current: {current}.")
            self.set_value(name, current)

    def set_vcors(self, names: List[str], in_strenghts: List[float], current_offsets: List[float] = None, is_group_call=True):
        if is_group_call:
            self.set_cor_parallel(names, in_strenghts, current_offsets=current_offsets, group='PeCorV')
        else:
            self.set_cor_serial(names, in_strenghts)

    def set_hcors(self, names: List[str], in_strenghts: List[float], current_offsets: List[float] = None, is_group_call=True):
        if is_group_call:
            self.set_cor_parallel(names, in_strenghts, current_offsets=current_offsets, group='PeCorH')
        else:
            self.set_cor_serial(names, in_strenghts)

    def get_bpms(self) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        data, names = self.bpm_adapter.get_orbit()
        off_go, _ = self.bpm_adapter.get_offsets_go()
        x = data[:, 0] - off_go[:, 0]  # - ref[:,0]
        y = data[:, 1] - off_go[:, 1]  # - ref[:,1]
        return x, y, names

    def set_machine_params(self, params: List[str], values: List[Any]):
        self.write("/SIMULATION/PETRA/DB", TABLE_NAMES.MACHINE_PARMS, 'SQL', input=[[('param', param), ('value', val)] for param, val in zip(params, values)], where_key='param')

    def get_machine_params(self):
        col_names = ['param', 'value']
        param_values_pairs = self.read("/SIMULATION/PETRA/DB", TABLE_NAMES.MACHINE_PARMS, "SQL", col_names=col_names)
        return {param_values_pair[0]: param_values_pair[1] for param_values_pair in param_values_pairs}

    def set_twiss(self, names: List[str], mat: List[List[float]]):
        """[summary]
        :param names: Names of the diffrent twiss parameters
        :type names: List[str]
        :param mat: 2D Matrix each row contains a diffrent twiss parameter. Order [beta_x, beta_y, D_x, D_y]
        :type mat: List[List[float]]
        """
        self.write("/SIMULATION/PETRA/DB", TABLE_NAMES.TWISS, 'SQL', input=[[('name', param), ('beta_x', row[0]),
                                                                             ('beta_y', row[1]), ('D_x', row[2]), ('D_y', row[3])] for param, row in zip(names, mat)], where_key='name')

    def get_twiss(self, names: List[str]) -> List[List[float]]:
        """[summary]

        :param names: Names of the requested twiss paramters
        :type names: List[str]
        :return: 2D Matrix each row contains a diffrent twiss parameter. Order [beta_x, beta_y, D_x, D_y]
        :rtype: List[List[float]]
        """
        col_names = ['name', 'beta_x', 'beta_y', 'D_x', 'D_y']
        query_mat = self.read("/SIMULATION/PETRA/DB", TABLE_NAMES.TWISS, "SQL", col_names=col_names)
        # sort by names
        mat = [[0.0 for _ in range(4)] for _ in range(len(names))]
        idx_hash = {name: idx for idx, name in enumerate(names)}
        for row in query_mat:  # ignore last to BPM because BPM adapter is ignoring this BPMs
            name = row[0]
            found_idx = idx_hash.get(name)
            if found_idx is not None:
                mat[found_idx] = list(row[1:])

        return mat

    def set_bpms(self, names, xy_arr: np.ndarray):
        ordered_indices = self._sort_by_hash_table(names, {name: idx for idx, name in enumerate(self.get_bpm_device_names())})

        curr_x, curr_y, _ = self.get_bpms()
        new_x = list(curr_x)
        new_y = list(curr_y)
        _logger.debug(f"length new_x: {len(new_x)}, length xy_arr: {xy_arr.shape}, length names: {len(names)}")
        _logger.debug(f"ordered_indices: {ordered_indices}")
        for idx, ordered_idx in enumerate(ordered_indices):
            new_x[ordered_idx] = xy_arr[idx, :][0]
            new_y[ordered_idx] = xy_arr[idx, :][1]

        xy = [[x_val, y_val] for x_val, y_val in zip(new_x, new_y)]
        self.write("/SIMULATION/PETRA/LBRENV", "ALL", "XY", input=xy)

    def get_ddxy(self, n_turns=10) -> Tuple[np.ndarray, List[str]]:
        return self.bpm_adapter.read(n_turns=n_turns)

    def get_dd_sum(self, n_turns=10) -> Tuple[np.ndarray, List[str]]:
        return self.bpm_adapter.read_sum(n_turns=n_turns)
