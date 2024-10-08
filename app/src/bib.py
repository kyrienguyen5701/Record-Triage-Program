from __future__ import annotations
from collections import deque
import xmltodict
from almapipy import AlmaCnxn
from dotenv import load_dotenv
import os
import rule
from logger import bib_logger
import traceback

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

API_KEY = os.getenv('ALMA_API_KEY')
FORMAT = 'json'
alma = AlmaCnxn(API_KEY, data_format=FORMAT)
TAG_FOR_CALL_NUMBER = '050'
TAG_FOR_OCLC_NUMBER = '035'
TAG_FOR_ILLUSTRATIONS = '300'
TAG_FOR_INDEX = '504'
TAG_FOR_LANG = '040'


# Lays out the format in which the 008 is received. The numbers correspont to the number of characters in the string that represent that field
# The order must be maintained in this way
FORMAT_008 = {
  "Date_file" : 6,
  "Pub_type" : 1,
  "Date_1" : 4,
  "Date_2" : 4,
  "Place_pub" : 3,
  "Illustrations_1" : 1,
  "Illustrations_2" : 1,
  "Illustrations_3" : 1,
  "Illustrations_4" : 1,
  "Target_audience" : 1,
  "Form" : 1,
  "Nature_1" : 1,
  "Nature_2" : 1,
  "Nature_3" : 1,
  "Nature_4" : 1,
  "Gov_pub" : 1,
  "Conf_pub": 1,
  "Festschrift": 1,
  "Index" : 1,
  "Undef" : 1,
  "Literary_form" : 1,
  "Bib" : 1,
  "Lang" : 3,
  "Modified_rec" : 1,
  "Cat_source" : 1
}

class Field:
  
  def __init__(self, mmsID, data=dict()):
    self.mmsID = mmsID
    self.data = data
    
  def get_text(self):
    return self.data.get('#text')
  
  def __eq__(self, other):
    if len(self.data) == 0 and other is None:
      return True
    return False
    
class ControlField(Field):
  
  def __init__(self, mmsID, data=dict()):
    super().__init__(mmsID, data)
    
class DataField(Field):
  
  def __init__(self, mmsID, data=dict()):
    super().__init__(mmsID, data)
    
  def data_subfield_exists_more_than_once(self, code: str) -> bool:
    """
    Check if a subfield with the given code exists more than once in the data field.
    
    Params:
    -----------
    code : str
        The code of the subfield to check for.
    
    Returns:
    --------
    bool
        True if a subfield with the given code exists more than once in the data field,
        False otherwise.
    """
    try:
      counter = 0
      sub_fields = self.data.get('subfield', [])
      if type(sub_fields) != list:
        sub_fields = [sub_fields]
      for sub_field in sub_fields:
        if sub_field['@code'] == code:
          counter += 1
          if counter > 1:
            return True
      return False
    except Exception as e:
      tag = self.data['@tag']
      bib_logger.critical(f'Something wrong with data field {tag}{code} of {self.mmsID}')
      bib_logger.error(traceback.format_exc())
      bib_logger.warn(self.data)
      return False
  
# may need to re-consider this implementation
# since subfield only has a @code and a #text
class SubField(Field):
  
  def __init__(self, mmsID, data=dict()):
    super().__init__(mmsID, data)

