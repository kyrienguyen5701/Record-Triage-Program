@Echo off

:: Navigate to correct dir regardless of shortcut location
CD /D %~dp0
set dir_indicator = "\"

set /p InputFilePath="Drag and drop the excel/csv file here (Press ENTER to skip): "
set /p OutputFileName="Name your new output file WITHOUT SPACE or drop another file for overriding (Press ENTER to add _triaged to the input file): "

:: Set filename to _triaged
:: Set filepath to the desktop folder created by setup.cmd
@setlocal enabledelayedexpansion
IF "%OutputFileName%" == "" (
    for %%a in (%InputFilePath%) do (
    set filename=%%~na
    )    
    set OutputFilePath="%userprofile%\Desktop\Triage Outputs\!filename!_triaged.xlsx"
) ELSE (
    set "OutputFilePath=%OutputFileName%"
    set OutputFilePath="%userprofile%\Desktop\Triage Outputs\%OutputFilePath%.xlsx"

)

:: Create desktop file if not already exists
if not EXIST "%userprofile%\Desktop\Triage Outputs" mkdir "%userprofile%\Desktop\Triage Outputs"

:: Used for debugging with config file
:: if "%InputFilePath%" == "" set "InputFilePath=%~dp0\src\results.xlsx"
:: if "%OutputFilePath%" == "" ( set "OutputFilePath=%InputFilePath:~0,-5%_triaged.xlsx" ) else ( set "OutputFilePath=%~dp0outputs\%OutputFilePath%" )

echo Input file: %InputFilePath%
echo Output file: %OutputFilePath%
py src\main.py -if %InputFilePath% -of %OutputFilePath%

@echo off
set params=%*
start excel %OutputFilePath% /e/%params%