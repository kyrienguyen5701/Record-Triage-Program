@Echo off
set /p InputFilePath="Drag and drop the excel/csv file here (Press ENTER to skip): "
set /p OutputFilePath="Name your new output file WITHOUT SPACE or drop another file for overriding (Press ENTER to add _triaged to the input file): "
if "%InputFilePath%" == "" set "InputFilePath=%~dp0results.xlsx"
if "%OutputFilePath%" == "" set "OutputFilePath=%InputFilePath:~0,-5%_triaged.xlsx"
echo Input file: %InputFilePath%
echo Output file: %OutputFilePath%
py src\main.py -if %InputFilePath% -of %OutputFilePath%
REM move %OutputFilePath% outputs
pause
