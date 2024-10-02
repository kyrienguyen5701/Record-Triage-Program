import os

ROOT = os.path.dirname(__file__)
MAINROOT = os.path.dirname(ROOT)
BATCH_SIZE = 10
APP_ROOT = os.path.join(ROOT)
DEFAULT_INPUT_FILE = os.path.join(MAINROOT, 'inputs\\results.xlsx')
DEFAULT_OUTPUT_FILE = os.path.join(MAINROOT, 'outputs\\results_triaged.xlsx')
ACCEPTED_EXTENSIONS = ('csv', 'xlsx', 'xls')
DEFAULT_EXT = 'xlsx'
DEFAULT_DEBUG_FN = 'debug'
DEFAULT_LOG_DIR = os.path.join(MAINROOT, 'logs')
DEFAULT_DEBUG_FP = os.path.join(DEFAULT_LOG_DIR, DEFAULT_DEBUG_FN)
