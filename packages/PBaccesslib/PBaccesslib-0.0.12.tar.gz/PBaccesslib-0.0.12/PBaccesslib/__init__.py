import json
import os
import platform
import logging.handlers
from Commacceslib.use_comm import UseBridge
from PBaccesslib.hearbeat_thread import KillableThread
from K2600acceslib import log_to_screen as k2600_screen, log_add_file_handler as k2600_add_file
from Commacceslib import log_to_screen as comm_screen, log_add_file_handler as comm_add_file
if platform.system() == "Linux":
    lib_name = "liblinda-lib.so"
else:
    lib_name = "linda-lib.dll"


input_data_path = os.path.abspath(os.path.dirname(__file__))
print(input_data_path)
# reading the data from the file
with open(os.path.join(input_data_path, 'data', 'init_values.txt')) as f:
    data = f.read()
js = json.loads(data)
IP = js.get("IP")
SYNC = js.get("SYNC")
ASYNC = js.get("ASYNC")
BITMAP = js.get("BITMAP")
VERBOSE = js.get("VERBOSE")
KEITHLEY_ADRESS = js.get("KEITHLEY_ADRESS")
DATA_FOLDER_PATH = js.get("DATA_FOLDER_PATH")
LOG_FILE_PATH = js.get("LOG_FILE_PATH")
# LIBPATH = os.path.join(input_data_path, 'lib', lib_name)
LIBPATH = js.get("LIBPATH")
CHIP_REG_PATH = os.path.join(input_data_path, 'data', 'chip_reg.npy')
PIXEL_REG_PATH = os.path.join(input_data_path, 'data', 'pixel_reg.npy')

# Defined here since it is imported in other pyvisa modules
BASE_NAME = 'ProbeCard'
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def log_to_screen(level=logging.DEBUG) -> None:
    log_to_stream(None, level)  # sys.stderr by default


def log_to_stream(stream_output, level=logging.DEBUG) -> None:
    logger.setLevel(level)
    ch = logging.StreamHandler(stream_output)
    ch.setLevel(level)
    ch.setFormatter(formatter)

    logger.addHandler(ch)


def log_add_file_handler(file_path, level=logging.DEBUG):
    fh = logging.handlers.RotatingFileHandler(filename=file_path, maxBytes=5 * 1024 * 1024, backupCount=5)
    fh.setLevel(level=level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def std_file_on(file_path):
    """ Add data to file """
    log_add_file_handler(file_path)
    k2600_add_file(file_path)
    comm_add_file(file_path)

    """ Std out log """
    log_to_screen()
    k2600_screen()
    comm_screen()


if VERBOSE:
    std_file_on(LOG_FILE_PATH)

""" Bridge initialization"""
bridge = UseBridge(IP, SYNC, ASYNC, LIBPATH)
heartbeat = KillableThread(bridge.use_update_HB, sleep_interval=2.5)
heartbeat.start()

__version__ = "unknown"

__all__ = [
    "logger",
    "log_to_screen",
    "log_to_stream",
    "log_add_file_handler",
    "BITMAP",
    "bridge",
    "heartbeat",
    "KEITHLEY_ADRESS",
    "DATA_FOLDER_PATH",
    "LOG_FILE_PATH",
    "CHIP_REG_PATH",
    "PIXEL_REG_PATH",
]
