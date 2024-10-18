import pandas as pd
import numpy as np
from argparse import ArgumentParser
from bib import Bib
from triage import columns_to_eval_funcs
from tkinter import messagebox
import os, sys, warnings, expand_columns
from config import *

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

READ_ENGINES = {
  'csv': pd.read_csv,
  'xlsx': pd.read_excel,
  'xls': pd.read_excel
}

def safe_sys_exit():
  '''
  Used in the rare case the output excel file is open
  i.e. the user is attempting to override a file they have already run the program on and it is open
  '''
  sys.exit()

def fill_ext(filename):
  '''
  Set default file extension to xlsx
  '''
  try:
    extract_ext(filename)
    return filename
  except ValueError:
    return f'{filename}.{DEFAULT_EXT}'
  
def create_df(filename):
  ext = extract_ext(filename)
  print('Reading the file ...')
  read_engine = READ_ENGINES[ext]
  df = read_engine(filename)
  print('Finish reading\n')
  return df


def save_df(df, filename):
  ext = extract_ext(filename)
  print('Writing output ...')
  if ext == 'csv':
    df.to_csv(filename, index=False)
  if ext in ('xlsx', 'xls'):
    try:
      df.to_excel(filename, index=False)
    except Exception:
      messagebox.showwarning(title="File Warning", message="The output file is open, please close it and try again")
      safe_sys_exit()

  print('Finish writing')

def extract_ext(filename):
  if '.' in filename:
    ext = filename.split('.')[-1]
    if ext in ACCEPTED_EXTENSIONS:
      return ext
    raise ValueError(f'File extension must be {ACCEPTED_EXTENSIONS}')
  raise ValueError(f'Cannot find file extension')
  
parser = ArgumentParser()
parser.add_argument('-if', '--input_file', default=DEFAULT_INPUT_FILE, type=str, help='Path to the input file')
parser.add_argument('-of', '--output_file', default=DEFAULT_OUTPUT_FILE, type=str, help='Path to the output file')

args = vars(parser.parse_args())

if __name__ == '__main__':

  input_path = os.path.join(ROOT, args['input_file'])
  input_df = create_df(input_path)
  input_df.columns = [col.lower().rstrip() for col in input_df.columns]
  mmsid_col = 'mms id'
  
  if 'mms id' not in input_df.columns:
    print('Cannot find column mms id in the table.')
    exit(1)
  
  n = len(input_df)
  print(f'Found {n} records ...')
  
  # convert from int to str for writing
  input_df[mmsid_col] = input_df[mmsid_col].apply(lambda mmsID: str(mmsID))

  output_path = fill_ext(os.path.join(ROOT, args['output_file']))
  output_df = pd.DataFrame()
  
  print('Evaluating ...\n')
  for start_id in range(0, n, BATCH_SIZE):
    end_id = min(start_id + BATCH_SIZE, n)
    df_size = min(BATCH_SIZE, end_id - start_id)
    print(f'Processing mmsID from {start_id} to {end_id} ...')
    batch_df = pd.DataFrame({
      'MMS ID': input_df[mmsid_col][start_id:end_id],
      'OCLC#' : np.full((df_size,), np.nan),
      'Floor_Status': np.full((df_size,), np.nan),
      'Size_Status': np.full((df_size,), np.nan),
      'Format_Assessment': np.full((df_size,), np.nan),
      'Call_Number_Assessment' : np.full((df_size,), np.nan),
      'Title': input_df['title'][start_id:end_id],
      'Brief_Level': 2 * np.ones((df_size,)),
      'Overall_Condition': np.full((df_size,), np.nan),
      'Illustration_Status': np.full((df_size,), np.nan),
      'Bibliography_Status': np.full((df_size,), np.nan),
      'Index_Status': np.full((df_size,), np.nan),
      'Pub_Locn': np.full((df_size,), np.nan),
      'Coding_Problems': np.full((df_size,), np.nan)
    })
    bib_series = input_df[mmsid_col][start_id:end_id].apply(lambda mmsID: Bib(mmsID))
    for col, func in columns_to_eval_funcs.items():
      vectorized_func = np.vectorize(func)
      batch_df[col] = vectorized_func(bib_series)
    output_df = pd.concat([output_df, batch_df])
    save_df(output_df, output_path)
  print("Finalizing ...")
  expand_columns.expand_columns(output_path)
  