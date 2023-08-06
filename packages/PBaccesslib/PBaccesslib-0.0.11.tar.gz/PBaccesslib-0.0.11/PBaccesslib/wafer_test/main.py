from PBaccesslib.wafer_test.connection_check import keithley_test, touchdown_test
from PBaccesslib.wafer_test.program_check import read_write_test


def test(chip_reg, pixel_reg, keithley_adress, folder_path):
    k_out_array = keithley_test(keithley_adress, folder_path)
    td_bin_array = touchdown_test()
    td_bin_array.extend(k_out_array)
    error_programing = read_write_test(chip_reg, pixel_reg)

    return td_bin_array, error_programing
