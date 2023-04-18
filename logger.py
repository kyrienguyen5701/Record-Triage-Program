import os
import logging
from config import DEFAULT_LOG_DIR

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
    
class TriageLogger(logging.Logger):
  def __init__(self, name='debug_logger', level=logging.DEBUG):
    super().__init__(name=name)
    self.setLevel(level=level)
    self.build()
    
  def create_stream_hdl(self):
    hdl = logging.StreamHandler()
    hdl.setLevel(self.level)
    hdl.setFormatter(CustomFormatter())
    return hdl
    
  def create_file_hdl(self):
    fn = os.path.join(DEFAULT_LOG_DIR, f'{self.name}.txt')
    hdl = logging.FileHandler(filename=fn, mode='w')
    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    hdl.setFormatter(fmt)
    return hdl
    
  def build(self):
    self.hdls = {
      'stream': self.create_stream_hdl(),
      'file': self.create_file_hdl()
    }
    for hdl in self.hdls.values():
      self.addHandler(hdl)
