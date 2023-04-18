import os

ROOT = os.path.dirname(__file__)
DEFAULT_INPUT_FILE = os.path.join(ROOT, 'results.xlsx')
DEFAULT_OUTPUT_FILE = os.path.join(ROOT, 'triage_output.xlsx')
ACCEPTED_EXTENSIONS = ('csv', 'xlsx', 'xls')
DEFAULT_EXT = 'xlsx'
DEFAULT_DEBUG_FN = 'debug.txt'
DEFAULT_LOG_DIR = os.path.join(ROOT, 'logs')
DEFAULT_DEBUG_FP = os.path.join(DEFAULT_LOG_DIR, DEFAULT_DEBUG_FN)
