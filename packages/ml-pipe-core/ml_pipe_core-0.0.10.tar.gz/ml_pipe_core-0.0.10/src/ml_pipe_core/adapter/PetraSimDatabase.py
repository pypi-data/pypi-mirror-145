import mysql
import numpy as np

from .simulation_db_types import TABLE_NAMES, MAGNET_TABLE_TYPES
from ..config import MYSQL_USER, MYSQL_PW, MYSQL_HOST, MYSQL_PORT
from ..utils.SqlDBConnector import SqlDBConnector
from ..logger import init_logger
from random import random


_logger = init_logger(__name__)


class PetraSimDatabase():
    HCOR_NAMES = ['PCH_SWR_9', 'PKDK_SWR_27', 'PKDK_SWR_43', 'PKDK_SWR_50', 'PKDK_SWR_64', 'PKDK_SWR_79', 'PKDK_SWR_93', 'PKDK_SWR_108', 'PKDK_SWR_122', 'PKDK_WL_151', 'PKDK_WL_136', 'PKDK_WL_122', 'PKDK_WL_108', 'PKDK_WL_93', 'PKDK_WL_79', 'PKDK_WL_64', 'PKDK_WL_49', 'PKHW_WL_31', 'PKHW_WL_19', 'PKHW_WL_7', 'PKHW_WR_5', 'PKHW_WR_18', 'PKHW_WR_30', 'PCH_WR_40', 'PKDK_WR_49', 'PKDK_WR_64', 'PKDK_WR_72', 'PKDK_WR_86', 'PKDK_WR_100', 'PKDK_WR_115', 'PKDK_WR_129', 'PKDK_WR_144', 'PKDK_NWL_129', 'PKDK_NWL_115', 'PKDK_NWL_100', 'PKDK_NWL_86', 'PKDK_NWL_72', 'PKDK_NWL_57', 'PKDK_NWL_43', 'PKDK_NWL_27', 'PCH_NWL_9', 'PCH_NWR_9', 'PKDK_NWR_27', 'PKDK_NWR_43', 'PKDK_NWR_50', 'PKDK_NWR_64', 'PKDK_NWR_79', 'PKDK_NWR_93', 'PKDK_NWR_108', 'PKDK_NWR_122', 'PKDK_NL_151', 'PKDK_NL_136', 'PKDK_NL_122', 'PKDK_NL_108', 'PKDK_NL_93', 'PKDK_NL_79', 'PKDK_NL_64', 'PKDK_NL_49', 'PKHW_NL_31', 'PKHW_NL_19', 'PKHW_NL_7', 'PKHW_NR_5', 'PKHW_NR_18', 'PKHW_NR_30', 'PCH_NR_40', 'PKDK_NR_49', 'PKH_NR_61', 'PKH_NR_64', 'PKPDA_NR_66', 'PKPDA_NR_77', 'PKH_NR_79', 'PKH_NR_81', 'PKH_NR_84', 'PKH_NR_86', 'PKPDD_NR_87', 'PKPDA_NR_99', 'PKH_NR_101', 'PKH_NR_103', 'PKDK_NR_108', 'PKDK_NR_115', 'PKDK_NR_129', 'PKDK_NR_144', 'PKDK_NOL_129', 'PKDK_NOL_115', 'PKDK_NOL_100', 'PKDK_NOL_86', 'PKDK_NOL_72', 'PKDK_NOL_57', 'PKDK_NOL_43', 'PKDK_NOL_27', 'PCH_NOL_7', 'PCH_NOR_9', 'PCH_NOR_24', 'PCH_NOR_32', 'PKPDA_NOR_37', 'PKH_NOR_40', 'PKPDA_NOR_45', 'PKH_NOR_47', 'PKH_NOR_58', 'PKPDA_NOR_60', 'PKH_NOR_63', 'PKPDA_NOR_68', 'PKH_NOR_70', 'PKH_NOR_81',
                  'PKPDA_NOR_83', 'PKH_NOR_86', 'PKPDA_NOR_91', 'PKH_NOR_93', 'PKH_NOR_104', 'PKPDA_NOR_106', 'PKH_NOR_109', 'PKPDA_NOR_114', 'PKH_NOR_116', 'PKH_NOR_127', 'PKPDA_NOR_129', 'PKH_NOR_132', 'PKPDA_OL_151', 'PKH_OL_149', 'PKH_OL_138', 'PKPDA_OL_136', 'PKH_OL_133', 'PKPDA_OL_128', 'PKH_OL_126', 'PKH_OL_115', 'PKPDA_OL_113', 'PKH_OL_110', 'PKPDA_OL_105', 'PKH_OL_103', 'PKH_OL_92', 'PKPDA_OL_90', 'PKH_OL_87', 'PKPDA_OL_82', 'PKH_OL_80', 'PKH_OL_69', 'PKPDA_OL_67', 'PKH_OL_64', 'PKPDA_OL_59', 'PCH_OL_55', 'PCH_OL_41', 'PCH_OL_32', 'PCH_OL_19', 'PCH_OL_7', 'PCH_OR_15', 'PCH_OR_25', 'PCH_OR_29', 'PCH_OR_44', 'PKDK_OR_49', 'PKH_OR_61', 'PKH_OR_64', 'PKPDA_OR_66', 'PKPDA_OR_77', 'PKH_OR_79', 'PKH_OR_81', 'PKH_OR_84', 'PKH_OR_86', 'PKPDD_OR_87', 'PKPDA_OR_99', 'PKH_OR_101', 'PKH_OR_103', 'PKDK_OR_108', 'PKDK_OR_115', 'PKDK_OR_129', 'PKDK_OR_144', 'PKDK_SOL_129', 'PKDK_SOL_115', 'PKDK_SOL_100', 'PKDK_SOL_86', 'PKDK_SOL_72', 'PKDK_SOL_57', 'PKDK_SOL_43', 'PKDK_SOL_27', 'PCH_SOL_7', 'PCH_SOR_7', 'PKDK_SOR_27', 'PKDK_SOR_43', 'PKDK_SOR_50', 'PKDK_SOR_64', 'PKDK_SOR_79', 'PKDK_SOR_93', 'PKDK_SOR_108', 'PKDK_SOR_122', 'PKDK_SL_151', 'PKDK_SL_136', 'PKDK_SL_122', 'PKDK_SL_108', 'PKDK_SL_93', 'PKDK_SL_79', 'PKDK_SL_64', 'PKDK_SL_49', 'PCH_SL_30', 'PCH_SL_5', 'PCH_SR_5', 'PCH_SR_30', 'PKDK_SR_49', 'PKDK_SR_64', 'PKDK_SR_72', 'PKDK_SR_86', 'PKDK_SR_100', 'PKDK_SR_115', 'PKDK_SR_129', 'PKDK_SR_144', 'PKDK_SWL_129', 'PKDK_SWL_115', 'PKDK_SWL_100', 'PKDK_SWL_86', 'PKDK_SWL_72', 'PKDK_SWL_57', 'PKDK_SWL_43', 'PKDK_SWL_27', 'PCH_SWL_9']

    VCOR_NAMES = ['PCV_SWR_13', 'PCVM_SWR_31', 'PKVSU_SWR_46', 'PKVSU_SWR_60', 'PKVSX_SWR_75', 'PKVSX_SWR_89', 'PKVSX_SWR_104', 'PKVSX_SWR_118', 'PKVSX_SWR_132', 'PKVSX_WL_140', 'PKVSX_WL_125', 'PKVSX_WL_111', 'PKVSX_WL_96', 'PKVSX_WL_82', 'PKVSU_WL_68', 'PCVM_WL_52', 'PCV_WL_40', 'PKVW_WL_25', 'PKVW_WL_13', 'PKVW_WL_1', 'PKVW_WR_12', 'PKVW_WR_24', 'PCV_WR_38', 'PKVW_WR_54', 'PKVSU_WR_68', 'PKVSX_WR_82', 'PKVSX_WR_96', 'PKVSX_WR_111', 'PKVSX_WR_125', 'PKVSX_WR_140', 'PKVSX_NWL_132', 'PKVSX_NWL_118', 'PKVSX_NWL_104', 'PKVSX_NWL_89', 'PKVSX_NWL_75', 'PKVSU_NWL_60', 'PKVSU_NWL_46', 'PCVM_NWL_31', 'PCV_NWL_13', 'PCV_NWL_1', 'PCV_NWR_13', 'PCVM_NWR_31', 'PKVSU_NWR_46', 'PKVSU_NWR_60', 'PKVSX_NWR_75', 'PKVSX_NWR_89', 'PKVSX_NWR_104', 'PKVSX_NWR_118', 'PKVSX_NWR_132', 'PKVSX_NL_140', 'PKVSX_NL_125', 'PKVSX_NL_111', 'PKVSX_NL_96', 'PKVSX_NL_82', 'PKVSU_NL_68', 'PCVM_NL_52', 'PCVM_NL_41', 'PKVW_NL_25', 'PKVW_NL_13', 'PKVW_NL_1', 'PKVW_NR_12', 'PKVW_NR_24', 'PCV_NR_38', 'PKVW_NR_54', 'PKV_NR_68', 'PKV_NR_76', 'PKV_NR_80', 'PKV_NR_85', 'PKV_NR_89', 'PKV_NR_97', 'PKVSU_NR_111', 'PKVSU_NR_125', 'PKVSU_NR_140', 'PKVSX_NOL_132', 'PKVSX_NOL_118', 'PKVSX_NOL_104', 'PKVSX_NOL_89', 'PKVSX_NOL_75', 'PKVSU_NOL_60', 'PKVSU_NOL_46', 'PCVM_NOL_31', 'PCV_NOL_11', 'PCV_NOR_6', 'PCV_NOR_26', 'PCV_NOR_36', 'PKV_NOR_43', 'PKV_NOR_46', 'PKV_NOR_49', 'PKV_NOR_57', 'PKV_NOR_59', 'PKV_NOR_66', 'PKV_NOR_69', 'PKV_NOR_72', 'PKV_NOR_80', 'PKV_NOR_82',
                  'PKV_NOR_89', 'PKV_NOR_92', 'PKV_NOR_95', 'PKV_NOR_103', 'PKV_NOR_105', 'PKV_NOR_112', 'PKV_NOR_115', 'PKV_NOR_118', 'PKV_NOR_126', 'PKV_NOR_128', 'PKV_OL_153', 'PKV_OL_150', 'PKV_OL_147', 'PKV_OL_139', 'PKV_OL_136', 'PKV_OL_130', 'PKV_OL_127', 'PKV_OL_124', 'PKV_OL_116', 'PKV_OL_113', 'PKV_OL_107', 'PKV_OL_104', 'PKV_OL_101', 'PKV_OL_93', 'PKV_OL_90', 'PKV_OL_84', 'PKV_OL_81', 'PKV_OL_78', 'PKV_OL_70', 'PKV_OL_67', 'PKV_OL_61', 'PKV_OL_58', 'PCV_OL_48', 'PCV_OL_37', 'PCV_OL_24', 'PCV_OL_13', 'PCV_OL_1', 'PCV_OR_8', 'PCV_OR_25', 'PCV_OR_30', 'PCV_OR_40', 'PKV_OR_54', 'PKV_OR_68', 'PKV_OR_76', 'PKV_OR_80', 'PKV_OR_85', 'PKV_OR_89', 'PKV_OR_97', 'PKVSU_OR_111', 'PKVSU_OR_125', 'PKVSU_OR_140', 'PKVSX_SOL_132', 'PKVSX_SOL_118', 'PKVSX_SOL_104', 'PKVSX_SOL_89', 'PKVSX_SOL_75', 'PKVSU_SOL_60', 'PKVSU_SOL_46', 'PCVM_SOL_31', 'PCVM_SOL_13', 'PCVM_SOL_1', 'PCVM_SOR_13', 'PCVM_SOR_31', 'PKVSU_SOR_46', 'PKVSU_SOR_60', 'PKVSX_SOR_75', 'PKVSX_SOR_89', 'PKVSX_SOR_104', 'PKVSX_SOR_118', 'PKVSX_SOR_132', 'PKVSX_SL_140', 'PKVSX_SL_125', 'PKVSX_SL_111', 'PKVSX_SL_96', 'PKVSX_SL_82', 'PKVSU_SL_68', 'PCVM_SL_52', 'PCV_SL_36', 'PCV_SL_25', 'PCV_SR_1', 'PCV_SR_25', 'PCV_SR_36', 'PCVM_SR_52', 'PKVSU_SR_68', 'PKVSX_SR_82', 'PKVSX_SR_96', 'PKVSX_SR_111', 'PKVSX_SR_125', 'PKVSX_SR_140', 'PKVSX_SWL_132', 'PKVSX_SWL_118', 'PKVSX_SWL_104', 'PKVSX_SWL_89', 'PKVSX_SWL_75', 'PKVSU_SWL_60', 'PKVSU_SWL_46', 'PCVM_SWL_31', 'PCV_SWL_13', 'PCV_SWL_1']

    BPM_NAMES = ['BPM_SWR_13', 'BPM_SWR_31', 'BPM_SWR_46', 'BPM_SWR_61', 'BPM_SWR_75', 'BPM_SWR_90', 'BPM_SWR_104', 'BPM_SWR_118', 'BPM_SWR_133', 'BPM_WL_140', 'BPM_WL_126', 'BPM_WL_111', 'BPM_WL_97', 'BPM_WL_82', 'BPM_WL_68', 'BPM_WL_53', 'BPM_WL_36', 'BPM_WL_30', 'BPM_WL_24', 'BPM_WL_18', 'BPM_WL_12', 'BPM_WL_6', 'BPM_WR_0', 'BPM_WR_7', 'BPM_WR_13', 'BPM_WR_19', 'BPM_WR_25', 'BPM_WR_31', 'BPM_WR_37', 'BPM_WR_56', 'BPM_WR_68', 'BPM_WR_82', 'BPM_WR_97', 'BPM_WR_111', 'BPM_WR_126', 'BPM_WR_140', 'BPM_NWL_133', 'BPM_NWL_118', 'BPM_NWL_104', 'BPM_NWL_90', 'BPM_NWL_75', 'BPM_NWL_61', 'BPM_NWL_46', 'BPM_NWL_31', 'BPM_NWL_13', 'BPM_NWL_1', 'BPM_NWR_13', 'BPM_NWR_31', 'BPM_NWR_46', 'BPM_NWR_61', 'BPM_NWR_75', 'BPM_NWR_90', 'BPM_NWR_104', 'BPM_NWR_118', 'BPM_NWR_133', 'BPM_NL_140', 'BPM_NL_126', 'BPM_NL_111', 'BPM_NL_97', 'BPM_NL_82', 'BPM_NL_68', 'BPM_NL_53', 'BPM_NL_36', 'BPM_NL_30', 'BPM_NL_24', 'BPM_NL_18', 'BPM_NL_12', 'BPM_NL_6', 'BPM_NR_0', 'BPM_NR_7', 'BPM_NR_13', 'BPM_NR_19', 'BPM_NR_25', 'BPM_NR_31', 'BPM_NR_37', 'BPM_NR_56', 'BPM_NR_62', 'BPM_NR_65', 'BPM_NR_69', 'BPM_NR_74', 'BPM_NR_79', 'BPM_NR_83', 'BPM_NR_87', 'BPM_NR_90', 'BPM_NR_96', 'BPM_NR_100', 'BPM_NR_104', 'BPM_NR_111', 'BPM_NR_126', 'BPM_NR_140', 'BPM_NOL_133', 'BPM_NOL_118', 'BPM_NOL_104', 'BPM_NOL_90', 'BPM_NOL_75', 'BPM_NOL_61', 'BPM_NOL_46', 'BPM_NOL_31', 'BPM_NOL_10', 'BPM_NOR_6', 'BPM_NOR_11', 'BPM_NOR_23', 'BPM_NOR_32', 'BPM_NOR_39', 'BPM_NOR_40', 'BPM_NOR_44', 'BPM_NOR_47', 'BPM_NOR_50', 'BPM_NOR_52', 'BPM_NOR_55', 'BPM_NOR_58', 'BPM_NOR_62', 'BPM_NOR_63', 'BPM_NOR_67', 'BPM_NOR_70', 'BPM_NOR_73', 'BPM_NOR_78', 'BPM_NOR_81', 'BPM_NOR_85', 'BPM_NOR_86', 'BPM_NOR_90', 'BPM_NOR_93', 'BPM_NOR_96',
                 'BPM_NOR_98', 'BPM_NOR_101', 'BPM_NOR_104', 'BPM_NOR_108', 'BPM_NOR_109', 'BPM_NOR_113', 'BPM_NOR_116', 'BPM_NOR_119', 'BPM_NOR_124', 'BPM_NOR_127', 'BPM_NOR_131', 'BPM_NOR_132', 'BPM_OL_152', 'BPM_OL_149', 'BPM_OL_146', 'BPM_OL_144', 'BPM_OL_141', 'BPM_OL_138', 'BPM_OL_134', 'BPM_OL_133', 'BPM_OL_129', 'BPM_OL_126', 'BPM_OL_123', 'BPM_OL_118', 'BPM_OL_115', 'BPM_OL_111', 'BPM_OL_110', 'BPM_OL_106', 'BPM_OL_103', 'BPM_OL_100', 'BPM_OL_98', 'BPM_OL_95', 'BPM_OL_92', 'BPM_OL_88', 'BPM_OL_87', 'BPM_OL_83', 'BPM_OL_80', 'BPM_OL_77', 'BPM_OL_75', 'BPM_OL_72', 'BPM_OL_69', 'BPM_OL_65', 'BPM_OL_64', 'BPM_OL_60', 'BPM_OL_58', 'BPM_OL_48', 'BPM_OL_37', 'BPM_OL_24', 'BPM_OL_13', 'BPM_OL_0', 'BPM_OR_8', 'BPM_OR_17', 'BPM_OR_22', 'BPM_OR_26', 'BPM_OR_32', 'BPM_OR_37', 'BPM_OR_44', 'BPM_OR_53', 'BPM_OR_62', 'BPM_OR_65', 'BPM_OR_69', 'BPM_OR_74', 'BPM_OR_79', 'BPM_OR_83', 'BPM_OR_87', 'BPM_OR_90', 'BPM_OR_96', 'BPM_OR_100', 'BPM_OR_104', 'BPM_OR_111', 'BPM_OR_126', 'BPM_OR_140', 'BPM_SOL_133', 'BPM_SOL_118', 'BPM_SOL_104', 'BPM_SOL_90', 'BPM_SOL_75', 'BPM_SOL_61', 'BPM_SOL_54', 'BPM_SOL_46', 'BPM_SOL_31', 'BPM_SOL_13', 'BPM_SOL_1', 'BPM_SOR_13', 'BPM_SOR_31', 'BPM_SOR_46', 'BPM_SOR_61', 'BPM_SOR_75', 'BPM_SOR_90', 'BPM_SOR_104', 'BPM_SOR_118', 'BPM_SOR_133', 'BPM_SL_140', 'BPM_SL_126', 'BPM_SL_111', 'BPM_SL_97', 'BPM_SL_82', 'BPM_SL_68', 'BPM_SL_53', 'BPM_SL_36', 'BPM_SL_24', 'BPM_SL_6', 'BPM_SR_6', 'BPM_SR_24', 'BPM_SR_36', 'BPM_SR_53', 'BPM_SR_68', 'BPM_SR_82', 'BPM_SR_97', 'BPM_SR_111', 'BPM_SR_126', 'BPM_SR_140', 'BPM_SWL_133', 'BPM_SWL_118', 'BPM_SWL_104', 'BPM_SWL_90', 'BPM_SWL_75', 'BPM_SWL_61', 'BPM_SWL_46', 'BPM_SWL_39', 'BPM_SWL_31', 'BPM_SWL_13', 'BPM_SWL_1', 'BPM_SOR_67', 'BPM_SOL_24']

    def __init__(self, sql_connector=None) -> None:
        self.db_connector = SqlDBConnector(user=MYSQL_USER, pw=MYSQL_PW, host=MYSQL_HOST, port=MYSQL_PORT, database="sim_db") if sql_connector is None else sql_connector

    def wait_until_table_created(table):
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except mysql.connector.errors.ProgrammingError as mysql_error:
                    if mysql_error.errno == mysql.connector.errorcode.ER_NO_SUCH_TABLE:
                        args[0].cnx.db_connector.wait_until_table_is_created(table)
                        return func(*args, **kwargs)
            return wrapper
        return decorator

    def create_petra_tables(self):
        self.create_magnets_table()
        self.insert_magnets_table(self.HCOR_NAMES, [MAGNET_TABLE_TYPES.HCOR for _ in range(len(self.HCOR_NAMES))], [0.0 for _ in range(len(self.HCOR_NAMES))])
        self.insert_magnets_table(self.VCOR_NAMES, [MAGNET_TABLE_TYPES.VCOR for _ in range(len(self.VCOR_NAMES))], [0.0 for _ in range(len(self.VCOR_NAMES))])

        self.create_twiss_table()
        self.insert_twiss(self.BPM_NAMES, [[0.0 for _ in range(4)] for _ in range(len(self.BPM_NAMES))])

        self.create_machine_params_table()
        param_names = ['Q_x', 'Q_y', 'I_total']
        values = [0.0, 0.0, 100.0]
        self.insert_default_machine_params(param_names, values)

        self.create_bpm_table()
        self.insert_bpms(self.BPM_NAMES)

        self.create_multi_turn_bpm_table()
        self.insert_multi_turn_bpms(self.BPM_NAMES)

    def create_magnets_table(self):
        cursor = self.db_connector.sql_con.cursor()
        cursor.execute(f"CREATE TABLE " + TABLE_NAMES.MAGNETS + " (name varchar(255) PRIMARY KEY, type varchar(255), time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, value FLOAT, pos INT)")
        self.db_connector.sql_con.commit()

    def create_twiss_table(self):
        cursor = self.db_connector.sql_con.cursor()
        cursor.execute(f"CREATE TABLE {TABLE_NAMES.TWISS} (name varchar(255) PRIMARY KEY, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, beta_x FLOAT, beta_y FLOAT, D_x FLOAT, D_y FLOAT)")
        self.db_connector.sql_con.commit()
        cursor.close()

    def create_machine_params_table(self):
        cursor = self.db_connector.sql_con.cursor()
        cursor.execute(f"CREATE TABLE {TABLE_NAMES.MACHINE_PARMS} (param varchar(255) PRIMARY KEY, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, value FLOAT)")
        self.db_connector.sql_con.commit()
        cursor.close()

    def create_bpm_table(self):
        cursor = self.db_connector.sql_con.cursor()
        cursor.execute(f"CREATE TABLE {TABLE_NAMES.BPM} (name varchar(255) PRIMARY KEY, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, x FLOAT, y FLOAT, length Float, pos INT)")
        self.db_connector.sql_con.commit()
        cursor.close()

    def create_multi_turn_bpm_table(self):
        cursor = self.db_connector.sql_con.cursor()
        cursor.execute(f"CREATE TABLE {TABLE_NAMES.MULTI_TURN_BPM} (name varchar(255) PRIMARY KEY, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, x BLOB, y BLOB, length Float, pos INT)")
        self.db_connector.sql_con.commit()
        cursor.close()

    def insert_multi_turn_bpms(self, names):
        cursor = self.db_connector.sql_con.cursor()
        x_default = np.array([0, 0, 0])
        y_default = np.array([0, 0, 0])
        query = '''INSERT INTO bpm_multiturn (name, x, y, length, pos) VALUES (%s, %s, %s, %s, %s)'''
        for idx, name in enumerate(names):
            cursor.execute(query, (name, x_default.tobytes(), y_default.tobytes(), '-1.0', idx))
        self.db_connector.sql_con.commit()
        cursor.close()

    def insert_bpms(self, names):
        cursor = self.db_connector.sql_con.cursor()
        for idx, name in enumerate(names):
            cursor.execute(f"INSERT INTO {TABLE_NAMES.BPM} (name, x, y, length, pos) VALUES ('{name}','0.0', '0.0', '-1.0', '{idx}')")
        cursor = self.db_connector.sql_con.cursor()
        self.db_connector.sql_con.commit()
        cursor.close()

    def insert_magnets_table(self, names, types, values):
        cursor = self.db_connector.sql_con.cursor()
        for idx, t in enumerate(zip(names, types, values)):
            name, type, value = t
            cursor.execute(f"INSERT INTO {TABLE_NAMES.MAGNETS} (name, type, value, pos) VALUES ('{name}','{type}', '{value}', '{idx}')")
        self.db_connector.sql_con.commit()
        cursor.close()

    def insert_twiss(self, names, value_mat):
        cursor = self.db_connector.sql_con.cursor()
        for name, row in zip(names, value_mat):
            beta_x, beta_y, D_x, D_y = row
            cursor.execute(f"INSERT INTO {TABLE_NAMES.TWISS} (name, beta_x, beta_y, D_x, D_y) VALUES ('{name}','{beta_x}', '{beta_y}', '{D_x}', '{D_y}')")
        self.db_connector.sql_con.commit()
        cursor.close()

    def insert_random_values_for_magnets(self, names, multiply_factor=1e-4):
        self.insert_magnets_table(names, [multiply_factor*random() for _ in range(len(names))])

    def insert_default_machine_params(self, param_names, values):
        cursor = self.db_connector.sql_con.cursor()
        for name, value in zip(param_names, values):
            cursor.execute(f"INSERT INTO {TABLE_NAMES.MACHINE_PARMS} (param, value) VALUES ('{name}','{value}')")
        self.db_connector.sql_con.commit()
        cursor.close()

    @wait_until_table_created(TABLE_NAMES.BPM)
    def set_xy_bpms(self, val):
        try:
            data = []
            for idx, val in enumerate(val):
                data.append((val[0], val[1], idx))
            cursor = self.db_connector.sql_con.cursor()
            cursor.executemany("Update " + TABLE_NAMES.BPM + " set x=%s, y=%s where pos=%s", data)
            self.db_connector.sql_con.commit()
            cursor.close()
        except mysql.connector.Error as error:
            self.db_connector.sql_con.rollback()

    @wait_until_table_created(TABLE_NAMES.MAGNETS)
    def set_magnet_values_as_group(self, group, values, size):
        try:
            data = []
            for pos, value in zip(range(size), values):
                data.append((value, pos, group))
            cursor = self.db_connector.sql_con.cursor()
            cursor.executemany("Update magnets set value = %s where pos=%s and type=%s", data)
            self.db_connector.sql_con.commit()
            cursor.close()
            return True
        except mysql.connector.Error as error:
            self.db_connector.sql_con.rollback()
        return False

    @wait_until_table_created(TABLE_NAMES.MAGNETS)
    def set_magnet_value(self, device, value):
        try:
            query = f"Update magnets set value ={value} where name='{device.upper()}'"
            cursor = self.db_connector.sql_con.cursor()
            cursor.execute(query)
            self.db_connector.sql_con.commit()
            cursor.close()
            return True
        except mysql.connector.Error as error:
            self.db_connector.sql_con.rollback()
        return False

    @wait_until_table_created(TABLE_NAMES.MACHINE_PARMS)
    def set_machine_params(self, names, values):
        try:
            data = [(value, name) for name, value in zip(names, values)]
            cursor = self.db_connector.sql_con.cursor()
            cursor.executemany("Update machine_params set value = %s where param = %s", data)
            cursor.close()
        except mysql.connector.Error as error:
            self.db_connector.sql_con.rollback()

    def _create_update_queries(self, table, where_key, rows):
        queries = []
        for row in rows:
            found_where_key_val_pair = next(
                (key_val_pair for key_val_pair in row if key_val_pair[0] == where_key), None
            )
            if found_where_key_val_pair is None:
                _logger.debug(f"update table {table} failed because key {where_key} is not in input.")
                return []
            ",".join([f"{key_val_pair[0]}={key_val_pair[1]}" for key_val_pair in row if key_val_pair[0] != where_key])
            set_clauses = []
            for key_val_pair in row:
                if key_val_pair[0] != where_key:
                    if type(key_val_pair[1]) == str:
                        set_clauses.append(f"{key_val_pair[0]}='{key_val_pair[1]}'")
                    else:
                        set_clauses.append(f"{key_val_pair[0]}={key_val_pair[1]}")

            query = f"Update {table} set {','.join(set_clauses)} where {found_where_key_val_pair[0]}='{found_where_key_val_pair[1]}'"
            queries.append(query)
        return queries

    @wait_until_table_created(TABLE_NAMES.BPM)
    def get_bpm(self, axes: str, bpm: str):
        sql_select_Query = f"select {axes}, name from {TABLE_NAMES.BPM} order by pos"
        cursor = self.db_connector.sql_con.cursor()
        cursor.execute(sql_select_Query)
        result = cursor.fetchall()
        self.db_connector.sql_con.commit()
        cursor.close()
        values = [res[0] for res in result]
        # bpm_names = [res[1] for res in result]
        # start_i = bpm_names.index(bpm)
        # values = values[start_i:] + values[:start_i]  # realign names to start from start_with
        return values

    @wait_until_table_created(TABLE_NAMES.MACHINE_PARMS)
    def get_machine_params(self):
        sql_select_Query = f"select param, value from {TABLE_NAMES.MACHINE_PARMS}"
        cursor = self.db_connector.sql_con.cursor()
        cursor.execute(sql_select_Query)
        res = {res[0]: res[1] for res in cursor.fetchall()}
        self.db_connector.sql_con.commit()
        cursor.close()
        return res

    @wait_until_table_created(TABLE_NAMES.BPM)
    def get_ref_orbit(self):
        sql_select_Query = f"select count(*) from {TABLE_NAMES.BPM}"
        cursor = self.db_connector.sql_con.cursor()
        cursor.execute(sql_select_Query)
        result = cursor.fetchall()
        self.db_connector.sql_con.commit()
        cursor.close()
        count = result[0][0]
        return [0.0 for _ in range(count)]

    @wait_until_table_created(TABLE_NAMES.MAGNETS)
    def get_magnets(self, device):
        query = f"select value from {TABLE_NAMES.MAGNETS} where name = '{device.upper()}'"
        cursor = self.db_connector.sql_con.cursor()
        cursor.execute(query)
        res = [res[0] for res in cursor.fetchall()]
        self.db_connector.sql_con.commit()
        return res

    @wait_until_table_created(TABLE_NAMES.MAGNETS)
    def get_magnets_by_group(self, group, size=None):
        query = f"select value from {TABLE_NAMES.MAGNETS} where type = '{group}' order by pos"
        if size is not None:
            query += f" Limit {size}"  # TODO: is this the right behavior of Tine?
        cursor = self.db_connector.sql_con.cursor()
        cursor.execute(query)
        res = [res[0] for res in cursor.fetchall()]
        self.db_connector.sql_con.commit()
        return res

    @wait_until_table_created(TABLE_NAMES.MAGNETS)
    def get_magnet_names(self, device, size=None):
        query = f"select name from {TABLE_NAMES.MAGNETS} where type='{device}' order by pos"
        if size is not None:
            query += f" Limit {size}"  # TODO: is this the right behavior of Tine?
        cursor = self.db_connector.sql_con.cursor()
        cursor.execute(query)
        res = [res[0] for res in cursor.fetchall()]
        self.db_connector.sql_con.commit()
        cursor.close()
        return res

    @wait_until_table_created(TABLE_NAMES.MAGNETS)
    def get_num_of_magnets(self, device, size=None):
        query = f"select COUNT(*) from {TABLE_NAMES.MAGNETS} where type='{device}' order by pos"
        if size is not None:
            query += f" Limit {size}"  # TODO: is this the right behavior of Tine?
        cursor = self.db_connector.sql_con.cursor()
        cursor.execute(query)
        res = cursor.fetchall()[0][0]
        self.db_connector.sql_con.commit()
        cursor.close()
        return res

    def get_table(self, table, where_key_value_pair=None, col_names=None):
        col_names_str = '*' if col_names is None else ','.join(col_names)
        query = f"select {col_names_str} from {table}" if where_key_value_pair is None else f"select {col_names_str} from {table} where {where_key_value_pair[0]}='{where_key_value_pair[1]}'"
        cursor = self.db_connector.sql_con.cursor()
        cursor.execute(query)
        return [res for res in cursor.fetchall()]

    def set_table(self, where_key, table, rows):
        try:
            cursor = self.db_connector.sql_con.cursor()
            queries = self._create_update_queries(table, where_key, rows)
            for query in queries:
                cursor.execute(query)
            self.db_connector.sql_con.commit()
            cursor.close()
            return True
        except mysql.connector.Error as error:
            self.db_connector.sql_con.rollback()
            return False
