import os
from bib import Bib
from triage import columns_to_eval_funcs
from argparse import ArgumentParser, ArgumentTypeError
import logging

ROOT = os.path.dirname(__file__)
debug_fn = 'debug.txt'
debug_fp = os.path.join(ROOT, debug_fn)

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
      
class Debugger:
  def __init__(self, logger) -> None:
    self.logger = logger
    
  def debug(self, mmsID):
    logger = self.logger
    try:
      bib = Bib(mmsID)
      header = f'--- Triage info of {mmsID} ---'
      logger.info(header)
      
      leader = bib.leader
      encoding_value = leader[17]
      logger.info(f'Leader: {leader}')
      logger.info(f'Encoding value: {encoding_value}')
      
      value_of_042a = bib.get_data_field('042', 'a').get_text()
      if value_of_042a:
        logger.info(f'042a: {value_of_042a}')
      else:
        logger.warning('No value for 042a field')
        
      value_of_300c = bib.get_data_field('300', 'c').get_text()
      if value_of_300c:
        logger.info(f'Size: {value_of_300c}')
      else:
        logger.critical('Missing value for 300c')
      
      for col, func in columns_to_eval_funcs.items():
        logger.info(f'{col}: {func(bib)}')
      print()
    except:
      if mmsID.lower() == 'q':
        exit()
      print(f'Cannot find record of MMS ID {mmsID}. Please make sure that the MMS ID is valid.')
    
parser = ArgumentParser()
parser.add_argument('-ids', '---mmsids', nargs='+', default=['991004787783604651'], type=str, help='An MMS ID or a list of MMS ID to debug')
parser.add_argument('-i', '--interactive', action='store_true', default=False, help='Run the debugger in interactive mode')
parser.add_argument('-f', '--filename', default=debug_fp, type=str, help='Name of the file to write the debug log')
args = vars(parser.parse_args())
    
if __name__ == '__main__':
  interactive = args['interactive']
  
  # setup configuration for logging
  logging.basicConfig(
    filename=args['filename'],
    format='%(asctime)s %(message)s',
    filemode='w'
  )
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)
  
  ch = logging.StreamHandler()
  ch.setLevel(logging.DEBUG)
  ch.setFormatter(CustomFormatter())
  
  logger.addHandler(ch)
  
  debugger = Debugger(logger)
  
  if interactive:
      # TODO: prompt input from user and run that prompt
      # even better: using python GUI toolkit
      waiting_input = True
      while waiting_input:
        mmsID = input('Enter a valid MMS ID (Press q to exit): ')
        debugger.debug(mmsID)
  else:
    for mmsID in args['mmsids']:
      debugger.debug(mmsID)