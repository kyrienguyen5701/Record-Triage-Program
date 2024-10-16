from __future__ import annotations
from bib import Bib, TAG_FOR_CALL_NUMBER, TAG_FOR_OCLC_NUMBER, TAG_FOR_ILLUSTRATIONS, TAG_FOR_NATURE, TAG_FOR_INDEX
import rule

OVERSIZE_ff_HEIGHT_MIN = 45
OVERSIZE_ff_DEPT_MIN = 39
OVERSIZE_f_HEIGHT_MIN = 34
OVERSIZE_q_HEIGHT_MIN = 27
OVERSIZE_q_DEPT_MIN = 23

def change_format_of_dimension(dim: str) -> int:
    """
    Returns modified dimensions of book

    :param dimen: Dimensions of book
    :type dimen: str
    :return: Modified dimensions of book
    :rtype: int
    """
    return int(''.join(dim.split(" ")))
  
def get_height_with_spacing(height: str) -> str:
    """
    Returns substring of height where index of height units is cut off

    :param height: Height of book
    :type height: str
    :return: Substring of height where index of height units is cut off
    :rtype: str
    """
    index_h = height.find("cm")
    index_x = height.find("x")
    if "x" in height and "cm" in height:
      return height[:index_x]
    return height[:index_h]
  
def get_depth_with_spacing(depth: str) -> str:
    """
    Returns substring of depth where index of depth units is cut off

    :param depth: Depth of book
    :type depth: str
    :return: Substring of depth where index of depth units is cut off
    :rtype: str
    """
    index_d = depth.find("cm")
    index_x = depth.find("x")
    if "x" in depth and "cm" in depth:
      return depth[index_x + 1:index_d]
    return "-1"

