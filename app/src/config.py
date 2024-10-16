import os
import platform

ROOT = os.path.dirname(__file__)
MAINROOT = os.path.dirname(ROOT)
BATCH_SIZE = 10
APP_ROOT = os.path.join(ROOT)
PLATFORM = ""

input_filename = 'biblio_data.xlsx'
output_filename = 'results_triaged.xlsx'

# Accounting fot the differences in file structure between Mac and Windows
plat = platform.platform() 

if "macOS" in plat:
    PLATFORM = 'macOS'
    DEFAULT_INPUT_FILE = os.path.join(MAINROOT, 'inputs/'+ input_filename)
    DEFAULT_OUTPUT_FILE = os.path.join(MAINROOT, 'outputs/'+ output_filename)
elif 'Windows' in plat:
    PLATFORM = 'windows'
    DEFAULT_INPUT_FILE = os.path.join(MAINROOT, 'inputs\\'+ input_filename)
    DEFAULT_OUTPUT_FILE = os.path.join(MAINROOT, 'outputs\\'+ output_filename)
else:
    DEFAULT_INPUT_FILE = os.path.join(MAINROOT, 'inputs\\'+ input_filename)
    DEFAULT_OUTPUT_FILE = os.path.join(MAINROOT, 'outputs\\'+ output_filename)
    
ACCEPTED_EXTENSIONS = ('csv', 'xlsx', 'xls')
DEFAULT_EXT = 'xlsx'
DEFAULT_DEBUG_FN = 'debug'
DEFAULT_LOG_DIR = os.path.join(MAINROOT, 'logs')
DEFAULT_DEBUG_FP = os.path.join(DEFAULT_LOG_DIR, DEFAULT_DEBUG_FN)