class Bib:
  
  def __init__(self, mmsID):
    self.create_bib(mmsID)
    
  def create_bib(self, mmsID: str) -> None:
    self.bib = alma.bibs.catalog.get(mmsID)
    bib_logger.info(f'Getting information for {mmsID} ...')
    marc_xml = self.bib['anies'][0]
    self.marc = xmltodict.parse(marc_xml)['record']
    self.leader = self.marc['leader']
    self.control_field = self.marc['controlfield']
    self.data_field = self.marc['datafield']
    
  def compute_brief_level(self) -> int:
    """
    Compute the brief level based on specific conditions of the bib record.

    Returns:
        int: The brief level for the bib record.
    """
    try:
      encoding_position = 17
      encoding_value = self.leader[encoding_position]
      ops = {
        'eq': '==',
        'ne': '!='
      }
      value_of_042a = self.get_data_field('042', 'a').get_text()
      
      # Brief 10: Filter for Full records by national cataloging agencies
      # Based on the documented dynamic that the position 17 (Encoding Level) of the LDR when coded with the following values is deemed a Full record or is fully input by a national-level cataloging authority (i.e. by a national library or national library authorized surrogate agency)
      # " " MARC 21 Full Level (reserved for national library use in OCLC)
      # "I" OCLC Full level from member library (with added check for presence of pcc imprimatur in the 042 field)
      # Note as OCLC loosens the validation routines on LDR/17, then member libraries can also contribute with value blank " ", resulting in "false positives" for Brief 10.
      brief_10 = rule.Rule(rule.Condition(encoding_value, ops['eq'], ' '), 10)
      sub_rule_10 = rule.Rule(rule.Condition(encoding_value, ops['eq'], 'I'))
      sub_rule_10.add_and(rule.Condition(value_of_042a, ops['eq'], 'pcc'))
      brief_10.add_or(sub_rule_10)
      if brief_10.evaluate():
        return 10
      
      # Brief 09: Filter for Full records by non-PCC member contributors
      # Based on the documented dynamic that the position 17 (Encoding Level) of the LDR when coded with the following values is deemed a Full record but is not fully input by a national-level cataloging authority (i.e. not by a national library or national library authorized surrogate agency)
      # Note as OCLC loosens the validation routines on LDR/17, then member libraries can also contribute with value blank " ", resulting in "false positives" for Brief 10.
      # "1" MARC 21 Full Level, Material not examined 
      # "L" OCLC Added from Batch (with higher scrutiny than the M level, but now deprecated)
      # "l" Ex Libris Added from Batch (parallels the OCLC L value)
      # "i" Ex Libris Full level from member library (parallels the OCLC I value)
      # "I" OCLC Full level from member library (with added check for absence of pcc imprimatur in the 042 field)
      brief_09 = rule.Rule(rule.Condition(encoding_value, ops['eq'], '1'), 9)
      brief_09.add_or(rule.Condition(encoding_value, ops['eq'], 'l'))
      brief_09.add_or(rule.Condition(encoding_value, ops['eq'], 'L'))
      brief_09.add_or(rule.Condition(encoding_value, ops['eq'], 'i'))
      sub_rule_09 = rule.Rule(rule.Condition(encoding_value, ops['eq'], 'I'))
      sub_rule_09.add_and(rule.Condition(value_of_042a, ops['ne'], 'pcc'))
      brief_09.add_or(sub_rule_09)
      if brief_09.evaluate():
        return 9
      
      # Brief 08: Filter for Core level records
      # Based on the documented dynamic that the position 17 (Encoding Level) of the LDR when coded with the following values is deemed a Core level record 
      # "4" MARC 21 Core Level
      brief_08 = rule.Rule(rule.Condition(encoding_value, ops['eq'], '4'), 8)
      if brief_08.evaluate():
        return 8
      
      # Brief 07: Filter for Minimal or Less than Full records
      # Based on the documented dynamic that the position 17 (Encoding Level) of the LDR when coded with the following values is deemed a Minimal or Less-than-Full record
      # "7" MARC 21 Minimal Level
      # "2" MARC 21 Less-than-full Level, Material not examined
      # "K" OCLC Minimal Level by OCLC participants
      # "k" Ex Libris Minimal Level (parallels the OCLC K value)
      brief_07 = rule.Rule(rule.Condition(encoding_value, ops['eq'], '7'), 7)
      brief_07.add_or(rule.Condition(encoding_value, ops['eq'], 'K'))
      brief_07.add_or(rule.Condition(encoding_value, ops['eq'], 'k'))
      brief_07.add_or(rule.Condition(encoding_value, ops['eq'], '2'))
      if brief_07.evaluate():
        return 7
      
      # Brief 06: Filter for Call number problems -- lacking altogether or multiple 050
      # Based on the policy dynamic that records lacking a LCC call number or having multiple LCC call numbers warrant extra attention before delivery from the Acquisitions/Cataloging workflow
      sub_rule_06 = rule.Rule(rule.Condition(self.get_data_field(TAG_FOR_CALL_NUMBER), ops['eq'], None))
      sub_rule_06.add_and(rule.Condition(self.get_data_field('090'), ops['eq'], None))
      sub_rule_06.add_and(rule.Condition(self.get_data_field('099'), ops['eq'], None))
      sub_rule_06.add_and(rule.Condition(self.get_data_field('086'), ops['eq'], None))
      brief_06 = rule.Rule(sub_rule_06, 6)
      brief_06.add_or(rule.Condition(self.data_field_exists_more_than_once(TAG_FOR_CALL_NUMBER), ops['eq'], True))
      if brief_06.evaluate():
        return 6
      
      # Brief 05: Filter for CIP Prepublication records
      # Based on the documented dynamic that the position 17 (Encoding Level) of the LDR when coded with the following value is deemed a CIP record
      # "8" MARC 21 Prepublication Level
      brief_05 = rule.Rule(rule.Condition(encoding_value, ops['eq'], '8'), 5)
      if brief_05.evaluate():
        return 5
      
      # Brief 04: Filter for locally keyed records – with field 597 having 
      # Keyed record or Recon Keyed record
      # Based on a desire at some point to be able to easily identify locally keyed records to future review and enhancement
      brief_04 = rule.Rule(rule.Condition(self.get_data_field('597', 'a').get_text(), ops['eq'], 'keyed record'), 4)
      if brief_04.evaluate():
        return 4
      
      # Brief 03: Filter for Partial and Extracted, aka Preliminary records
      # Based on the documented dynamic that the position 17 (Encoding Level) of the LDR when coded with the following values is deemed a preliminary record
      # "5" MARC 21 Partial (preliminary) Level
      # "M" OCLC Added from Batch Process
      # "m" Ex Libris Added from Batch Process
      brief_03 = rule.Rule(rule.Condition(encoding_value, ops['eq'], '5'), 3)
      brief_03.add_or(rule.Condition(encoding_value, ops['eq'], 'M'))
      brief_03.add_or(rule.Condition(encoding_value, ops['eq'], 'm'))
      if brief_03.evaluate():
        return 3
      
      # Brief 02: Filter for Deficient records
      # Based on the documented dynamic that the position 17 (Encoding Level) of the LDR when coded with the following values is deemed a deficient record
      # "3" MARC 21 Abbreviated Level (also deployed by some vendors for "discovery" records consisting of ISBN, Title, Publisher, and Date)
      # "J" OCLC Deleted Record
      # "u" MARC 21 Unknown level
      # "z" MARC 21 Not applicable
      brief_02 = rule.Rule(rule.Condition(encoding_value, ops['eq'], '3'), 2)
      brief_02.add_or(rule.Condition(encoding_value, ops['eq'], 'J'))
      brief_02.add_or(rule.Condition(encoding_value, ops['eq'], 'u'))
      brief_02.add_or(rule.Condition(encoding_value, ops['eq'], 'z'))
      if brief_02.evaluate():
        return 2
      
      # Brief 01: Filter for Acquisition Brief Records
      # Based on the observed dynamic that the position 18 (Descriptive Cataloging Form) of the LDR is coded as "u" in vendor records
      tmp = self.marc['leader'][18]
      brief_01 = rule.Rule(rule.Condition(tmp, ops['eq'], 'u'), 1)
      if brief_01.evaluate():
        return 1
      
      # default value
      return 2
    except Exception as e:
      bib_logger.critical(f'Cannot compute brief level for {self.bib["mms_id"]}. Return 2 as default')
      bib_logger.error(traceback.format_exc())
      return 2
    
  def get_data_field(self, tag: str, code=None) -> DataField:
    """
    Returns a DataField object with the specified @tag and optional @code.

    Params:
        tag (str): The @tag value to search for.
        code (str): An optional @code value to search for.

    Returns:
        Field: A Field object with the specified @tag and optional @code,
            or an empty Field if no matching DataField is found.
    """
    try:
      for data_field in self.data_field:
        if data_field['@tag'] == tag:
          df_obj = DataField(self.bib['mms_id'], data_field)
          if code and data_field.get('subfield'):
            sub_fields = data_field['subfield']
            if type(sub_fields) != list:
              sub_fields = [sub_fields]
            for sub_field in sub_fields:
              if sub_field['@code'] == code:
                sf_obj = SubField(self.bib['mms_id'], sub_field)
                return sf_obj
            return SubField(self.bib['mms_id'])
          return df_obj
      return DataField(self.bib['mms_id'])
    except Exception as e:
      code = code if code else ''
      bib_logger.critical(f'Something wrong with data field {tag}{code} of {self.bib["mms_id"]}.')
      bib_logger.error(traceback.format_exc())
      return DataField(self.bib['mms_id'])
    
  def get_control_field(self, tag: str, code=None) -> DataField:
    """
    Returns a DataField object -> one of the 3 datafields in each Alma entry dependent on @tag

    Params:
        tag (str): The @tag to search by (currently one of three - 001, 005, 008)
        code (str): Not yet implemented. It is not yet clear wether this is necessary for control fields

    Returns:
        Field: A Field object with the specified @tag
            or an empty Field if no matching DataField is found.

    """
    try:
      for control_field in self.control_field:
        if control_field['@tag'] == tag:
          df_obj = ControlField(self.bib['mms_id'], control_field)
          return df_obj
    except Exception as e:
      bib_logger.critical(f'Something wrong with control field {tag}{code} of {self.bib["mms_id"]}.')
      bib_logger.error(traceback.format_exc())
      return ControlField(self.bib['mms_id'])

  
  def data_field_exists_more_than_once(self, tag: str) -> bool:
    """
    Returns True if the specified @tag appears more than once in the list of data fields.

    Params:
        tag (str): The @tag value to search for.

    Returns:
        bool: True if the specified @tag appears more than once in the list of data fields,
            False otherwise.
    """
    try:
      counter = 0
      for df in self.data_field:
        if df['@tag'] == tag:
          counter += 1
          if counter > 1:
            return True
      return False
    except Exception as e:
      bib_logger.critical(f'Something wrong with data field {tag} of {self.bib["mms_id"]}.')
      bib_logger.error(traceback.format_exc())
      return False
  
  # Try to make sense of the string 008 recieved from the alma bib
  # Will need changing if alma decides to add more to the 008 field
  def extract_008(self):

    str_008 = deque(self.get_control_field('008').get_text())
    Item = {}

    for key in FORMAT_008.keys():
      # print(str_008)
      temp = ""
      for chars in range (0, FORMAT_008[key]):
        try:
          temp += str_008.popleft()
        except Exception:
          temp = ""
      Item[key] = temp # This creates a dictionary of the 008 entries. Needs appending to a dataframe

    return Item