class Triage:
  def __init__(self):
    pass
  
  @staticmethod
  def compute_brief_level(bib: Bib) -> str:
    return bib.compute_brief_level()
  
  @staticmethod
  def eval_brief_level(bib: Bib) -> str:
    '''
    This function returns a string indicating quality of record being analyzed.
    The method translates value of initialized variable to string indicating quality of record.
    The code uses if-else statements to check the value of briefLevel and returns a string accordingly.
    If briefLevel is 10 or 9, it returns 'High quality Record, Minimal Review'.
    If briefLevel is 8 or 7, it returns 'Acceptable Record, Light Review'.
    If briefLevel is 6, it returns 'Call number issue'.
    If briefLevel is 5, it returns 'Pre-publication Record, Upgrade'.
    If briefLevel is 4, it returns 'Keyed Record, Upgrade'.
    If briefLevel is 3, it returns 'Substandard Record, Overlay'.
    Otherwise, it returns 'Out of scope: Review'.
    
    :param bib: A parameter that represents the record being analyzed.
    :return: A string indicating quality of record being analyzed.
    '''
    assessment = {
        10: 'High quality Record, Minimal Review',
        9: 'High quality Record, Minimal Review',
        8: 'Acceptable Record, Light Review',
        7: 'Acceptable Record, Light Review',
        6: 'Call number issue',
        5: 'Pre-publication Record, Upgrade',
        4: 'Keyed Record, Upgrade',
        3: 'Substandard Record, Overlay'
    }
    
    # Return assessment based on bib's brief level
    return assessment.get(bib.compute_brief_level(), 'Out of scope: Review')
  
  @staticmethod
  def eval_call_number(bib: Bib) -> str:
    '''
    Returns string for call number
    checks data field to see what type of call number should be returned
    
    :param bib: A parameter that represents the record being analyzed.
    :return: A string indicating quality of record being analyzed.
    '''
    to_add = 'Manually Review'
    call_number = bib.get_data_field(TAG_FOR_CALL_NUMBER)
    if call_number != None and call_number.data_subfield_exists_more_than_once('a'):
        return to_add + ': Double $$a'
    else:
        call_number_a = bib.get_data_field(TAG_FOR_CALL_NUMBER, 'a').get_text()
        call_number_b = bib.get_data_field(TAG_FOR_CALL_NUMBER, 'b').get_text()
        if bib.data_field_exists_more_than_once(TAG_FOR_CALL_NUMBER):
            return to_add + ': Duplicate call numbers'
        elif call_number_a == None:
            return to_add + ': No call number'
        elif call_number_b == None:
            return to_add + ': Incomplete call number'
        else:
            return f'{call_number_a} {call_number_b}' if 'LAW' not in call_number_a and 'PER' not in call_number_a else f'{to_add}: Text Call Number'  
  
  @staticmethod
  def eval_location(bib: Bib) -> str:
    '''
    Returns string indicating where in library book should be
    '''
    if not Triage.is_call_number_complete(bib):
      return ''
    call_number_a = bib.get_data_field(TAG_FOR_CALL_NUMBER, 'a').get_text()[0]
    if call_number_a not in ['A', 'B', 'C', 'D']:
      if 'Manually Review' in Triage.eval_size(bib) or 'No edits' in Triage.eval_size(bib):
        return ''
    return 'Change location to floor 2'
  
  @staticmethod
  def eval_size(bib: Bib) -> str:
    """
    Returns string indicating if book category is correct for its size
    """
    size = bib.get_data_field("300", "c").get_text()
    if size == None or size in ("cm", "cm."):
        return "Manually Review: Missing size"

    if "mm" in size or "mm." in size:
        return "Manually Review: Miniature"

    height = change_format_of_dimension(get_height_with_spacing(size))
    depth = change_format_of_dimension(get_depth_with_spacing(size))

    if height >= OVERSIZE_f_HEIGHT_MIN:
        return "Change to Oversize f"

    if height < OVERSIZE_q_HEIGHT_MIN and depth < OVERSIZE_q_DEPT_MIN:
        return "No edits: Regular size"

    if height < OVERSIZE_ff_HEIGHT_MIN and depth < OVERSIZE_ff_DEPT_MIN:
        return "Change to Oversize q"

    return "Change to Oversize ff"
  
  @staticmethod
  def eval_format(bib: Bib) -> str:
    """
    Returns string of whether 300 needs reformatting

    :param bib: Bibliographic record
    :type bib: object
    :return: String of whether 300 needs reformatting
    :rtype: str
    """
    pagination = bib.get_data_field("300", "a").get_text()
    if pagination == None or "pages" in pagination or " p." in pagination:
      return ""

    if "online" in pagination:
      return "Online record; overlay with print"

    if " v." not in pagination and "volume" not in pagination:
      return "Manually Review: Field 300 problem"

    return "Multivolume title; create items"
  
  @staticmethod
  def is_call_number_complete(bib: Bib) -> bool:
    """
    Returns True if the call number is complete else False
    """
    return bool(bib.get_data_field(TAG_FOR_CALL_NUMBER) != None and \
      bib.get_data_field(TAG_FOR_CALL_NUMBER, 'a') and \
      bib.get_data_field(TAG_FOR_CALL_NUMBER, 'b'))
  
  @staticmethod
  def eval_call_number(bib: Bib) -> str:
    """
    Returns string for call number
    checks data field to see what type of call number should be returned
    """
    to_add = 'Manually Review'
    call_number = bib.get_data_field(TAG_FOR_CALL_NUMBER)
    
    # You can use Rule and Condition here should the conditional statements become more complicated
    if call_number != None and call_number.data_subfield_exists_more_than_once('a'):
      return f'{to_add}: Double $$a'
    
    if bib.data_field_exists_more_than_once(TAG_FOR_CALL_NUMBER):
      return f'{to_add}: Duplicate call numbers'
    
    call_a = bib.get_data_field(TAG_FOR_CALL_NUMBER, 'a').get_text()
    if call_a == None:
      return f'{to_add}: No call number'
    
    call_b = bib.get_data_field(TAG_FOR_CALL_NUMBER, 'b').get_text()
    if call_b == None:
      return f'{to_add}: Incomplete call number'
    
    if 'LAW' not in call_a and 'PER' not in call_b:
      return f'{call_a} {call_b}'
    
    return f'{to_add}: Text Call Number'
  
  @staticmethod
  def eval_coding(bib: Bib) -> str:
    to_add = 'Manually Review:\n'
    if False:
      to_add += '- Spacing in field 300c\n'
    
    df_505 = bib.get_data_field('505')
    if df_505 == None and df_505.data_subfield_exists_more_than_once('a'):
      to_add += '- Subfield $$a coding in field 505\n'
      
    df_520 = bib.get_data_field('520')
    if df_520 == None and df_520.data_subfield_exists_more_than_once('a'):
      to_add += '- Subfield $$a coding in field 520\n'
      
    call_a = bib.get_data_field(TAG_FOR_CALL_NUMBER, 'a').get_text()
    if call_a != None:
      if call_a[:2] == 'PZ':
        to_add += '- PZ call number\n'
      if 'PS8' in call_a:
        if '.' in call_a:
          dot_idx = call_a.index('.')
          call_a = call_a[:dot_idx]
        if len(call_a) == 6:
          to_add += ': Canadian literature\n'
    
    any_problem = to_add != 'Manually Review:\n'
    if any_problem:
      return to_add
    return ''
  

  # Start of the OCLC number evaluation
  @staticmethod
  def eval_OCLC(bib: Bib) -> str:
     
     df_035 = bib.get_data_field(TAG_FOR_OCLC_NUMBER, 'a').get_text()
     try:
      OCLC = df_035.split(')')[1] # OCLC number is returned as (OCoLC)#########. This takes care of that formatting. May want to look for multiple 035 entries?
      if df_035 == None:
          to_add = "Missing OCLC Number"
      elif OCLC.isnumeric():
          to_add = OCLC
      else:
          to_add = "OCLC not readable"
     except Exception:
        to_add = "OCLC not readable"

     return to_add
  
  @staticmethod
  def eval_nature(bib: Bib) -> dict[bool]:
    """
    Returns a dictionary with index and bibliography
    Nature[index] is True if 'index' is present in the 504 or 500 fields
    Nature[bibliography] is True is 'bibliograph' is present in 504 field
    """

    Nature_dict = {
       "index" : False,
       "bibliography" : False
    }

    try: # Trying to find the 504
      nature = bib.get_data_field(TAG_FOR_NATURE,'a').get_text().lower()
      if "index" in nature:
        Nature_dict["index"] = True
      if "bibliograph" in nature:
          Nature_dict["bibliography"] = True
    except Exception:
      pass

    try: # Trying to find the 500
      index = bib.get_data_field(TAG_FOR_INDEX,'a').get_text().lower()
      if "index" in index:
         Nature_dict["index"] = True
    except Exception:
      return Nature_dict
      
    return Nature_dict
  
  @staticmethod
  def compare_illustrations(bib: Bib) -> str:
    """
    Returns a string to be outputted to the spreadsheet if there are any issues with the illustration fields
    Illustration data is kept in both data field 300 as plain text, and the 008 control field as encoded characters
    These fields are compared, any mismatches are reported on the output spreadsheet
    to_add = "Illustration mismatch" to highlight any problems
    """
    ill_translate = { # allows translation between data field and 008 code
       "a" : 'illustration',
       "b" : 'map',
       "f" : 'plate'
    }

    data_field_illustrations = { # pairs 008 code with wether it appears in the data field
       "a" : False,
       "b" : False,
       "f" : False
    }
    
    ill_008 = bib.extract_008("Illustrations")
    try:
      if "plates" in bib.get_data_field(TAG_FOR_ILLUSTRATIONS, 'a').get_text().lower():
         data_field_illustrations["f"] = True
      illustrations = bib.get_data_field(TAG_FOR_ILLUSTRATIONS, 'b').get_text().lower()
    except Exception:
      illustrations = ""

    for key in data_field_illustrations.keys(): # Checks the data field against the 008
       if ill_translate[key] in illustrations:
          data_field_illustrations[key] = True
       if data_field_illustrations[key] == True and key not in ill_008:
          return "Illustration mismatch"
    
    for char in ill_008.split(): # Checks the 008 against the data field
      try:
        if data_field_illustrations[char] == False:
          return "Illustration mismatch"
      except Exception: # If there is any value that isnt an a, b or f in 008
          pass

    return ""
  
  @staticmethod
  def compare_bibliography(bib: Bib) -> str:
    """
    First evaluates the nature field (504) to check if 'bibliograph' is in the plain text
    Compares this with the 008 field which should contain "b" if bibliographies present
    to_add = "Bibliography mismatch" if the fields don't match and is reported on the spreadsheet
    """
    to_add = ""
    nature_dict = Triage.eval_nature(bib)
    bib_008 = bib.extract_008("Nature")

    bibliography_in_008 = False

    if "b" in bib_008:
       bibliography_in_008 = True

    if bibliography_in_008 != nature_dict["bibliography"]: # Checks for True True, False False
      to_add += "Bibliography mismatch"

    return to_add
  
  @staticmethod
  def compare_index(bib: Bib) -> str:
    """
    First evaluates the nature field (504) & index field (500) to check if 'index' is in the plain text
    Compares this with the 008 field which should contain "1" if index present
    to_add = "Index mismatch" if the fields don't match and is reported on the spreadsheet
    """
    to_add = ""
    nature_dict = Triage.eval_nature(bib)
    index_008 = bib.extract_008("Index")

    index_in_008 = False
    if index_008 == "1":
      index_in_008 = True

    if index_in_008 != nature_dict["index"]: # Checks for True True, False False
      to_add += "Index mismatch"

    return to_add
  
  @staticmethod
  def eval_publication(bib: Bib) -> str:
     """
     The only unacceptable value in the 008 is xx
     Missing is returned and outputted to the spreadsheet if this code is present
     """
     if bib.extract_008("Place_pub") == 'xx ':
        return "Missing"
     else:
        return "" 


columns_to_eval_funcs = { # Output columns that require evaluation by the program and cannot just be stripped from the input spreadsheet
  'OCLC#' : Triage.eval_OCLC,
  'Floor_Status': Triage.eval_location,
  'Size_Status': Triage.eval_size,
  'Format_Assessment': Triage.eval_format,
  'Call_Number_Assessment': Triage.eval_call_number,
  'Brief_Level': Triage.compute_brief_level,
  'Overall_Condition': Triage.eval_brief_level,
  'Illustration_Status' : Triage.compare_illustrations,
  'Bibliography_Status' : Triage.compare_bibliography,
  'Index_Status' : Triage.compare_index,
  'Pub_Locn' : Triage.eval_publication,
  'Coding_Problems': Triage.eval_coding,
}
