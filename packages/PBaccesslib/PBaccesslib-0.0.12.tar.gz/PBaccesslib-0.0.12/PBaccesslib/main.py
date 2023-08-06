import numpy as np
from PBaccesslib.wafer_test import main as wafer_main
from PBaccesslib.characteritzation import main as charac_main
from PBaccesslib.doc_operations import ManageCsv
from PBaccesslib import bridge, heartbeat, logger, KEITHLEY_ADRESS, DATA_FOLDER_PATH, LOG_FILE_PATH, CHIP_REG_PATH, \
    PIXEL_REG_PATH


def kill_hearbeat():
    """"""
    heartbeat.kill()


def close_connection():
    """"""
    bridge.close_communication()


def test(row: int, column: int, wafer_pos: int):
    """"""
    """ Load chip_reg and pixel_reg initial config"""
    try:
        chip_reg = np.load(CHIP_REG_PATH)
        pixel_reg = np.load(PIXEL_REG_PATH)
    except FileNotFoundError:
        logger.error("Check init_config.txt. CHIP_REG_PATH or PIXEL_REG_PATH are not okay.")
        return True

    """Main folder creation"""
    gen_doc = ManageCsv()
    new_folder_path = gen_doc.create_folder(DATA_FOLDER_PATH, f"wafer_{wafer_pos}")
    new_folder_path = gen_doc.create_folder(new_folder_path, f"chip_{row}_{column}")
    td_bin_array, error_programing = wafer_main.test(chip_reg, pixel_reg, KEITHLEY_ADRESS, new_folder_path)
    # if sum(td_bin_array) != len(td_bin_array):
    #     logger.error(td_bin_array)
    #     return True
    # if error_programing:
    #     return True
    error_dac = charac_main.dac_test(chip_reg, pixel_reg, new_folder_path)
    if error_dac:
        return True
    error_disc = charac_main.disc_test(chip_reg, pixel_reg, new_folder_path)
    if error_disc:
        return True
    error_ifeed = charac_main.ifeed_test(chip_reg, pixel_reg, new_folder_path)
    if error_ifeed:
        return True
    return False
