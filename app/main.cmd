@Echo off

:: Navigate to correct dir regardless of shortcut location
CD /D %~dp0

set /p InputFilePath="Drag and drop the excel/csv file here (Press ENTER to skip): "
set /p OutputFilePath="Name your new output file WITHOUT SPACE or drop another file for overriding (Press ENTER to add _triaged to the input file): "

:: Set filename to _triaged
:: Set filepath to the desktop folder created by setup.cmd
IF "%OutputFilePath%" == "" set "OutputFileName=%InputFilePath:~0,-5%_triaged.xlsx"

FOR %%a IN ("%InputFilepath%") DO ( set "OutputFilename=%%~nxa")

:: Create desktop file if not already exists
if not EXIST "%userprofile%\Desktop\Triage Outputs" mkdir "%userprofile%\Desktop\Triage Outputs"

set OutputFilePath="%userprofile%\Desktop\Triage Outputs\%OutputFilename:~0,-5%_triaged.xlsx"

:: Used for debugging with config file
:: if "%InputFilePath%" == "" set "InputFilePath=%~dp0\src\results.xlsx"
:: if "%OutputFilePath%" == "" ( set "OutputFilePath=%InputFilePath:~0,-5%_triaged.xlsx" ) else ( set "OutputFilePath=%~dp0outputs\%OutputFilePath%" )

echo Input file: %InputFilePath%
echo Output file: %OutputFilePath%
py src\main.py -if %InputFilePath% -of %OutputFilePath%

pause