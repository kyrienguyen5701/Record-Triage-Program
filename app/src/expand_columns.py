import openpyxl

def expand_columns(filepath):


    wb = openpyxl.load_workbook(filename = filepath)        
    worksheet = wb.active

    column_widths = {
        'A' : 22, # MMS ID
        'B' : 15, # OCLC Number
        'C' : 27, # Floor Status
        'D' : 32, # Size Status
        'E' : 32, # Format Assessment
        'F' : 35, # Call Number
        'G' : 37, # Title
        'H' : 14, # Brief Level
        'I' : 40, # Overall Condition
        'J' : 23, # Illustration Status
        'K' : 25, # Bibliography Status
        'L' : 23, # Index Status
        'M' : 17, # Pub Location
        'N' : 23 # Coding Problems
        }

    for column in column_widths.keys():
        worksheet.column_dimensions[column].width = column_widths[column]

    wb.save(filepath)