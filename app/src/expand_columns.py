import openpyxl

def expand_columns(filepath):


    wb = openpyxl.load_workbook(filename = filepath)        
    worksheet = wb.active

    column_widths = {
        'A' : 22,
        'B' : 14,
        'C' : 27,
        'D' : 32,
        'E' : 32,
        'F' : 27,
        'G' : 37,
        'H' : 12,
        'I' : 40,
        'J' : 20,
        'K' : 23,
        'L' : 23,
        'M' : 23,
        'N' : 23,
        'O' : 23}

    for column in column_widths.keys():
        worksheet.column_dimensions[column].width = column_widths[column]

    wb.save(filepath)