@Echo off
set /p InputFilePath="Drag and drop the excel/csv file here (Press ENTER to skip): "
set /p OutputFilePath="Name your new output file or drop another file for overriding (Press ENTER to skip): "
if "%InputFilePath%" == "" set "InputFilePath=%~dp0results.xlsx"
if "%OutputFilePath%" == "" set "OutputFilePath=%~dp0triage_output.xlsx"
py main.py -if "%InputFilePath%" -of "%OutputFilePath%"
pause
